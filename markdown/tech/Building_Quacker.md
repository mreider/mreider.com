+++
title = "Building Quacker: A Weekend Project with ChatGPT"
date = "2024-11-26"
author = "Matt Reider"
summary = "Building an app with AI is both impressive and frustrating."
categories = ["tech writing"]
tags = ["ChatGPT","AI","Agile"]
images = ["/images/matt/duck.jpg"]
+++

Last weekend, I built [Quacker](https://github.com/mreider/quacker), a Python app that lets static blogs send newsletters. Static blogs are simple, reliable, and fast—but they’re missing some essentials, like email subscriptions or notifications for new posts. I could’ve switched to something like Ghost, which would’ve been quicker and easier, but instead, I chose to spend my weekend reinventing the wheel. Maybe not my smartest decision.  

Quacker does what I need: it adds a subscribe form to my blog, stores emails, polls the RSS feed for updates, and sends subscribers an email if I post something new. It’s not groundbreaking—there are plenty of tools that do this better.

I used ChatGPT almost the whole time. I started with a clear plan (Flask, SQLite, Gunicorn, Nginx) and let ChatGPT take the lead on writing the initial setup. From there, it was an endless loop of tweaking and debugging.  

ChatGPT can’t keep up with complex, multi-step projects. The longer we iterated, the more its suggestions became a messy mix of old fixes and new ideas, riddled with subtle errors. For example, there was a duplicate email bug. ChatGPT proposed an ok solution—adding a table to track sent posts—but reintroduced earlier bugs in the process. It’s not that it “forgot”; it just couldn’t juggle all the moving parts.  

At some point, I realized I was doing more work *because* of ChatGPT, not less. Every major fix required resetting the chat, pasting my latest working code, and explaining the problem all over again. For quick tasks, ChatGPT is brilliant. For anything more complex, it’s exhausting.  

Also - it doesn’t know when it’s failing. Instead of stopping when it’s out of its depth, it keeps generating solutions that are just close enough to seem right but wrong enough to waste your time. Off we go. Around in circles.

But stepping back it's like [Louis C.K.’s joke](https://www.youtube.com/watch?v=kBLkX2VaQs4) about people complaining on airplanes - griping about Wi-Fi or legroom, forgetting they’re flying through the sky in a metal tube. ChatGPT isn’t perfect, but the fact that it can almost build an app at all is remarkable.

> *The image of the duck is licensed under the Creative Commons Attribution-Share Alike 2.0 Generic license.  
> Original photo by Ernst Vikne. Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:White_domesticated_duck,_stretching.jpg).*