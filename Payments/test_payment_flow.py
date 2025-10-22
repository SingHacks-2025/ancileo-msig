import os
import sys
import time
import stripe
import boto3
import requests
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-southeast-2',
    endpoint_url='http://localhost:8000',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

payments_table = dynamodb.Table('lea-payments-local')

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_step(step_num, text):
    print(f"{Colors.CYAN}[Step {step_num}]{Colors.RESET} {Colors.BOLD}{text}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def create_payment_intent():
    payment_intent_id = f"test_payment_{uuid.uuid4().hex[:12]}"
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    quote_id = f"quote_{uuid.uuid4().hex[:8]}"
    
    print_step(1, "Creating payment record in DynamoDB with 'pending' status")
    
    payment_record = {
        'payment_intent_id': payment_intent_id,
        'user_id': user_id,
        'quote_id': quote_id,
        'payment_status': 'pending',
        'amount': 5000,
        'currency': 'SGD',
        'product_name': 'Travel Insurance - Test Policy',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    try:
        payments_table.put_item(Item=payment_record)
        print_success(f"Payment record created with ID: {payment_intent_id}")
        print_info(f"Initial status: {Colors.YELLOW}pending{Colors.RESET}")
        return payment_intent_id, user_id, quote_id
    except Exception as e:
        print_error(f"Failed to create payment record: {e}")
        sys.exit(1)

def create_stripe_checkout(payment_intent_id, amount, product_name):
    print_step(2, "Creating Stripe Checkout Session")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'sgd',
                    'unit_amount': amount,
                    'product_data': {
                        'name': product_name,
                        'description': 'Travel Insurance Policy',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'http://localhost:8085/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url='http://localhost:8085/cancel',
            client_reference_id=payment_intent_id,
        )
        
        payments_table.update_item(
            Key={'payment_intent_id': payment_intent_id},
            UpdateExpression='SET stripe_session_id = :sid',
            ExpressionAttributeValues={':sid': checkout_session.id}
        )
        
        print_success("Stripe Checkout Session created")
        print_info(f"Session ID: {checkout_session.id}")
        return checkout_session
        
    except Exception as e:
        print_error(f"Failed to create Stripe session: {e}")
        sys.exit(1)

def check_payment_status(payment_intent_id):
    try:
        response = payments_table.get_item(Key={'payment_intent_id': payment_intent_id})
        item = response.get('Item')
        if item:
            return item.get('payment_status', 'unknown')
        return None
    except Exception as e:
        print_error(f"Failed to check payment status: {e}")
        return None

def check_stripe_payment_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status, session
    except Exception as e:
        print_error(f"Failed to check Stripe status: {e}")
        return None, None

def trigger_local_webhook(session_data):
    print_info("Triggering local webhook endpoint...")
    
    webhook_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session_data.id,
                "client_reference_id": session_data.client_reference_id,
                "payment_intent": session_data.payment_intent,
                "payment_status": session_data.payment_status
            }
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8086/webhook/stripe",
            json=webhook_event,
            timeout=5
        )
        if response.status_code == 200:
            print_success("Webhook triggered successfully")
            return True
        else:
            print_error(f"Webhook returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to trigger webhook: {e}")
        return False

