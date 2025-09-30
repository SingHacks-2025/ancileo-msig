# Ancileo × MSIG — Conversational Insurance

> **Travel Insurance MCP** — Build an MCP-enabled assistant that turns travel-insurance conversations into understanding → comparison → quotation → purchase, topped with claims-backed recommendations.

---

## Challenge Summary

- **Goal:** Ship a working assistant that can **parse policies → answer with citations → quote from uploaded trip docs → purchase in-chat**.  
- **Build path:** Implement the **Feature Blocks (1→5)** in order. If time is tight, submit sequentially starting from **Block 1**.

---

## Problem → Outcome

### What is the current problem?
Travel insurance journeys are inefficient: users fill forms, read long PDFs, compare complex benefits, and can’t get precise answers in real time—turning a decision that should take minutes into 10–30 minutes.

### What is the expected final product?
A **MCP** enabled system that transforms AI assistants:
- **understands & normalizes** policy wording (with source anchors),
- **answers questions & compares plans** with clear tables and citations,
- **extracts trip details** from user documents to **generate quotes**, and
- **completes a purchase** in the same conversation. *Bonus:* **claims-informed recommendations** with a concise rationale.

### Who are the users?
AI developers, insurer tech teams, and end-customers purchasing through assistants powered by ChatGPT, Claude and more.

### Use Case
This solution enables AI assistants to become knowledgeable insurance advisors that
can instantly compare policies, explain coverage differences, and guide users through
purchase decisions. The business case involves transforming AI conversations into
effective distribution and customer service channels, while improving conversion rates
through reduced friction.

## Data & Resources

- **Policy Wordings:** 4–5 MSIG travel policy PDFs  
- **Normalization Taxonomy:** schema for apples-to-apples comparison  
- **Insurance Datasets:** traveler profiles & trip scenarios (JSON)  
- **Developer Resources:** Endpoints for **Quotation** & **Purchase** 

---

## Feature Blocks — Recommended Build Path (1 → 5)

> Treat these as **features** to implement sequentially. Ideal submissions cover **1–5**.

### ✅ Block 1 — Policy Intelligence & Normalization (with Source Anchors)
Parse policy PDFs → **standardized JSON** (benefits, limits, sub-limits, exclusions, deductibles, eligibility).  
Each field includes a **page/section anchor** to the original wording.

---

### ✅ Block 2 — Conversational QA & Comparison
A chat layer that **routes** queries and answers with **clean tables, plain-language rationales, and citations**.  
**Query types:** comparison · explanation · eligibility · scenario analysis.  
**MCP tools (suggested):** `compare_policies`, `faq_lookup`.

---

### ✅ Block 3 — Document Upload → Auto-Quote
Accept flight/hotel/itinerary docs or screenshots; **extract** travelers, dates, destinations, spend, activities → call **Ancileo Quotation** → return options in chat.

---

### ✅ Block 4 — In-Chat Purchase (Sandbox)
Convert an accepted quote into a **completed policy** in the same conversation.  
Show progress states, handle errors, and return a **confirmation** payload.

---

### ⭐ Block 5 — Claims-Backed Recommendations (Bonus)
Use historical claims patterns to **right-size coverage** (e.g., med-evac, destination risks) and **explain the why** in one sentence.

---

## Judging Criteria

**Technical Implementation (25%)**
- Quality of policy-wording processing and normalization  
- MCP protocol integration and functionality  
- Code architecture and documentation

**User Experience (20%)**
- Conversational interface design and natural language interaction  
- Clarity of policy comparisons and recommendations

**Innovation (20%)**
- Creative approaches to policy analysis and comparison  
- Novel use of MCP capabilities or hypothetical product generation

**Feasibility (20%)**
- Realistic path to production implementation  
- Scalability considerations for multiple insurers

**Business Impact (15%)**
- Potential for market transformation and revenue generation  
- Understanding of insurance industry dynamics

---

## Expected Prototype

**Format**
- Live demo of a working MCP system integrated with an AI assistant  
- Slides (.pptx) explaining architecture and business case

**Key elements to show**
- Policy-wording processing pipeline  
- Side-by-side comparison via conversation  
- Normalization taxonomy & data structure (how JSON maps to wording)  
- Full journey from **comparison → quotation → purchase**

**Requirements**
- **10-minute presentation**, including a **5-minute live demo**  
- Working prototype with **at least 3 processed policies**  
- Clear documentation of MCP implementation
