# Ancileo × MSIG — Conversational Insurance Challenge

## 🎯 Challenge Summary

**Your Goal**: Create a breakthrough conversational AI that transforms insurance from a tedious form-filling process into an engaging, intelligent dialogue.

**The Innovation Opportunity**: We've provided a foundation with 5 feature blocks, but **your creativity is unlimited**. Think beyond traditional insurance flows—imagine how AI can make insurance truly conversational, personalized, and delightful.

> **💡 INNOVATION FIRST**: While we provide guidance through feature blocks, we encourage you to:
> - **Rethink the entire user journey** — What if insurance was as engaging as chatting with a knowledgeable friend?
> - **Experiment with novel approaches** — Surprise us with creative solutions we haven't considered
> - **Focus on the B2C experience** — Make it so good that customers prefer your bot over human agents
> - **Push the boundaries** — Use the provided data and tools as a springboard, not a constraint

> **📖 CONTEXT**: Read the **Next-Generation Conversational Travel Insurance Distribution Hackathon.pdf** for background, but don't let it limit your imagination. The best solutions often come from questioning assumptions and exploring uncharted territory.

> **API KEY**: To access the Ancileo × MSIG hackathon endpoints, use the event API key below.

 API KEY -> https://pwpush.com/p/y9hg-pkgeg-bzeik/r

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

## 🎯 Innovation Framework — Your Creative Playground

We've outlined **5 feature blocks** as inspiration, but remember: **these are starting points, not requirements**. The most innovative solutions often emerge when you:

- **Add entirely new capabilities** we haven't imagined
- **Rethink the conversation flow** from first principles
- **Create delightful micro-interactions** that surprise and engage

### The Foundation Blocks (Use as Inspiration)

