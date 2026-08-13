# Interview with Arthur Severin, founder of Evo-ai

*Transcript of a conversation. June 2026. Prepared as material for an industry Telegram channel about AI adoption in business; never published in the end. The file is kept in the project for internal use — it may come in handy for PR, clients and hiring.*

---

**— Arthur, let's start at the beginning. Before Evo-ai you worked at a big company, on an ML team. Why did you leave?**

Yes, I spent several years on the ML team of a large player — a bank, big tech, it doesn't matter what you call it. Strong team, good resources, interesting models. But at some point I realised that we were rolling out AI for the hype and for a tick in a box, not for a result. Somebody builds a beautiful demo, it gets shown to the board, everyone applauds — and in production it falls apart. Nobody asks afterwards how it is doing three months later under real load. And that was eating away at me.

**— So the problem wasn't the technology?**

The technology was actually excellent. The problem was the attitude. AI was rolled out for presentations to the board, and in production it fell apart. I was trained to build models, and it turned out that the main skill is getting a model to the state where it closes somebody's real task every day and doesn't crash. Almost nobody paid attention to that. Everyone wanted to launch something new, nobody wanted to finish the old thing.

**— And that's when you decided to start a studio?**

I carried the thought around for six months before I committed. I wrote down what annoyed me and how it ought to be done differently. Then I understood: either I build a company that rolls out AI that actually works in production, or I forget about it and go on working "for the demo". I chose to build. That's how Evo-ai came about in 2021.

**— Why "Evo-ai" exactly? What's in the name?**

There are two things there, and both matter to me. The first is "evo", evolution. I don't believe in AI you roll out once and forget. The business changes, the data changes, customer questions change — and the solution has to change with them, to learn, to evolve. We build AI that evolves along with the business. The second thing is "ai" and the idea of connection itself. Our symbol is two nodes joined by an arc: on one side the business task, on the other the model. We connect business and AI. We don't bring a box saying "here's your neural network, go figure it out" — we connect a specific task with a specific solution. Hence our line: "we connect business and AI".

**— Do you have a stronger tagline than that one?**

The main one is "AI that works in production, not in a demo". It may sound dry, engineering. But it's honest. I'd rather say it dry and to the point than beautifully and emptily. In general we try to work without hype and without a "magic button". AI is a tool with limits, and those limits should be said out loud, not hidden behind a nice interface.

**— Who are your clients? Who comes to you?**

The ones who come have a specific task and are tired of beautiful promises. Our flagship product is an AI support assistant: an LLM plus RAG over the company's knowledge base, which prompts the operators and closes part of the requests itself. Right now our main rollout is the project for Hermes — that's nationwide logistics, 3PL, warehousing and freight. We're building them a support assistant over their policies, tariffs and shipment statuses, and doing the integration with their helpdesk. Go-live in production is by the autumn. That's what real work looks like to me: not a slide, but a system that live operators will sit down at tomorrow.

**— And before Hermes, had you actually finished anything?**

Yes, we have project Atlant behind us — a manufacturing group. We rolled out an AI assistant and a document processor for them. And that's where the thing I'm proudest of is — the numbers. Handling time dropped by 38 percent. The first line started closing 27 percent more requests without escalating upwards. The assistant's answer accuracy is 94 percent on the acceptance set. The rollout paid for itself in seven months. That's what I can bring to a client and say: look, this isn't a promise, this already happened. A demo doesn't work like that — a demo always shows the perfect picture. Atlant shows how it lives in reality.

**— What do you refuse to do on principle?**

I have my own list, like anyone who has been burned. We don't roll out AI for the hype — if the task sounds like "we need a neural network too, the competitors have one", we don't take it. We don't take on work without clear success metrics — if we can't agree in advance on the number that tells us it worked, there's no project. We don't promise a "magic button". And we don't ship a demo that won't survive production — that's probably the main taboo. And we don't chase project count for the sake of the count: better fewer, but carry each one to a result.

**— But that limits growth.**

It does. So be it. I don't want to grow the number of projects for the sake of the number. I want every project of ours to be one where the client can name a specific figure — this is how much better it got. If we take ten projects and don't get a single one to production, we're worthless. Better to take fewer and really close them.

**— What do you run on technically? Whose model, whose infrastructure?**

We have our own proven RAG engine, that's our core. Inference — that is, the model computation itself — we re-picked recently, we compared vendors and settled on one main one, with a backup in case of outages. I won't go into the details — that's engineering kitchen. What matters is something else: we're not fanatically tied to a single supplier, and we always look at the cost per request and at what we actually need for the client's task. The technology is secondary. The task comes first.

**— What are the plans for the future?**

The nearest one is getting Hermes to go-live in production, with everything working as it should. After that — there are more companies in the funnel that we're talking to. But I don't want to frame the plan as "open twenty projects by such-and-such a year". My plan is different: that we accumulate cases like Atlant — with honest numbers we're not embarrassed to show. If in three years I can show ten cases like that, rather than a hundred empty ones, then it worked.

**— What would you say to someone thinking of going into AI delivery?**

Don't go into AI if you love the technology. Go into it if you want to solve the client's task. I'm serious. Technology is beautiful, it's easy to fall in love with it and spend six months polishing a model nobody needs. And the client needs a result. Anyone can put a demo together — these days that's a couple of evenings' work. Making it survive in production takes engineering and honesty about the limits. That's what you should go into it for. Otherwise you'll build a pretty toy and shut down.

---

*End of transcript.*
