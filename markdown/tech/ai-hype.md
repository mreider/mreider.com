---
title: "Why AI won't take control"
description: "Co-Pilot vs. Autopilot in high-stakes environments"
author: "Matt Reider"
date: "2025-05-10"
image: "/images/matt/copilot.jpg"
---

AI went from a niche tech topic to a mainstream obsession in just the last 24 months. Unlike other hyped technologies that promised future revolutions, AI delivers immediate value anyone can experience. People can jump onto ChatGPT and be dazzled by its ability to write a poem, draft an email, or provide information that previously required a Google search. This immediate, almost magical utility has transformed AI from industry jargon into a household term.

During my nightly dog walks, I listen to podcasts about AI and other tech trends. Unlike the blockchain hype cycle that I found off-putting, discussions about AI genuinely hold my attention. A recent Cloudcast episode on [MCP servers and Agentic AI](https://www.thecloudcast.net/2025/04/the-intersection-of-ai-and-apis.html) gave me insights into how AI infrastructure is evolving. I also enjoy The New York Times' Hard Fork interviews with leaders like [Sam Altman](https://www.nytimes.com/2023/11/20/podcasts/mayhem-at-openai-our-interview-with-sam-altman.html) and [Dario Amodei](https://www.nytimes.com/2025/02/28/podcasts/hardfork-anthropic-dario-amodei.html).

Similar to blockchain, though, I'm irritated by the hype surrounding AI's future. Almost every Hard Fork episode mentions AGI (Artificial General Intelligence) as if it's inevitable. Cohost Kevin Roose even [announced this week he's writing a book about it](https://bsky.app/profile/kevinroose.com/post/3lne4qlnylc2d). The speculation about autonomous AI capabilities gets amplified when figures like Microsoft CEO Satya Nadella [proclaim that Agentic AIs will replace traditional software across every industry](https://www.youtube.com/watch?v=quXuKnGnOMs).

I don't buy it 💩

Last year, I listened to [an episode of #shifthappens with Martin Eekels](https://www.youtube.com/watch?v=csY-PH0CEHk) who described what I think is a more realistic AI future. Eekels said that AI works best as "a copilot to human capabilities rather than a replacement." The key point is that AI's limitations aren't technical. They're about risk. 

It's not that autonomous or "agentic" AI won't happen. It absolutely will. It will go beyond ChatGPT's current ability to suggest vacation spots. It will take the next step and book refundable airline tickets, reserve cars, and secure hotel rooms by communicating with other AI systems across different organizations in an interoperable network. But in these scenarios of AI-to-AI interactions, the word "refundable" becomes crucial. When mistakes have minimal consequences, letting AI take control is no problem.

But for anything with serious consequences, both agentic and autopilot AI models fall apart. (While there are technical differences between networked AI systems and fully autonomous ones, they face the same risk limitations.) When real stakes are involved, the exciting future promised by podcasters, tech bloggers, CEOs, and VCs simply doesn't hold up.

## The Automation Bargain

I experienced these tradeoffs firsthand last week, which inspired this post. I built a tool comparing message brokers (SQS, RabbitMQ, Kafka) with various instrumentations across multiple cloud platforms. Using [Anthropic's Sonnet LLM](https://www.anthropic.com/claude/sonnet), I completed the entire project in about a week, despite not being an engineer. Without AI, it would have been a year-long side project.

My project was purely a prototype with zero real-world risk. It involved no customer data, processed no financial transactions, and required no regulatory compliance. In this controlled environment where failure had no consequences, I confidently clicked the "Automated Approval" button in my VSCode plugin, [Cline](https://cline.bot/), letting Anthropic handle everything from building code to pushing it to my Kubernetes cluster.

Comparing my throw-away prototype to an autonomous AI taking control of a production system reveals unacceptable legal, financial, reputational, and human risks. This is why the co-pilot versus autopilot distinction matters. While I happily let AI assist me, I cannot imagine giving it complete autonomy to commit to git, approve its own pull requests, and deploy to production. No fucking way.

## The 5% problem. A Real-World Example

At a previous startup, I led a team of engineers as PM for an automated identity verification system. Our challenge was delivering instant results without mistakes that could directly harm people's lives.

Our engineering team built an AI neural network to evaluate probability matches between public records and user profiles. The system performed as well as humans for 95% of cases while providing instantaneous results. This met our business requirements for rapid turnaround and made our customers happy.

For the remaining 5% of cases, the system was hit-or-miss. In AI terms, that 5% represented our confusion matrix, instances where the AI couldn't confidently determine the answer. We ensured human review for each of these cases. Despite two years of intense effort under an ambitious CEO, we never reduced that confusion rate below 5%. According to friends still working there years later, they still can't.

The 5% problem wasn't a technical limitation. It was a risk management reality. The AI could make decisions autonomously if we let it. But the consequences of being wrong on that 5% were simply too severe to allow automation without human oversight. This is why "agentic AI" remains a pipe dream for any domain involving significant risk. The 5% barrier isn't about capability but about accountability.

And now I'm going to wade into political territory. Sorry. There's no avoiding it.

Hypothetically, only two scenarios could eliminate our 5% verification problem. The first is a surveillance state with perfect data collection, where our public record verification would be flawless because records would already link directly to individuals. This would also make AI verification unnecessary.

The second scenario is a monopolistic or fully state-controlled economy where our AI's verification risks become irrelevant because customers would have nowhere else to go when the software made critical errors. 

Both these scenarios typically exist under authoritarian regimes and, unfortunately, represent the ambitions of certain powerful figures that appear in the news quite often these days, both within technology and politics, or both.

## Back to reality

AI will remain a co-pilot rather than an autopilot, at least in any moderately risky situation, for the foreseeable future. The real-world consequences of errors are simply too high for societies that have laws that protect their citizens (God help us there).

The "agentic AI revolution" that tech leaders promise will likely follow the same path as "mortgages on the blockchain." Endless hype that never materializes. Despite all the promises of a future where we can sit back while AI handles everything, I suspect we'll find that when it comes to meaningful work, humans will stay in the driver's seat while AI rides shotgun.