```
┌─────────────────────────────────────────────────────────────────┐
│  🧠 Block 1: Policy Intelligence                               │
│  ↓ Your creative approach to understanding insurance documents │
├─────────────────────────────────────────────────────────────────┤
│  💬 Block 2: Conversational Magic                              │
│  ↓ How will you make insurance chat feel natural and helpful? │
├─────────────────────────────────────────────────────────────────┤
│  📄 Block 3: Document Intelligence                             │
│  ↓ What innovative ways can you extract and use trip data?    │
├─────────────────────────────────────────────────────────────────┤
│  💳 Block 4: Seamless Commerce                                 │
│  ↓ How do you make purchasing feel effortless and secure?     │
├─────────────────────────────────────────────────────────────────┤
│  🎯 Block 5: Predictive Intelligence                           │
│  ↓ How can you use claims data to create breakthrough insights?│
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
├── Hackathon_Documentation/           ← API & Additional Resources
│   ├── Travel Insurance API Documentation.pdf  ← API endpoints & integration guide
│   └── Scoot_SG_destination_list.xlsx         ← Destination data for quotes
│
├── Claims_Data_DB.pdf                ← Historical claims database for BONUS BLOCK
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

## 🏗️ Innovation Blocks — Inspiration & Guidance

> **🚀 Remember**: These are **inspiration blocks**, not rigid requirements. Feel free to combine, modify, or completely reimagine any of these approaches!

### 🧠 Block 1: Policy Intelligence — Your Approach to Understanding Documents

**💡 Innovation Opportunity**: How will you make sense of complex insurance documents? 

**Traditional Approach**: Convert PDFs into structured data using predefined taxonomies.

**🚀 Your Innovation Space**:
- **Beyond text extraction**: Could you use visual analysis to understand policy layouts?
- **Dynamic normalization**: What if your system learns new terminology on the fly?
- **Semantic understanding**: How might you capture the "spirit" of policies, not just the words?

**Where to start**: `Taxonomy/Taxonomy_Hackathon.json`

**The Challenge**:
- Insurance policies use different words for the same thing ("medical expenses" vs "healthcare costs")
- Limits are buried in paragraphs ("up to $50,000 per trip, with a sub-limit of $5,000 for dental")
- You need to compare apples-to-apples across 3+ products

**💡 One Possible Solution — Taxonomy Normalization** (but innovate beyond this!):

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


### 💬 Block 2: Conversational Magic — How Will You Make Insurance Chat Feel Natural?

**💡 Innovation Opportunity**: Transform insurance from boring forms into engaging conversations.

**Traditional Approach**: Answer questions with policy citations and comparisons.

**🚀 Your Innovation Space**:
- **Personality & Empathy**: What if your bot had a unique personality that users love?
- **Proactive Intelligence**: Could it anticipate questions before users ask them?
- **Emotional Intelligence**: How might it adapt to user stress, confusion, or excitement?
- **Multimodal Conversations**: What if users could share photos, voice messages, or documents naturally?
- **Learning & Memory**: Could it remember user preferences across sessions?

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

### 📄 Block 3: Document Intelligence — What Innovative Ways Can You Extract Trip Data?

**💡 Innovation Opportunity**: Replace tedious form-filling with intelligent document understanding.

**Traditional Approach**: Upload documents → extract data → generate quotes.

**🚀 Your Innovation Space**:
- **Smart Document Understanding**: What if your system could read handwritten notes or messy itineraries?
- **Predictive Extraction**: Could it infer missing information from context?
- **Multi-format Intelligence**: How might it handle photos, screenshots, or voice recordings?
- **Real-time Validation**: What if it could spot inconsistencies and ask clarifying questions?
- **Contextual Recommendations**: Could it suggest additional coverage based on trip patterns?

**The Transformation**:
- ❌ **Old way**: Fill 15-30 form fields manually (20 minutes, 70% abandonment)
- ✅ **New way**: Upload flight booking PDF (2 minutes, instant quote)

**Document Types to Handle**:
- ✈️ Flight confirmations (dates, destinations, traveler names, ticket costs)
- 🏨 Hotel bookings (check-in/out dates, location, investment value)
- 📄 Itineraries (activities, destinations, timeline)
- 🛂 Visa applications (trip purpose, duration)


### 💳 Block 4: Seamless Commerce — How Do You Make Purchasing Feel Effortless?

**💡 Innovation Opportunity**: Transform payment from a friction point into a delightful experience.

**Traditional Approach**: Redirect to external payment pages, lose conversation context.

**🚀 Your Innovation Space**:
- **In-Chat Payments**: What if users never leave the conversation?
- **Trust & Security**: How might you build confidence through transparency?
- **Post-Purchase Experience**: How do you make policy delivery feel special?

**The Challenge**: MCP servers don't handle callbacks natively, but we've provided a **creative workaround** (though you're free to innovate beyond this!).

**🛠️ Our Suggested Approach — Callback Server Workaround** (Optional!):

> **Why This Workaround?**: MCP servers are designed for stateless tool calls, not persistent webhooks. Our callback server bridges this gap by:
> 1. **Receiving Stripe webhooks** when payments complete
> 2. **Updating a shared database** with payment status
> 3. **Allowing your MCP tools** to poll for status updates
> 
> **💡 But Remember**: This is just ONE approach! Feel free to innovate with:
> - **Direct API integrations** with payment providers
> - **Event-driven architectures** using message queues
> - **Real-time updates** via WebSockets or Server-Sent Events
> - **Blockchain-based payments** for transparency
> - **Any other creative solution** you can imagine!

**Where to start**: `Payments/` folder (but don't feel constrained by our approach!)

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

**Payment Flow Visualization**:

<img width="6206" height="2577" alt="Stripe_Callback_Workaround 41 jpg" src="https://github.com/user-attachments/assets/674f330e-aff2-4fff-9a40-882ded5dd613" />


**💡 Why This Architecture?**: MCP servers are stateless and can't receive webhooks directly. Our callback server bridges this gap, but feel free to innovate with your own approach!

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

### 🎯 Block 5: Predictive Intelligence — How Can You Use Claims Data to Create Breakthrough Insights?

**💡 Innovation Opportunity**: Transform historical data into predictive intelligence that revolutionizes insurance recommendations.

**🚀 FREE DATA FOR INNOVATION**: We're providing you with **real historical claims data** and This is your chance to:

- **Discover hidden patterns** in travel risks and claims
- **Build predictive models** that anticipate user needs
- **Create breakthrough insights** that traditional insurers miss
- **Develop novel recommendation engines** based on real-world data
- **Experiment with AI approaches** that could transform the industry

**💡 Innovation Questions to Explore**:
- What if you could **predict claim likelihood** before users even ask?
- How might you use **seasonal patterns** to suggest optimal coverage timing?
- Could you build **risk scoring** that's more accurate than traditional methods?
- What if you could **prevent claims** through proactive recommendations?
- How might you use **demographic insights** to personalize experiences?

**Example Innovation Scenario**:
```
User uploads: Flight to Japan (skiing trip)
Your AI analyzes: Historical claims for Japan ski trips
Discovers: 80% of medical claims exceed $30,000
Innovates: "Based on similar trips, we recommend the Silver plan 
           with $50,000 medical coverage (vs. Bronze at $20,000)
           Plus, here's why ski insurance add-ons matter..."
