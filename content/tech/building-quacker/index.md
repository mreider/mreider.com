---
title: "Building Quacker: A Weekend Project with ChatGPT"
description: "Building an app with AI is both impressive and frustrating"
author: "Matt Reider"
date: "2024-11-26"
image: "/images/matt/duck.jpg"
---

Last weekend, I built [Quacker](https://github.com/mreider/quacker), a Python app that lets static blogs send newsletters. Static blogs are simple, fast, and reliable - but they don't have built-in features like email subscriptions or post notifications. I could've used something like Ghost, but I spent the weekend reinventing the wheel.

Quacker does what I need: it adds a subscription form to my blog, stores emails, checks the RSS feed for updates, and sends subscribers an email when there's a new post. It's not fancy, and there are better tools out there, but it works.

I used ChatGPT to build most of it. I started with a clear plan (Flask, SQLite, Gunicorn, Nginx) and let ChatGPT handle the initial setup. From there, it became a constant cycle of tweaking and debugging.

ChatGPT works well for quick, isolated tasks, but it struggles with complex, multi-step projects. The longer we iterated, the more its suggestions became a mix of old fixes and new ideas, with subtle bugs creeping in. For example, there was a duplicate email bug. ChatGPT's solution - adding a table to track sent posts - was fine in theory, but it accidentally reintroduced earlier bugs. It wasn't "forgetting" exactly, but it couldn't keep track of all the moving parts.

I realized I was doing more work because of ChatGPT, not less. Every major fix required resetting the chat, pasting my latest code, and re-explaining the issue from scratch. It was like a loop: solve one thing, break another, repeat.

ChatGPT doesn't know when it's out of its depth. Instead of stopping, it keeps generating solutions that look good at first but end up wasting your time. It's like taking advice from someone who confidently knows just enough to be dangerous.

Still, it's impressive. It reminds me of [Louis C.K.'s joke](https://www.youtube.com/watch?v=kBLkX2VaQs4) about people complaining on airplanes - griping about Wi-Fi or legroom while flying through the sky in a metal tube. ChatGPT isn't perfect, but the fact that it can almost build an app is remarkable.

---

> *The image of the duck is licensed under the Creative Commons Attribution-Share Alike 2.0 Generic license.  
> Original photo by Ernst Vikne. Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:White_domesticated_duck,_stretching.jpg).*
