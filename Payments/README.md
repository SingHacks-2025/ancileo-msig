# Ancileo x MSIG Hackathon - Payment Services

A lightweight Stripe payment integration system for Insurance travel insurance payments.

## What It Does

This service handles the complete payment flow:
1. Creates payment records in DynamoDB with `pending` status
2. Generates Stripe checkout sessions for users to pay
3. Listens to Stripe webhook events (payment success/failure/expiry)
4. Updates payment status in DynamoDB to `completed`, `failed`, or `expired`
5. Shows users success/cancel pages after payment

## Architecture

```
┌─────────────────┐
│  DynamoDB Local │  ← Payment records storage
└────────┬────────┘
         │
         ├─────────────────────┐
         │                     │
┌────────▼────────┐   ┌────────▼─────────┐
│ Stripe Webhook  │   │  Payment Pages   │
│   Port: 8086    │   │   Port: 8085     │
└─────────────────┘   └──────────────────┘
         ▲
         │
         │ Webhook events
         │
┌────────┴────────┐
│  Stripe API     │
└─────────────────┘
```

## Services

| Service | Port | Purpose |
|---------|------|---------|
| **DynamoDB Local** | 8000 | Local NoSQL database for payment records |
| **DynamoDB Admin** | 8010 | Web UI to view DynamoDB tables |
| **Stripe Webhook** | 8086 | Receives Stripe events and updates DB |
| **Payment Pages** | 8085 | Success/cancel pages after checkout |

## Quick Start

### 1. Set Environment Variables

Create a `.env` file:

```bash
# Required
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Optional (defaults shown)
AWS_REGION=ap-southeast-1
DYNAMODB_PAYMENTS_TABLE=lea-payments-local
```

### 2. Start Services

```bash
docker-compose up -d
```

This will:
- Start DynamoDB Local
- Create the `lea-payments-local` table with indexes
- Start webhook service
- Start payment pages service

### 3. Verify Services

Check health endpoints:
```bash
curl http://localhost:8086/health  # Stripe webhook
curl http://localhost:8085/health  # Payment pages
```

View DynamoDB tables:
```bash
open http://localhost:8010  # DynamoDB Admin UI
```

## Database Schema

**Table:** `lea-payments-local`

| Field | Type | Description |
|-------|------|-------------|
| `payment_intent_id` | String (PK) | Unique payment identifier |
| `user_id` | String | User identifier |
| `quote_id` | String | Insurance quote identifier |
| `stripe_session_id` | String | Stripe checkout session ID |
| `stripe_payment_intent` | String | Stripe payment intent ID |
| `payment_status` | String | `pending`, `completed`, `failed`, `expired` |
| `amount` | Number | Payment amount in cents |
| `currency` | String | Currency code (e.g., SGD) |
| `product_name` | String | Product description |
| `created_at` | String (ISO) | Record creation timestamp |
| `updated_at` | String (ISO) | Last update timestamp |
| `webhook_processed_at` | String (ISO) | Webhook processing timestamp |

**Indexes:**
- `user_id-index` - Query payments by user
- `quote_id-index` - Query payments by quote
- `stripe_session_id-index` - Query by Stripe session

## API Endpoints

### Stripe Webhook Service (Port 8086)

#### `POST /webhook/stripe`
Receives Stripe webhook events.

**Handled Events:**
- `checkout.session.completed` → Updates status to `completed`
- `checkout.session.expired` → Updates status to `expired`
- `payment_intent.payment_failed` → Updates status to `failed`

**Headers:**
- `stripe-signature` - Stripe webhook signature (auto-verified)

### Payment Pages Service (Port 8085)

#### `GET /success?session_id={id}`
Success page shown after payment completion.

#### `GET /cancel`
Cancel page shown when user cancels payment.

## Payment Flow Example

```python
import stripe
import boto3

# 1. Create payment record
payments_table.put_item(Item={
    'payment_intent_id': 'payment_123',
    'user_id': 'user_456',
    'quote_id': 'quote_789',
    'payment_status': 'pending',
    'amount': 5000,  # $50.00 in cents
    'currency': 'SGD',
    'created_at': '2025-10-15T10:00:00Z'
})

# 2. Create Stripe checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'sgd',
            'unit_amount': 5000,
            'product_data': {'name': 'Travel Insurance'}
        },
        'quantity': 1
    }],
    mode='payment',
    success_url='http://localhost:8085/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='http://localhost:8085/cancel',
    client_reference_id='payment_123'  # Links to our DB record
)

# 3. Redirect user to session.url
# 4. User pays → Stripe sends webhook → Status updated to 'completed'
# 5. User redirected to success page
```

## Testing

Run the interactive payment flow test:

```bash
pip install -r requirements-test.txt
python test_payment_flow.py
```

This will:
1. Create a test payment record
2. Generate a real Stripe payment link
3. Wait for you to complete the payment (use test card: `4242 4242 4242 4242`)
4. Verify webhook processing
5. Confirm status changed to `completed`

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_REGION` | `ap-southeast-1` | AWS region |
| `DYNAMODB_PAYMENTS_TABLE` | `lea-payments-local` | DynamoDB table name |
| `STRIPE_WEBHOOK_SECRET` | *(required)* | Stripe webhook signing secret |
| `DDB_ENDPOINT` | `http://dynamodb:8000` | DynamoDB endpoint (local) |

### Stripe Test Cards

For testing payments:

| Card Number | Result |
|-------------|--------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 9995` | Declined |
| `4000 0000 0000 0341` | Attach succeeded, charge failed |

Use any future expiry date, any 3-digit CVC, and any ZIP code.

## Development

### View Logs

```bash
docker-compose logs -f stripe-webhook
docker-compose logs -f payment-pages
```

### Rebuild Services

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Access DynamoDB Directly

```python
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-southeast-1',
    endpoint_url='http://localhost:8000',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

table = dynamodb.Table('lea-payments-local')
response = table.scan()
print(response['Items'])
```

## Troubleshooting

### Webhook not receiving events
- Check `STRIPE_WEBHOOK_SECRET` is set correctly
- Ensure webhook service is running: `docker-compose ps`
- View logs: `docker-compose logs stripe-webhook`

### Payment status not updating
- Verify webhook received the event (check logs)
- Ensure `client_reference_id` in Stripe session matches `payment_intent_id` in DB
- Check DynamoDB has the record: Visit http://localhost:8010

### Services won't start
- Ensure ports 8000, 8010, 8085, 8086 are not in use
- Check Docker daemon is running
- Verify `.env` file exists with required variables

Proprietary - Ancileo

