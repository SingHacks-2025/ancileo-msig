# Ancileo × MSIG — Conversational Insurance

> **Travel Insurance MCP** — Build an AI assistant that turns travel-insurance conversations into understanding → comparison → quotation → purchase, topped with claims-backed recommendations.

---

## Challenge Summary

**Goal**: Ship a working assistant that can **parse policies** → **answer with citations** → **quote from uploaded trip docs** → **purchase in-chat**.

**Build path**: Implement the **Feature Blocks (1→5)** in order.

> **📖 IMPORTANT**: Before diving into the code, please read the **Next-Generation Conversational Travel Insurance Distribution Hackathon.pdf** document first. It contains essential context, detailed requirements, and additional guidance that will help you build a winning solution.

---

## 📋 The Problem We're Solving

### Current State
- Customers spend **10-30 minutes** filling forms and reading dense policy documents
- No real-time Q&A with an expert
- Manual comparison across products is confusing and error-prone
- High abandonment rates (70%+) due to friction

### What You're Building
- **Conversational Insurance** 
- Upload your policies → get instant personalized quotes
- Ask questions, get answers with exact policy citations
- Complete purchase without leaving the chat

### Who Benefits
- **End users**: Travelers buying insurance through ChatGPT, Claude, or similar AI assistants
- **AI developers**: Building insurance-aware conversational agents
- **Insurance teams**: Transforming distribution channels with AI

---

## 🎯 What You're Building

A system with **5 feature blocks** that work together:

