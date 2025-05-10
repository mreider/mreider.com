---
title: "Why AI won't take control"
description: "Co-Pilot vs. Autopilot in high-stakes environments"
author: "Matt Reider"
date: "2025-05-10"
image: "/images/matt/copilot.jpg"
---

AI went from a niche tech topic to a mainstream obsession in just the last 24 months. Unlike other hyped technologies that promised revolutions without delivering, AI is actually useful right away. During my nightly dog walks, I listen to tech podcasts to keep up with what's happening. The Cloudcast and NYT's Hard Fork have both pivoted heavily toward AI (from blockchain, which proved largely useless), now dedicating most episodes to AI tools and trends.

These podcasts aren't just discussing what AI can do today. They're hyping what it might do tomorrow. Cloudcast (a technical podcast that [recently focused on MCP servers and Agentic infrastructure](https://www.thecloudcast.net/2025/04/the-intersection-of-ai-and-apis.html) dives into systems that supposedly talk to each other to handle complex tasks. Hard Fork constantly discusses AGI (Artificial General Intelligence) as if it's inevitable. Cohost Kevin Roose [even announced this week he's writing a book about AGI](https://bsky.app/profile/kevinroose.com/post/3lne4qlnylc2d). [They've interviewed Sam Altman](https://www.nytimes.com/2023/11/20/podcasts/mayhem-at-openai-our-interview-with-sam-altman.html), [Dario Amodei](https://www.nytimes.com/2025/02/28/podcasts/hardfork-anthropic-dario-amodei.html) and other AI leaders as if human-level machine intelligence is a foregone conclusion. This hype gets amplified when figures like [Microsoft's CEO, Satya Nadella, claim that "Agentic AI" is going to replace all of SaaS software](https://www.youtube.com/watch?v=quXuKnGnOMs).

I don't buy it 💩

Last year I listened to [an episode of #shifthappens where Martin Eekels](https://www.youtube.com/watch?v=csY-PH0CEHk) described what I found to be a more realistic future. In my view, he gets it right when he suggested that AI works best as "a copilot to human capabilities rather than a replacement." What's important is that these limitations are NOT technical. They're completely about risk.

Eekels is not saying autonomous AI won't be a reality. It definitely will be. He's just arguing that it will be limited to low-risk scenarios. Sure, we'll see LLMs doing more than just generating creative content or suggesting next steps. We'll see them both searching for vacation spots, reserving refundable tickets, cars, and hotel rooms. But the emphasis here is on refundable. When the stakes are low, letting AI take the wheel is no problem. 

For anything involving significant risk or consequence, the autopilot model breaks down in predictable ways. And the exciting picture of our future, described by podcasters, tech bloggers, CEOs, and venture capitalists breaks down with it.

## The Automation Bargain

I was thinking about these tradeoffs last week. It's what inspired me to write this post. I was building a tool that compares message brokers (SQS, RabbitMQ, Kafka) with different instrumentations across multiple cloud platforms. Using [Anthropic's Sonnet LLM](https://www.anthropic.com/claude/sonnet), I completed the whole thing in about a week despite not being an engineer. Without AI, it would have been a year-long side project.

My project was strictly a prototype with zero real-world risk. No customer data was involved, no financial transactions processed, and no regulatory compliance required. It was a controlled experiment where failure had no consequences. I happily clicked the "Automated Approval" button in my VSCode plugin, [Cline](https://cline.bot/), and let Anthropic handle everything from building code to pushing it to my Kubernetes cluster.

The prototype example shows exactly why AI excels in certain environments. But letting an AI bot make changes to production software carries far too many legal, financial, reputational, and human risks. This creates the co-pilot versus autopilot distinction: AI excels as a co-pilot, and is also good as an auto-pilot, but only in low-risk contexts. I simply can't imagine walking away from it and letting it commit to git, approve its own pull requests based on passing tests, and deploy to prod. No fucking way.

## The 95/5 Divide: A Real-World Example

At a previous startup, I was the PM for a team of engineers building an automated identity verification system. Our challenge was delivering instant results in an environment where mistakes could directly harm people's lives.

Our engineering team built an AI neural network to evaluate probability matches between public records and user profiles. For 95% of cases, it performed adequately. Though not superior to humans, it was instantaneous, which met the business requirements for rapid turnaround and made our customers happy.

For the remaining 5% of cases, the system failed. Despite two years of intense effort under an over-ambitious CEO, we never reduced that error rate below 5%. Years later, according to friends that still work there, they still can't.

The 95/5 split wasn't a technical limitation. It was a risk management reality. The AI could make decisions autonomously if we let it. But the consequences of being wrong on that 5% were simply too severe to allow automation without human oversight. This is why "agentic AI" remains a pipe dream for any domain involving significant risk. The 5% barrier isn't about capability but about accountability.

And now I'm going to wade into political territory. Sorry. There's no avoiding it.

Two scenarios eliminate the 5% verification risk. In a surveillance state with perfect data collection, AI verification would be flawless but unnecessary, as public records would already link directly to individual profiles. However, this would enable concerning AI applications in other areas, operating with minimal risk due to the absence of privacy protections.

Similarly, in a monopolistic economy, verification risks disappear because customers cannot leave when software makes critical errors. Both scenarios likely exist under authoritarian regimes and unfortunately represent the ambitions of certain powerful individuals who, like Voldemort, I prefer not to mention by name.

## Back to business

Returning to reality, in today's democratic societies, AI will remain a co-pilot rather than an autopilot for the foreseeable future.

Perhaps AI autopilots and agentic AI will follow the same path as putting mortgages on the blockchain - something that never materializes despite countless blog posts, podcasts, books, and keynote presentations promising a future where we simply relax while technology handles everything.