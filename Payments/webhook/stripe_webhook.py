import os
import json
import logging
from typing import Dict, Any
from datetime import datetime

import stripe
import boto3
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stripe-webhook")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
DYNAMODB_PAYMENTS_TABLE = os.getenv("DYNAMODB_PAYMENTS_TABLE", "lea-payments-local")
DDB_ENDPOINT = os.getenv("DDB_ENDPOINT")

if DDB_ENDPOINT:
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION, endpoint_url=DDB_ENDPOINT)
else:
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

payments_table = dynamodb.Table(DYNAMODB_PAYMENTS_TABLE)

app = FastAPI(title="Stripe Webhook Service", version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "stripe-webhook"}

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    logger.info(f"Webhook secret length: {len(STRIPE_WEBHOOK_SECRET)}")
    logger.info(f"Webhook secret: {STRIPE_WEBHOOK_SECRET[:15]}...")
    
    if not STRIPE_WEBHOOK_SECRET:
        logger.error("STRIPE_WEBHOOK_SECRET not configured")
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    try:
        if len(STRIPE_WEBHOOK_SECRET) < 20 or not sig_header:
            logger.warning("Using webhook without signature verification (local testing)")
            event = json.loads(payload.decode('utf-8'))
        else:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        if 'signature' in str(e).lower():
            logger.error(f"Invalid signature: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    event_type = event["type"]
    event_data = event["data"]["object"]
    
    logger.info(f"Received Stripe event: {event_type}")
    
    if event_type == "checkout.session.completed":
        await handle_payment_success(event_data)
    elif event_type == "checkout.session.expired":
        await handle_payment_expired(event_data)
    elif event_type == "payment_intent.payment_failed":
        await handle_payment_failed(event_data)
    else:
        logger.info(f"Unhandled event type: {event_type}")
    
    return JSONResponse({"status": "success"})

async def handle_payment_success(session_data: Dict[str, Any]):
    session_id = session_data.get("id")
    client_reference_id = session_data.get("client_reference_id")
    payment_intent_id = session_data.get("payment_intent")
    
    logger.info(f"Payment successful for session: {session_id}")
    
    if not client_reference_id:
        logger.warning(f"No client_reference_id found for session {session_id}")
        return
    
    try:
        response = payments_table.get_item(Key={"payment_intent_id": client_reference_id})
        payment_record = response.get("Item")
        
        if not payment_record:
            logger.warning(f"Payment record not found for payment_intent_id: {client_reference_id}")
            return
        
        payment_record["payment_status"] = "completed"
        payment_record["stripe_payment_intent"] = payment_intent_id
        payment_record["updated_at"] = datetime.utcnow().isoformat()
        payment_record["webhook_processed_at"] = datetime.utcnow().isoformat()
        
        payments_table.put_item(Item=payment_record)
        
        logger.info(f"Updated payment status to completed for {client_reference_id}")
        
    except Exception as e:
        logger.error(f"Failed to update payment record: {e}")

async def handle_payment_expired(session_data: Dict[str, Any]):
    session_id = session_data.get("id")
    client_reference_id = session_data.get("client_reference_id")
    
    logger.info(f"Payment session expired: {session_id}")
    
    if not client_reference_id:
        logger.warning(f"No client_reference_id found for expired session {session_id}")
        return
    
    try:
        response = payments_table.get_item(Key={"payment_intent_id": client_reference_id})
        payment_record = response.get("Item")
        
        if not payment_record:
            logger.warning(f"Payment record not found for payment_intent_id: {client_reference_id}")
            return
        
        payment_record["payment_status"] = "expired"
        payment_record["updated_at"] = datetime.utcnow().isoformat()
        payment_record["webhook_processed_at"] = datetime.utcnow().isoformat()
        
        payments_table.put_item(Item=payment_record)
        
        logger.info(f"Updated payment status to expired for {client_reference_id}")
        
    except Exception as e:
        logger.error(f"Failed to update expired payment record: {e}")

async def handle_payment_failed(payment_intent_data: Dict[str, Any]):
    payment_intent_id = payment_intent_data.get("id")
    
    logger.info(f"Payment failed for intent: {payment_intent_id}")
    
    try:
        response = payments_table.scan(
            FilterExpression="stripe_payment_intent = :intent_id",
            ExpressionAttributeValues={":intent_id": payment_intent_id}
        )
        
        items = response.get("Items", [])
        if not items:
            logger.warning(f"Payment record not found for intent: {payment_intent_id}")
            return
        
        payment_record = items[0]
        payment_record["payment_status"] = "failed"
        payment_record["updated_at"] = datetime.utcnow().isoformat()
        payment_record["webhook_processed_at"] = datetime.utcnow().isoformat()
        
        payments_table.put_item(Item=payment_record)
        
        logger.info(f"Updated payment status to failed for {payment_record['payment_intent_id']}")
        
    except Exception as e:
        logger.error(f"Failed to update failed payment record: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)

