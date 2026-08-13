<!--
SOURCE (.md) → builds into Шпаргалка_Cowork_en.docx. Handed to participants AFTER the workshop.
English version of Шпаргалка_Cowork.md. The former "First week checklist" is merged in (section "First week plan").
Check against workshop-coffee.md when the script changes. Build: python3 раздатки/build-docx.py раздатки/second-brain-materials/Шпаргалка_Cowork_en.md раздатки/second-brain-materials/Шпаргалка_Cowork_en.docx
-->
# Claude Cowork Cheat Sheet

Your post-workshop reference: how to frame tasks, which commands work, what not to do — plus a plan for your first week.

---

## How to get a project on the rails — checklist

1. **Download the constructor.** Repository <https://github.com/DanilZherebtsov/knowledge-base-constructor-en> → green **Code → Download ZIP** button → unzip.
2. **Put it on your disk.** Place the `knowledge-base-constructor-en-main` folder wherever you'll run the project (your desktop, for example); it helps to rename your copy after the project itself — `<project>-second-brain`.
3. **Create the project in Cowork.** Claude Desktop → **Cowork** tab → **Projects** → **+** → **Use an existing folder** → pick that folder.
4. **Go through the constructor's guide.** In your first message, tell it **who you are and what you do** (you can attach your job description). Answer a couple of interview questions — the constructor will build the structure around you (`CLAUDE.md`, `raw/`, `wiki/`, `output/`, `input/`) and clear away the scaffolding.
5. **Add your documents (if you have any).** Drop working files into the project's **`input/`** folder and ask: "sort through these documents and put them in order" — Cowork will file the raw material into `raw/` and synthesize the knowledge into `wiki/`.
6. **From there — work in chats** (just like in the workshop): **1 chat = 1 task**; after a task — "remember this" / "record this in `wiki/`"; separate roles (lawyer, finance, …) once you've built up enough work in that area; once a week — "run maintenance".

---

## The formula for a good task

**CONTEXT → GOAL → CONSTRAINTS → OUTPUT FORMAT**

- **Bad:** "Sort through the contracts folder."
- **Good:** "The `Contracts/2025` folder has contract PDFs. Build an Excel file: counterparty, tax ID, amount, term. If you can't find a field, leave it blank and flag it in a 'check' column. Save as `register.xlsx`, don't touch the originals."

---

## Techniques that always work

- **"Before you start, ask me 1–2 clarifying questions"** — saves you from a junk result.
- **"Cite the source / clause number for every fact"** — cures hallucinations: when Claude has to point at a specific spot in a document, it doesn't invent.
- **"Here's a sample of the result I want, in this format"** — gets the work done to your template.
- **"Check the knowledge base (`wiki/`) first, then do the work"** — Claude builds on what's already there instead of starting from scratch.
- **"Remember this: …"** — turns a decision or fact into a knowledge base entry (`wiki/`) with a date and a source. That's how the base grows as you work.
- **"Is there anything here worth recording in `wiki/`? Suggest what and where"** — ask this after a big task; the base fills itself in.
- **A large batch of files:** "process the first 10 and show me the result" → then "keep going with the same rules." And at the end: "remember this processing template" — the next batch runs off a single prompt.

---

## Useful commands (triggers)

- **How to start a new project:** see the "How to get a project on the rails" checklist above. In short: download the constructor from https://github.com/DanilZherebtsov/knowledge-base-constructor-en, put the folder on your disk, create a project on it in Claude Cowork, and in your first message tell it who you are and what you do. The constructor walks you through the stages and builds the structure; put your documents (if any) in the `input/` folder.
- **Set up a role as a team member:** "Create a lawyer (finance, marketing) role for our project." Call it up in a new chat: "Work as the lawyer."
- **Train a role further:** "Work as the lawyer — our corporate standard has been updated, process it and turn it into your knowledge."
- **Weekly maintenance:** "Run maintenance" — Claude checks the knowledge base and pulls in improvements without breaking your entries.
- **A scheduled task:** Scheduled Tasks → New → prompt + schedule (for example, "every weekday at 09:00").

---

## Working modes

