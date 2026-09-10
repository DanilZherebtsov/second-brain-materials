# Second Brain workshop prompts (AI studio example)

These are the commands we type into Claude Cowork during the workshop, in order. The numbers match the ones in the script: the host calls out a prompt number — you copy it from here. Names like Hermes or Orbita come from the worked example; use your own in your own project.

*This file is generated automatically from the workshop script — it always matches it.*

---

### 1. Block 1 · First message to the constructor (who I am and what I do)
```
I'm a project manager at Evo-ai. I'm building myself an assistant to help me do my job: I run AI implementation projects (clients, vendors, the team, contracts, budgets, risks, decisions). [Add everything you do here; you can attach your job description too.] Build me a project structure for this.
```

### 2. Block 3 · Process the documents we just loaded
```
Our first task will be getting our flagship project Hermes (an AI support assistant for a logistics company) all the way to production launch. I've loaded in my working folders with materials, all jumbled up (brand, the contract, candidate resumes, the solutions catalogue, vendor quotes, the budget, decks, pilot feedback). Go through all of these documents and sort them out.
```

### 3. Demo 1 · Analysing the pilot feedback
```
Open the feedback on the Hermes AI assistant pilot — I collected it all into one file.

Find that file and produce an analytical report on the feedback:

1. Split every complaint and request into categories (for example: answer accuracy, speed/latency, tone and wording, topic coverage, integration/bugs, prompt UX, trust and escalation).
2. For each category — how many times it comes up, one or two specific quotes, and what it means for us before we go to production.
3. Call out separately what people say that's positive — those are our strengths, we need to keep them.

Save the result as Pilot feedback analysis in docx format.

Before you start, ask me one or two clarifying questions if anything is unclear.
```

### 4. Demo 1 · Iteration: what to fix before production
```
Good. Now add a section to this report called "Must-fix before production launch" — based on the comments where people criticise specific technical parameters (latency at peak hours, answers with no reference to a policy, confusion over tariffs, no escalation for complex cases). 5-7 items; for each one, what exactly to do and how to verify it's fixed.
```

### 5. Demo 1 · Excel: vendor comparison
```
Open the quotes from the inference vendors (the Excel with prices and terms).

The prices and terms are in all different formats (dollars/euros, per 1,000 requests / per 1M tokens / per GPU-hour / per month, different minimum orders, different payment terms). Normalise them to a single format:
— all prices in $ per 1,000 requests (convert euros at 1.08 $/€; assumption: an average request ≈ 1,500 tokens);
— a "Minimum order" column (in plain language);
— an "SLA" column: the percentage as a number;
— a "Postpay available" column: yes/no/partial.

Save it as a new file called Vendor_comparison_2026-06.xlsx.

At the end — a short written conclusion: which vendor is the best deal all things considered (bear in mind that VectoDB is about a vector database, not inference, so don't compare it directly).
```

### 6. Demo 1 · Remember the vendor decision
```
Remember this: based on the inference vendor comparison, we're going with ModelAPI. We keep TokenFlow as a backup for outages and for when we need top-tier models.
```

### 7. Demo 2 · Reviewing the Hermes contract
```
Open the draft development and implementation contract with Hermes.

Give me a short review:
1. Key financial terms (value, payment schedule, advance) — write out the specific numbers.
2. Termination terms — who can walk away and how, what they lose, what happens to the advance and to the work done so far.
3. Penalties, fines and late fees — how much and for what.
4. Rights to the deliverables and liability — what a lawyer would flag.
5. A list of questions to put to the client or our lawyer before signing.

Save it as Hermes_contract_review.md.

IMPORTANT: for every point, give me the clause number in the original contract so I can check it.
```

### 8. Demo 2 · What should we record in the wiki?
```
Is there anything here important and long-lived enough to record in wiki/? If so, suggest what's worth remembering.
```

### 9. Demo 2 · Email to the counterparty
```
Draft an email to the client with our comments on the contract. For every critical clause, give its current wording, our preferred wording, and the rationale for the change we're asking for. The document should be ready to send to this client as-is. Save it in MS Word format.
```

### 10. Demo 3 · Research: the AI support assistant market
```
Before you start — check the knowledge base, we may already have something on the AI assistant market. If we do, factor it in. If not, carry on.

Find fresh data online (2025-2026) on the market for AI customer support assistants:
— the size and growth of the AI market in customer service;
— the typical impact of an implementation (reduction in handling time, self-resolution rate);
— benchmarks for cost per request / support unit economics;
— successful cases of LLM assistants deployed in support.

Save the result as AI_support_market_research.md, with a source link for every fact.

When you're done — give me a short summary of the key figures (5-7 of them) and tell me whether it's worth recording them in the wiki as our market reference.
```

### 11. Demo 3 · What it means for the project
```
Given this analysis, what does it change for our Hermes project? Does it affect our proposal at all, or the success metrics we're promising the client? If you need to, go look at the source documents you haven't processed yet.
```

### 12. Demo 3 · New deck outline
```
Read:
— the current (weak) version of the Hermes deck — v1;
— the project budget (Excel);
— our pilot feedback analysis;
— our research on the AI support market.

Build a new deck outline for the kick-off meeting, 10-12 slides. On each slide:
— a headline;
— 3-4 key points;
— what specifically to show (a number, a chart, a quote).

Base it on the real data in those files, don't make anything up. If a slide is short on data — mark it "[data needed: ...]".

Save it as Hermes_presentation_v2_outline.pptx.
```