```
┌─────────────────────────────────────────────────────────────────┐
│  Block 1: Parse & Normalize Policy Documents                   │
│  ↓ Turn PDFs into comparable data + keep original text         │
├─────────────────────────────────────────────────────────────────┤
│  Block 2: Conversational Q&A with Citations                    │
│  ↓ Answer questions, compare products, explain differences     │
├─────────────────────────────────────────────────────────────────┤
│  Block 3: Upload Trip Documents → Auto-Quote                   │
│  ↓ Extract flight/hotel info, generate personalized quotes     │
├─────────────────────────────────────────────────────────────────┤
│  Block 4: Purchase In-Chat                                      │
│  ↓ Accept quote → pay → get policy confirmation               │
├─────────────────────────────────────────────────────────────────┤
│  Block 5: Smart Recommendations from Claims Data               │
│  ↓ Use historical claims to suggest best coverage              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Repository Structure — Where to Find What

```
ancileo-msig/
├── README.md                          ← You are here
│
├── Taxonomy/                          ← FOR BLOCK 1 (Normalization)
│   ├── Taxonomy_Hackathon.json       ← Schema to normalize policies into
│   └── Travel Insurance Product Taxonomy - Documentation.pdf
│
├── Policy_Wordings/                   ← FOR BLOCK 1 (Source Documents)
│   ├── Scootsurance QSR022206_updated.pdf
│   ├── TravelEasy Policy QTD032212.pdf
│   └── TravelEasy Pre-Ex Policy QTD032212-PX.pdf
│
├── Payments/                         ← FOR BLOCK 4 (Payments)
│   ├── docker-compose.yaml           ← Local payment stack (DynamoDB + Stripe webhook)
│   ├── webhook/                      ← Stripe webhook service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── stripe_webhook.py
│   ├── payment_pages/                ← Success/cancel pages
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── scripts/                      ← Database initialization
│   │   ├── Dockerfile.init
│   │   └── init_payments_table.py
│   ├── test_payment_flow.py          ← Interactive payment test
│   ├── requirements.txt              ← Python dependencies
│   └── README.md                     ← Detailed payment stack docs
│
└── Next-Generation Conversational Travel Insurance Distribution Hackathon.pdf
```

---

## 🏗️ Feature Blocks — Step-by-Step Build Guide

### Block 1: Parse & Normalize Policy Documents

**What it does**: Converts messy policy PDFs into clean, comparable data while keeping the original text for citations.

**Where to start**: `Taxonomy/Taxonomy_Hackathon.json`

**The Challenge**:
- Insurance policies use different words for the same thing ("medical expenses" vs "healthcare costs")
- Limits are buried in paragraphs ("up to $50,000 per trip, with a sub-limit of $5,000 for dental")
- You need to compare apples-to-apples across 3+ products

**The Solution — Taxonomy Normalization**:

The `Taxonomy_Hackathon.json` file shows you the **target structure**:

```json
{
  "taxonomy_name": "Travel Insurance Product Taxonomy",
  "products": ["Product A", "Product B", "Product C"],
  "layers": {
    "layer_1_general_conditions": [
      {
        "condition": "age_eligibility",
        "condition_type": "eligibility",
        "products": {
          "Product A": {
            "condition_exist": true,
            "original_text": "Travelers must be between 18-75 years old...",
            "parameters": {
              "min_age": 18,
              "max_age": 75
            }
          },
          "Product B": { ... }
        }
      }
    ],
    "layer_2_benefits": [...],
    "layer_3_benefit_conditions": [...],
    "layer_4_operational": [...]
  }
}
```

**Four Layers to Extract**:

1. **Layer 1: General Conditions**
   - Eligibility: age, residency, trip duration, health declarations
   - General exclusions: pre-existing conditions, high-risk activities, war/terrorism

2. **Layer 2: Benefits**
   - Medical coverage, trip cancellation, baggage protection
   - Maximum limits, sub-limits, geographic variations

3. **Layer 3: Benefit-Specific Conditions**
   - When does specific coverage apply?
   - What's excluded under each benefit?
   - Waiting periods, documentation requirements

4. **Layer 4: Operational Details**
   - Deductibles and co-pays
   - Approved provider networks
   - Claims procedures and time limits


### Block 2: Conversational Q&A with Citations

**What it does**: Answers questions intelligently by choosing between normalized data (for comparisons) or original text (for detailed explanations).

**The Challenge**: Users ask questions in plain English. Your system must know whether to use:
- **Normalized data** for "Which plan has better medical coverage?"
- **Original policy text** for "What exactly is covered under medical expenses?"
- **Both** for "What happens if I break my leg skiing in Japan?"

**Query Types**:

| Query Type | Example | Data Source | Output |
|------------|---------|-------------|--------|
| **Comparison** | "Compare medical coverage between Plan A and B" | Normalized taxonomy | Side-by-side matrix with clear differences |
| **Explanation** | "What's covered under trip cancellation?" | Original text + context | Detailed answer with exact policy citations |
| **Eligibility** | "Am I covered for pre-existing conditions?" | Rules + text | Clear yes/no with qualifying conditions |
| **Scenario** | "Skiing accident in Japan—am I covered?" | Multiple benefits/exclusions | Step-by-step coverage analysis |

**Deliverables**:
- [ ] Working MCP tools for comparison and FAQ
- [ ] All answers include citations to original policy text
- [ ] Session memory maintains conversation state
- [ ] Demo: answer 3+ different query types accurately

---

### Block 3: Upload Trip Documents → Auto-Quote

**What it does**: Replace form-filling with document upload. Extract travel details automatically and generate instant quotes.

**The Transformation**:
- ❌ **Old way**: Fill 15-30 form fields manually (20 minutes, 70% abandonment)
- ✅ **New way**: Upload flight booking PDF (2 minutes, instant quote)

**Document Types to Handle**:
- ✈️ Flight confirmations (dates, destinations, traveler names, ticket costs)
- 🏨 Hotel bookings (check-in/out dates, location, investment value)
- 📄 Itineraries (activities, destinations, timeline)
- 🛂 Visa applications (trip purpose, duration)


### Block 4: Purchase In-Chat

**What it does**: Converts accepted quotes into completed policies without leaving the conversation.

**Where to start**: `Payments/` folder

**What's in the Payments folder**:

The `Payments/` folder contains a working payment system with:

```
Payments/
├── docker-compose.yaml          ← Start all services with one command
├── webhook/
│   └── stripe_webhook.py        ← Receives Stripe payment events, updates database
├── payment_pages/
│   └── app.py                   ← Success/cancel pages users see after payment
├── test_payment_flow.py         ← Test the entire flow end-to-end
└── README.md                    ← Detailed docs for the payment stack
```

**The Stack** (runs locally via Docker):

| Service | Port | What It Does |
|---------|------|--------------|
| **DynamoDB Local** | 8000 | Stores payment records |
| **DynamoDB Admin UI** | 8010 | View database contents in browser |
| **Stripe Webhook** | 8086 | Listens for Stripe events, updates payment status |
| **Payment Pages** | 8085 | Shows success/cancel pages after checkout |

**Quick Start**:

```bash
cd Payments/

# 1. Set your Stripe webhook secret
echo "STRIPE_WEBHOOK_SECRET=whsec_your_secret_here" > .env

# 2. Start all services
docker-compose up -d