- **Ask before acting** — asks permission at every step. **By default, this is the only one we use.** It gives you time to stop both a mistake and a hidden malicious instruction coming from someone else's file or website.
- **Act without asking** — works on its own. Turn it on only when a task is routine and already proven (a scheduled task you've debugged, for example). Claude always confirms file deletion regardless.

---

## Memory: 5 levels (+ STATE)

- **Global instructions** — your personal preferences across all projects (Settings → Cowork). Set it once, it works everywhere.
- **Project instructions (`CLAUDE.md`)** — this project's rules, loaded at the start of every chat. Built by the constructor.
- **Chat context** — remembered until the end of the conversation; close it and it's gone.
- **Claude memory** — project context across chats; helpful, but gets overwritten over time.
- **The `wiki/` folder** — synthesized knowledge, permanently (decisions, facts, counterparties) with dates and sources; available in any chat.
- **`STATE.md`** — operations: what's in progress, what's next, what's awaiting a decision (not memory about the world).

The rule: **one business process = one project.** Don't cram everything into Instructions — rules go there, facts go in `wiki/`. When a chat gets long and Claude starts fumbling — ask for a summary in a file, start a new chat, feed it the summary.

---

## When to start a new chat

Don't run everything in one chat. Claude has a limited "attention window" (context): the longer the chat, the more old material it's holding in its head — it starts getting confused and fumbling.

**Start a new chat when:**

- the task or topic changes — a new chat starts with a clean desk;
- the chat has gotten very long and Claude has slowed down or is getting confused;
- you need a separate role (lawyer, finance) — it gets its own chat.

**Why this is better:** the project's shared memory (`wiki/` and the project Instructions) is visible in every chat, so splitting things up does NOT lose context — but each chat stays short and precise. If a chat has already sprawled: "write a short summary to a file", start a new chat, and feed it that summary.

---

## Security — 4 rules

- **One folder — one project**, don't hand over all of `Documents`/`Desktop`.
- **Only on an explicit "yes":** payments, sending emails, permanent deletion, passing files to third parties.
- **Other people's files and websites** (from clients, counterparties) — only in **Ask before acting** mode (protection against prompt injection).
- **Don't put** the following into Cowork without a corporate plan: clients' personal data, NDA documents, third parties' medical or banking data (personal data law, 152-FZ).

---

## When something goes wrong

- **Claude is stuck** → Stop → "Tell me briefly what you did. I'll say how to continue."
- **It produced the wrong thing** → don't start over: "This doesn't work because X. Redo Y."
- **It looks made up** → "Re-check every number against the originals, and flag what you couldn't find."
- **It can't find a file** → check that the folder is connected; give the exact path if needed.
- **Claude's answer is unclear** → ask it in plain language =)

---

## How to look at your project files

You don't need a code editor — your OS's built-in tools are enough:

- **The project folder** — open it in **Finder** (Mac) / **File Explorer** (Windows), keep it next to Claude and watch `raw/`, `wiki/`, `output/` grow.
- **Viewing `.md`** — on Mac, select the file and hit **space** (Quick Look); on Windows, turn on the preview pane (View → Preview pane).
- **Results** — `.docx/.xlsx/.pptx` open in Word/Excel/PowerPoint; `.html` — double-click to open in your browser.

---

## First week plan

The goal for the week isn't to learn every feature — it's to make Cowork a habit. Small wins beat big experiments.

**Days 1–2. Setup**

- Claude Desktop installed, Pro subscription active, VPN working.
- Create a separate folder on your computer for work projects.

**Days 2–3. Your first project**

- Get a project on the rails using the checklist above (download the constructor → put it on your disk → create the project in Cowork → go through the guide → add documents to `input/`).
- Pick ONE real, recurring task (sorting client email, a weekly report, a document register).

**Days 3–7. Five simple tasks**

Warm-ups, 10–15 minutes each — don't try to solve your biggest problem right away:

- sort one folder of documents into a structured register;
- pull the key terms out of one long contract or spec;
- compare 3–5 proposals in a single table;
- rewrite a draft email or document into a final version;
- build a summary of reviews/feedback by category.

**Habits for the week**

- Every day — **Ask before acting** mode only.
- Once a day — the **Usage** tab, to keep an eye on your limits.
- A prompt that worked — **save it** (your personal library). One that didn't — **write down the problem**.
- After the 3rd task — try setting up a specialized role chat (lawyer / finance / researcher).
- Once a week — "run maintenance".

**What NOT to do in your first week**

- Do NOT switch to Act without asking.
- Do NOT give access to entire personal folders (`Documents`, `Desktop`).
- Do NOT upload clients' personal data, NDAs, or third parties' medical/financial data.
- Do NOT automate critical processes for the first two weeks — build up your intuition first.

**For our next meeting**

- One example where Cowork helped a lot — what it did, how much time it saved.
- One example where Cowork failed — what happened, how you fixed it. **This is the most valuable one.**
- One prompt from your library that you're proud of — we'll share them with each other.