def wait_for_payment_confirmation(payment_intent_id, session_id):
    print_step(4, "Checking payment status on Stripe")
    print_info("Polling Stripe API for payment completion...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        payment_status, session_data = check_stripe_payment_status(session_id)
        
        if payment_status == 'paid':
            print_success("Payment confirmed on Stripe!")
            print_info(f"Payment Status: {payment_status}")
            
            trigger_local_webhook(session_data)
            
            time.sleep(2)
            
            db_status = check_payment_status(payment_intent_id)
            if db_status == 'completed':
                print_success("Database status updated to 'completed'!")
                return True
            else:
                print_info(f"Database status: {db_status} (waiting for webhook processing...)")
                time.sleep(2)
                db_status = check_payment_status(payment_intent_id)
                if db_status == 'completed':
                    print_success("Database status confirmed as 'completed'!")
                    return True
        
        if attempt < max_attempts - 1:
            print(f"   Stripe status: {payment_status or 'checking...'} - Retrying in 2 seconds... ({attempt + 1}/{max_attempts})")
            time.sleep(2)
    
    print_error("Payment was not completed within timeout")
    return False

def cleanup(payment_intent_id):
    try:
        payments_table.delete_item(Key={'payment_intent_id': payment_intent_id})
        print_info(f"Cleaned up test payment record: {payment_intent_id}")
    except:
        pass

def main():
    print_header("LEA Payment Services - Interactive Payment Flow Test")
    
    print(f"{Colors.BOLD}This test will:{Colors.RESET}")
    print("1. Create a payment record with 'pending' status")
    print("2. Generate a real Stripe payment link")
    print("3. Wait for you to make the payment")
    print("4. Check Stripe API and trigger local webhook")
    print("5. Verify the status changed to 'completed'")
    print("6. Confirm payment received\n")
    
    print(f"{Colors.GREEN}✓ No Stripe CLI needed - works with Docker services only!{Colors.RESET}\n")
    
    input(f"{Colors.YELLOW}Press Enter to start the test...{Colors.RESET}")
    
    payment_intent_id, user_id, quote_id = create_payment_intent()
    
    initial_status = check_payment_status(payment_intent_id)
    print_info(f"Current DB status: {Colors.YELLOW}{initial_status}{Colors.RESET}\n")
    
    checkout_session = create_stripe_checkout(
        payment_intent_id,
        5000,
        'Travel Insurance - Test Policy'
    )
    
    print_step(3, "Make Payment on Stripe")
    print(f"\n{Colors.BOLD}Please open this link to make payment:{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{checkout_session.url}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}Test Card Details:{Colors.RESET}")
    print("  Card Number: 4242 4242 4242 4242")
    print("  Expiry: Any future date (e.g., 12/34)")
    print("  CVC: Any 3 digits (e.g., 123)")
    print("  ZIP: Any 5 digits (e.g., 12345)\n")
    
    user_input = input(f"{Colors.BOLD}After completing payment, type 'done paid' and press Enter: {Colors.RESET}").strip().lower()
    
    if user_input == 'done paid':
        print()
        if wait_for_payment_confirmation(payment_intent_id, checkout_session.id):
            print()
            print_step(5, "Application Response")
            final_status = check_payment_status(payment_intent_id)
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Okay payment made, thank you!{Colors.RESET}")
            print(f"{Colors.GREEN}Payment Status: {final_status}{Colors.RESET}")
            print(f"{Colors.GREEN}Payment ID: {payment_intent_id}{Colors.RESET}\n")
            
            print_header("Test Summary")
            print(f"{Colors.GREEN}✓ Step 1: Payment record created with 'pending' status{Colors.RESET}")
            print(f"{Colors.GREEN}✓ Step 2: Stripe checkout link generated{Colors.RESET}")
            print(f"{Colors.GREEN}✓ Step 3: User completed payment on Stripe{Colors.RESET}")
            print(f"{Colors.GREEN}✓ Step 4: Payment verified via Stripe API{Colors.RESET}")
            print(f"{Colors.GREEN}✓ Step 5: Local webhook triggered and DB updated{Colors.RESET}")
            print(f"{Colors.GREEN}✓ Step 6: Application confirmed payment{Colors.RESET}\n")
            
            keep_record = input(f"{Colors.YELLOW}Keep test record in database? (y/n): {Colors.RESET}").strip().lower()
            if keep_record != 'y':
                cleanup(payment_intent_id)
            
            sys.exit(0)
        else:
            print()
            print_error("Payment was not confirmed")
            print_info("This might mean:")
            print("  - Payment was not completed on Stripe")
            print("  - Webhook service is not running")
            print("  - There was an error processing the payment")
            
            check_anyway = input(f"\n{Colors.YELLOW}Check current status anyway? (y/n): {Colors.RESET}").strip().lower()
            if check_anyway == 'y':
                final_status = check_payment_status(payment_intent_id)
                print(f"Current status: {final_status}")
            
            cleanup(payment_intent_id)
            sys.exit(1)
    else:
        print_error(f"Invalid input: '{user_input}'. Expected 'done paid'")
        cleanup(payment_intent_id)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