# 3. Verify everything is running
curl http://localhost:8086/health
curl http://localhost:8085/health
open http://localhost:8010  # View database UI
```

**Payment Flow**:

```python
# 1. Create payment record in database with 'pending' status
payment_record = {
    'payment_intent_id': 'unique_id_123',
    'user_id': 'user_456',
    'quote_id': 'quote_789',
    'payment_status': 'pending',
    'amount': 5000,  # $50.00 in cents
    'currency': 'SGD',
    'product_name': 'Travel Insurance - Premium Plan'
}

# 2. Create Stripe checkout session
session = stripe.checkout.Session.create(
    line_items=[{...}],
    success_url='http://localhost:8085/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='http://localhost:8085/cancel',
    client_reference_id='unique_id_123'  # Links to payment_record
)

# 3. User pays on Stripe
# 4. Webhook receives event → updates status to 'completed'
# 5. User redirected to success page
# 6. Chat shows confirmation
```

**Test the Payment Flow**:

```bash
# Interactive test that walks you through the entire flow
pip install -r Payments/requirements.txt
python Payments/test_payment_flow.py

# It will:
# 1. Create a test payment record
# 2. Generate a real Stripe payment link
# 3. Wait for you to pay (use test card: 4242 4242 4242 4242)
# 4. Verify webhook processed the payment
# 5. Confirm status changed to 'completed'
```

**Your MCP Purchase Tool Should**:
- Create payment record in DynamoDB
- Generate Stripe checkout session
- Monitor webhook updates in real-time
- Report status back to the chat
- Handle errors gracefully (declined cards, expired sessions, etc.)

**Deliverables**:
- [ ] MCP purchase tool that creates Stripe sessions
- [ ] Payment status updates reflected in conversation
- [ ] Success/failure handling with clear user messaging
- [ ] Policy delivery confirmation after successful payment

---

### Block 5: Smart Recommendations from Claims Data

**What it does**: Uses MSIG's historical claims data to recommend the best product tier during quotation.

**Example Scenario**:
```
User uploads: Flight to Japan (skiing trip)
System analyzes: Historical claims for Japan ski trips
Finds: 80% of medical claims exceed $30,000
Recommends: "Based on similar trips, we recommend the Silver plan 
             with $50,000 medical coverage (vs. Bronze at $20,000)"
```

---

## 🏆 Judging Criteria

Your submission will be evaluated on:

### Technical Implementation (25%)
- How well did you process and normalize policy documents?
- Quality of MCP integration and tool implementation
- Code architecture, documentation, and maintainability

### User Experience (20%)
- Natural conversation flow and interaction design
- Clarity of policy comparisons and recommendations
- Ease of understanding complex insurance concepts

### Innovation (20%)
- Creative approaches to policy analysis
- Novel use of MCP capabilities
- Unique features or insights

### Feasibility (20%)
- Realistic path to production deployment
- Scalability considerations (multiple insurers, countries, languages)
- Error handling and edge cases

### Business Impact (15%)
- Potential for market transformation
- Understanding of insurance industry dynamics
- Revenue generation opportunities

## ✅ Features Checklist

### Block 1: Normalization
- [ ] 3+ policies processed into taxonomy structure
- [ ] Completeness validation report
- [ ] Comparison matrix export with citations
- [ ] Documentation of normalization decisions (what was kept/lost)

### Block 2: Conversation
- [ ] MCP tools for comparison and FAQ working
- [ ] All answers include policy text citations
- [ ] Session memory maintains state
- [ ] Demo covers 4 query types (comparison, explanation, eligibility, scenario)

### Block 3: Document Intelligence
- [ ] Upload handler for multiple document formats
- [ ] Extraction with ≥95% accuracy demonstration
- [ ] Cross-document validation working
- [ ] MCP quotation tool integration
- [ ] Conversational clarification for missing data

### Block 4: Purchase
- [ ] Payment stack running (`docker-compose up -d`)
- [ ] MCP purchase tool implemented
- [ ] End-to-end flow: quote acceptance → payment → confirmation
- [ ] Status updates visible in conversation and database
- [ ] Error handling for payment failures

### Block 5: Claims Intelligence
- [ ] Historical claims analysis integrated
- [ ] Recommendations with supporting rationale
- [ ] Evidence-based product tier suggestions

---

## 🤝 Support & Contact

**Mentor**:
- Joffrey Lemery — Head of AI, Ancileo

**Getting Help**:
- Technical questions: Ask during mentor sessions
- MCP integration: Reference `https://modelcontextprotocol.io/`
- Payment stack: See `Payments/README.md` for troubleshooting
