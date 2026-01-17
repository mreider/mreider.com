---
title: "Building Mastopub: Auto-Posting to Mastodon"
author: "Matt Reider"
date: "2025-01-17"
image: "/images/matt/mastopub.png"
mastodon: true
mastodon_thread: true
---

I'm excited about the [Forkiverse experiment](https://pjvogt.substack.com/p/the-fediverse-experiment).

If you haven't heard, the folks behind Hard Fork and Search Engine ([@kevin@theforkiverse.com](https://theforkiverse.com/@kevin), [@Casey@theforkiverse.com](https://theforkiverse.com/@Casey), and [@pj@theforkiverse.com](https://theforkiverse.com/@pj)) have launched their own Mastodon instance. The current internet is arguably the worst it's ever been, so instead of just complaining about it, they're building a small alternative. A bot-free mini-world.

It's not theoretical. These are tech journalists who've spent years covering social media, and now they're actually trying the decentralized alternative themselves.

It got me thinking. I have a Mastodon account, and I want to post there more often. But I also like writing on my blog. Now I can do both at the same time. We should all be contributing to the fediverse rather than algorithmic social networks. These platforms are arguably hurting our mental health, not to mention whatever progress we made towards the ideal of democracy, by encouraging content that makes us angry at one another, all for clicks.

I actually invested a ton of time during COVID building a social network like the fediverse called Peacenik (yes, idealistic name, I know). You can see me [promote this now-failed project here](https://www.youtube.com/watch?v=9fo8JNKIoJo&t=4s). That didn't work out.

Today I built [Mastopub](https://github.com/mreider/mastopub), a GitHub Action that automatically publishes my blog entries to Mastodon.

Add `mastodon: true` to a post's frontmatter, push to GitHub, and Mastopub handles the rest.

### How It Works

This blog runs on [Hugo](https://gohugo.io/), a static site generator. Each post is a Markdown file with YAML frontmatter at the top, where you set the title, date, author, and other metadata. I added two new fields:

```yaml
mastodon: true
mastodon_thread: true
```

![frontmatter example](/images/matt/frontmatter.png)

When I push changes to GitHub, a workflow runs that scans for posts with `mastodon: true`. If it finds one that hasn't been posted yet, it publishes it to my Mastodon account.

The `mastodon_thread` option breaks the entire article into a thread, chunking the text into 480-character toots. Images get uploaded too. It's like live-tweeting your own blog post, except automated.

A JSON file keeps track of what's already been posted, so you don't accidentally spam your followers with the same article every time you fix a typo.

### Proof It Works

My [Lost and Found](/life/lost-and-found/) story about Max's gym bag on the Vienna streetcar was one of the first posts to use Mastopub. You can see it on Mastodon [here](https://ieji.de/@mateo/115910965322919799).

If you're reading this on Mastodon right now, you're looking at more proof. This post was auto-published the same way. I wrote it, added the frontmatter flags, pushed to GitHub, and Mastopub did the rest.

### Why Bother?

I could just copy and paste. But I'm lazy in that programmer way where I'll spend a weekend automating something to save five minutes.

This whole approach of publishing on your own site and syndicating elsewhere has a name: the [IndieWeb](https://indieweb.org/). It's different from the fediverse, but they share a spirit. The IndieWeb is a throwback to when everyone had their own little website. My site is part of the [IndieWeb webring](https://indieweb.org/webring), which is why you see those links at the bottom of the page. It'd be great if the Forkiverse crew talked about that.

They did talk about the throwback part when they discussed their vibe-coded homepages. Check out [kevinroose.com](https://kevinroose.com/) and [cnewton.org](https://cnewton.org/). Casey's has way more character than Kevin's, which is sort of how I feel about them as people. No offense to Kevin, though that would be hard not to take offense to. 🤡

If you run a Hugo blog (or Jekyll, or any static site), try it out. Instructions are in the [GitHub repo](https://github.com/mreider/mastopub).
