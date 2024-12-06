+++
title = "Engine Yard and the Cost of Venture Capital"
date = "2024-10-19"
summary = "Sharing my experiences at Engine Yard and how venture funding shaped its future"
categories = ["tech writing"]
author = "Matt Reider"
images = ["/images/matt/old-train.jpg"]
+++


We were one of the original cloud vendors, back before "cloud" meant what it does today. Our infrastructure was built on custom-patched Gentoo servers—lovingly nicknamed "pizza boxes" — housed in two data centers on opposite coasts. Every customer knew the exact moment their pizza boxes would light up, serving traffic. It wasn’t like the elastic cloud of today. You couldn’t just spin up a VM and shut it down at will. Scaling required humans. As the head of our support team jokingly called it, we were a "meat cloud."

Still, we were ahead of the game, offering a platform as a service (PaaS) specifically for Ruby on Rails apps, MongoDB, and MySQL databases. Customers didn’t have to configure anything. You pushed your code, and it "just worked."

Our co-founder, Ezra Zygmuntowicz, was a legend in the Ruby community. He authored Merb, which later merged with Rails. And there were other Ruby on Rails heros there too. Wayne Seguin (creator of RVM), Carl Lerche, Yehuda Katz (co-creators of Bundler), Evan Phoenix (Rubinius), and eventually the entire JRuby team. Engine Yard wasn’t just a hosting company — it was a friendly sponsor for open-source talent.

By the time I arrived, none of these folks were working directly on Engine Yard's product. They were focused on Rails itself, pushing the ecosystem forward. They ate lunch with us, joked with us, and drank with us. Well, not so much with me — I was at least 15 years older, with toddlers at home, a house in the suburbs, and zero tattoos.

The product itself was a bit of a mess by then. Every customer had their own slightly customized setup running on slightly different Gentoo configurations, with shared storage from an inexpensive vendor (CORAID) that was notoriously fragile under load. When shared storage failed, it would take down clusters, causing blackouts or brownouts for customers. Much of my time was spent on the phone with customers, investigating problems, writing postmortems, and negotiating compensation.

Our customers were a who’s who of Ruby startups including GitHub, New Relic, and Groupon. Hosting GitHub for free gave us credibility in the Rails community — it was marketing gold. But years went by and GitHub never paid us a dime. That was weird.

We joked that Engine Yard "sold dollars for 99 cents."

Even though the agreement to host GitHub for free started before my time, it stings when I read quotes from GitHub's co-founders about never needing venture funding. Of course they didn’t — we footed their infrastructure bill.

## The New Guard

When I joined (2009) things were changing. Investors wanted profitability and a “real” product. The new guard was tasked with transforming our quirky, beloved platform into something scalable and maintainable. Our job was to clean up the snowflakes — migrating customers off their custom setups to something sustainable and retiring the clusters in our data centers.

The migration effort was massive. 

We gave customers three options:

1. Move to Engine Yard on Terremark Cloud at a premium cost with better shared storage.
2. Refactor their apps into "12-factor apps" (the Heroku term that preceded "cloud-native") and move to Engine Yard on AWS.
3. Leave Engine Yard entirely.

Some customers migrated with us - but many left. GitHub was one of them. For those who stayed, we coordinated migrations and tracked progress. It was messy work, but we got it done. To celebrate, we smashed an old pizza box with a sledgehammer in the parking lot of Tres Agaves, a nearby Mexican restaurant. It more gimmicky, and less satisfying, than we’d hoped.

The Decline

Even after the migrations, things didn’t go very well. Heroku, our biggest competitor, had been acquired by Salesforce and was dominating the Rails hosting market They’d opted for a cloud-native design earlier and had stronger UX. Also, by then, they supported more than just Rails.

There were also major missed opportunities. VMware offered to buy us for something like $200 million. Our founders turned it down, thinking it wasn’t enough. Ezra told me about it - in of all places - the bathroom. He was crushed. He wanted the payout. Not long after, he left Engine Yard to work on Cloud Foundry at VMware. Tragically, he took his own life a few years later, leaving behind a wife and a newborn son.

In the end, Engine Yard struggled to survive. The cult-like energy of the Rails community, which had once made us special, wasn’t enough to sustain us. I’d bought stock in the company, hoping they'd IPO. But like so many startups, the certificate turned out to be worthless.

> *The image of the train is licensed under the Creative Commons Attribution-Share Alike 2.0 Generic license.  
> This image was originally posted to Flickr by train_photos at https://flickr.com/photos/99279135@N05/22299294105 (archive).