```

> **📊 YOUR INNOVATION PLAYGROUND**: The `Claims_Data_DB.pdf` contains historical claims data. Use it to build the most innovative B2C insurance agent possible!
> 
> **What's Inside**:
> - **Real claims patterns** by destination, activity, and demographics
> - **Actual claim amounts** for different scenarios
> - **Risk factors** and correlation data
> - **Seasonal trends** and coverage gaps
> - **Everything you need** to build breakthrough insights

---

## 🏆 Judging Criteria — Innovation First!

Your submission will be evaluated on:

### 🚀 Innovation & Creativity (30%)
- **Breakthrough thinking**: How did you reimagine the insurance experience?
- **Novel approaches**: What creative solutions did you develop?
- **Unexpected combinations**: How did you combine technologies or concepts in new ways?
- **Future vision**: How does your solution point toward the next generation of insurance?

### 💡 Technical Excellence (25%)
- **Smart implementation**: How well did you execute your innovative ideas?
- **MCP mastery**: Creative use of MCP capabilities beyond basic tool calls
- **Architecture innovation**: Novel system design and integration approaches
- **Code quality**: Clean, maintainable, and well-documented solutions

### 🎯 User Experience Innovation (20%)
- **Conversation design**: How did you make insurance chat feel natural and engaging?
- **Personalization**: What innovative ways did you customize the experience?
- **Emotional intelligence**: How did you handle user emotions and build trust?
- **Delight factors**: What surprising moments did you create?

### 🌟 Business Impact & Vision (15%)
- **Market transformation**: How could your approach change the insurance industry?
- **Scalability innovation**: What novel approaches to growth and expansion?
- **Revenue innovation**: Creative monetization or value creation ideas?
- **Industry understanding**: Deep insights into insurance challenges and opportunities

### ⚡ Feasibility & Execution (10%)
- **Realistic innovation**: Groundbreaking ideas that could actually work
- **Implementation path**: Clear roadmap from prototype to production
- **Error handling**: Robust solutions for real-world challenges
- **Edge case innovation**: Creative approaches to handling unusual situations

## ✅ Innovation Checklist — Your Creative Journey

> **🚀 Remember**: These are **inspiration checkpoints**, not rigid requirements. Feel free to innovate beyond any of these suggestions!

### 🧠 Policy Intelligence Innovation
- [ ] **Your unique approach** to understanding insurance documents
- [ ] **Creative normalization** that goes beyond traditional taxonomies
- [ ] **Innovative comparison methods** that reveal hidden insights
- [ ] **Documentation of your breakthroughs** and novel approaches

### 💬 Conversational Magic Innovation
- [ ] **Unique personality** that users love and remember
- [ ] **Innovative conversation flows** that feel natural and engaging
- [ ] **Creative citation methods** that build trust and understanding
- [ ] **Breakthrough interaction patterns** that surprise and delight

### 📄 Document Intelligence Innovation
- [ ] **Novel extraction approaches** that handle edge cases creatively
- [ ] **Innovative validation methods** that catch errors before they matter
- [ ] **Creative integration** with conversation flow
- [ ] **Breakthrough accuracy** through innovative techniques

### 💳 Commerce Innovation
- [ ] **Seamless payment experience** that feels magical
- [ ] **Creative trust-building** approaches
- [ ] **Innovative error handling** that turns problems into opportunities
- [ ] **Breakthrough post-purchase** experience design

### 🎯 Predictive Intelligence Innovation
- [ ] **Novel insights** from claims data that others missed
- [ ] **Creative recommendation engines** that feel personal and smart
- [ ] **Breakthrough predictive models** that anticipate user needs
- [ ] **Innovative data visualization** that makes complex insights clear

---

## 🤝 Support & Innovation Community

**Your Innovation Mentor**:
- Joffrey Lemery — Head of AI, Ancileo
- **Focus**: Helping you push boundaries and explore breakthrough ideas

**Getting Help & Inspiration**:
- **Innovation questions**: Ask during mentor sessions — we love creative thinking!
- **Technical exploration**: Reference `https://modelcontextprotocol.io/` for MCP capabilities
- **Payment innovation**: See `Payments/README.md` for our suggested approach (but innovate beyond it!)
- **Data exploration**: Dive deep into `Claims_Data_DB.pdf` — it's your innovation playground!
