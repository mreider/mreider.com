---
title: "Email Subscriptions from Static Blogs"
author: "Matt Reider"
date: "2025-02-17"
image: "/images/matt/emails-everywhere.png"
---

In my [last blog entry](krems_static_site_generator.md), I introduced Krems, a project I built for generating static blogs. One of the challenges with static blogs is their inability to run server-side code or databases, which makes storing email addresses for blog subscriptions impossible. To work around this, you can either use a paid service like [rssfeedpulse.com](https://rssfeedpulse.com) to scrape your RSS feed and email new posts to subscribers, or you can encourage readers to follow your blog using an RSS reader.

A few months ago, I decided to build my own alternative to RSSFeedPulse using Python with [some help from ChatGPT](Building_Quacker.md).his week, I took it a step further and rewrote the entire application in Golang. So far, it's been running smoothly. I named it Quacker, and you can check it out at [quacker.eu](https://quacker.eu). However, access is restricted — you'll need me to add your GitHub username to the approved list before you can log in.

Last night, after publishing a new blog post, Quacker did exactly what it was designed to do — it sent me an email notification.

![screenshot of a quacker email](/images/matt/email-from-quacker.png)

# How it works

Every few minutes, Quacker fetches the RSS feeds of every blog in its database and emails new posts to subscribed users. To add a blog to the database, simply log in and create a new entry like this:

![adding a site to quacker](/images/matt/quacker-add-site.png)

Once the site is saved it shows up in my site list (here there's only one site listed).

![mreider site list](/images/matt/quacker-site-list.png)

From here you can click View HTML and see the email subscription form to paste into your blog.

![html form](/images/matt/quacker-html-form.png)

This HTML snipped creates a little form that will subscribe users to your blog posts.

![subscribe form](/images/matt/quacker-form.png)

# Krems auto-quacker config

As the creator of [Krems](krems_static_site_generator.md), which generated the blog you're currently looking at, I decided to streamline the process by integrating a Quacker config into Krems’ config parser. The email subscription form you're seeing here on mreider.com was generated using the following configuration:

```yaml
quacker:
  domain: "mreider.com"
  site_owner: "mreider"
  target: "quacker.eu"
```

# Open to sharing

If you run a static blog using Hugo or Jekyll and want to try Quacker without hosting it yourself, I’d be open to adding you to the site owner list. Since Quacker uses GitHub login IDs, all I’d need is your GitHub username to set you up.

# Install your own quacker

To install Quacker on your own server, follow the instructions in the [Github repository](https://github.com/mreider/quacker). If you run into any issues, have ideas, or want to give feedback, feel free to open a discussion on Quacker’s [Github issues](https://github.com/mreider/quacker/issues).