### 13. Block 8 · Bulk-processing 20 resumes
```
The project has a folder with 20 PDF applications for the ML/LLM engineer role on project Hermes, plus a file with the candidate requirements.

Do this:

1. Read all 20 resumes one by one. For each, extract into a normalised form: full name, age, grade (senior/middle/junior/intern), years of ML/LLM experience, most recent employer, whether they have a production LLM/RAG project (yes/no), core stack, English (reading / conversational / fluent), timezone and overlap with the team (CET), willingness to work the sprint rhythm and be on call.

2. Save the table as output/drafts/Candidate_screening_summary.xlsx. The table should have 20 rows, one per candidate.

3. Score each one from 1 to 10 on fit against the requirements in the role file. Put the score in its own column, and a one-line rationale in the column next to it.

4. Sort by score. Highlight the top 5 with a fill colour.

5. At the end — a short written comment: which of the top 5 to invite to the technical interview first, and why.
```

### 14. Block 9 · Create the finance role
```
I've put a folder with our project economics standard into the project (project-standards). Create a finance role and process these documents — let them become its reference knowledge.
```

### 15. Block 9 · Question for the finance lead: the norms
```
We're working in the role of the finance lead. What's our target gross margin on a project, and the minimum client prepayment at the start? And does Hermes fit inside those bounds, given the data already in the project?
```

### 16. Block 9 · Task for the finance lead: the project's financial profile
```
Work out the financial profile of project Hermes: gross margin, cost structure and project EBITDA. Base it on our norms (payroll share, infrastructure/inference, reserve, target margin) and factor in the legal findings (the 12-month free-fixes warranty as a hidden cost, the late-delivery penalty). Take the contract value and the budget from the project.

The output — a short .docx called "Hermes project financial profile" in output/drafts/, and record the conclusion in the project's knowledge base.
```

### 17. Block 10 · Claude in Chrome: scouting Orbita
```
Open the Orbita company website and the public sources about them (news, careers pages, social profiles). Put together a short dossier:
— what the company does, its scale (revenue/headcount, if it's in the public data);
— what products/business lines they have, any mentions of IT and AI;
— their tech stack and any job openings related to development/data/AI;
— recent news from the last 3-6 months (launches, deals, problems);
— who makes the IT decisions (CTO/CIO/head of digital), if it's findable in open sources.

Give me a short summary as text. I'll copy it into the project afterwards.
```

### 18. Block 11 · Scheduled task: competitor monitoring
```
Using Claude in Chrome, open three competing AI support assistant sites:
1. https://www.intercom.com/fin (Intercom Fin)
2. https://www.ada.cx/pricing (Ada)
3. https://autofaq.ai/ (AutoFAQ)

For each one:
— record the current plans/prices (as stated on the site) and the pricing model (per request, per seat, per resolution, etc.);
— check which key features and integrations they advertise, and whether there are new announcements/promotions;
— compare against what was recorded yesterday (if yesterday's digest file exists in output/monitoring/).

Create a digest at output/monitoring/Digest_YYYY-MM-DD.md (use today's date), containing:
— a "price/pricing model + key features" table for today across the three competitors;
— a list of changes versus yesterday;
— an "urgent, take a look" flag if anyone changed their pricing model or shipped a major feature.

If there are material changes — append a short summary to output/monitoring/summary.md with the date. If nothing changed — append nothing.

IMPORTANT: don't ask permission to move between sites — permission is only needed if you're about to log in or click "buy".
```

### 19. Block 12 · Onboarding pack for the new PM
```
I'm handing project Hermes to a new project manager. Put together an onboarding pack for them — only what they need for their zone: what stage the project is at, what decisions have been made (vendor, approach), what risks we found in the contract, what the project economics look like, what's currently open and needs a decision. Format it as a document they'll load into their own project as context. Don't tell them about all my other work — only their part, on Hermes.
```

### 20. Block 12 · Joining the project as the new hire
```
Process this onboarding material — I'm the new project manager on project Hermes at the Evo-ai studio, and I'm starting today. Turn it into my working knowledge and tell me briefly: what stage we're at, what decisions have already been made, what's on my plate. I've put the file in input.
```

### 21. Block 13 · Landing page: hunting for pearls
```
We want a one-page landing site for our flagship AI support assistant (an Evo-ai studio product, first deployment — project Hermes). The goal of the page: a wait-list of early/pilot clients, enquiries from companies that need AI, and proof to investors that the product is real.

FIRST THING — don't write a single line of code. Start by going through the whole project: raw/, wiki/, output/. Find everything that will make this landing page real rather than generic: the founder's story, the brand's values and manifesto, real client testimonials/feedback, the solutions catalogue, the brand colours, the logo, any visuals, diagrams, screenshots, results charts. Use files in any format — text, documents, spreadsheets, decks, images, logos.

Once you've found them — give me a list of the "pearls": what you found, which file it's in, and one line on why it's useful for the landing page. I want to see that list BEFORE you start building the site.

Wait for me to say "carry on" before you write any code.
```

### 22. Block 13 · Landing page: build the page
```
Great, go build it. The visuals from the deck — pull them out and use the ones that genuinely make the page stronger (not all of them).

When you're done — open the file yourself, look at how it turned out, and if you see anything obviously off, fix it before you show me.
```
