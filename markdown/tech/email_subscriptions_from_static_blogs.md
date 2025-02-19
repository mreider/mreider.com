---
title: "Email Subscriptions from Static Blogs"
author: "Matt Reider"
date: "2025-02-17"
image: "/images/matt/emails-everywhere.png"
---

In my last blog entry, I introduced Krems, a project I built for generating static blogs. One challenge with static blogs is that they can't run server code or databases, making it impossible to store email addresses for blog subscriptions. There are paid services, like rssfeedpulse.com, that scrape your RSS feed and send new posts to email subscribers.

A few months ago, I built my own version of this service using Python, with [some help from ChatGPT](Building_Quacker.md). I called it Quacker. This week I rewrote the entire thing in Golang. It's been working quite well.

Here’s the email I received via Quacker from the blog post I wrote last night:

![screenshot of a quacker email](/images/matt/email-from-quacker.png)

# How Quacker works

Every few minutes, Quacker fetches the RSS feeds of every blog in its database and emails them to all subscribed users. To add a blog to the database, simply log in and create a new entry like this:

![adding a site to quacker](/images/matt/quacker-add-site.png)

Once the site is saved you each user will see it in their site list (here there's only one site listed for mreider).

![mreider site list](/images/matt/quacker-site-list.png)

From here you can click View HTML    and see the email subscription form to paste into your blog.

![html form](/images/matt/quacker-html-form.png)

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

