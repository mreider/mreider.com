---
title: "Engine Yard and the Cost of Venture Capital"
author: "Matt Reider"
date:  "2024-10-19"
description: "My experience at Engine Yard and how venture funding shaped its fate."
image: "/images/matt/old-train.jpg"
---

Back in the early days of cloud computing, before "cloud" meant what it does today, we were one of the original cloud vendors. Our infrastructure ran on custom-patched Gentoo servers -nicknamed "pizza boxes" -housed in two data centers on opposite coasts. Scaling wasn’t automated. It was manual, requiring real humans to intervene. As our head of support jokingly put it, we were a "meat cloud."

Still, we were ahead of the curve, offering a platform as a service (PaaS) for Ruby on Rails apps, MongoDB, and MySQL databases. Developers could push their code, and it “just worked.”  

---

## Building a Community  

Our co-founder, Ezra Zygmuntowicz, was a legend in the Ruby community. He authored Merb, which eventually merged with Rails. Other big names in Ruby worked at Engine Yard, too: Wayne Seguin (creator of RVM), Carl Lerche and Yehuda Katz (co-creators of Bundler), Evan Phoenix (Rubinius), and even the JRuby team.  

Engine Yard wasn’t just a hosting company -it was a sponsor for open-source talent. These folks didn’t work on Engine Yard’s product. They worked on Rails itself, advancing the ecosystem. They ate lunch with us, joked with us, and occasionally drank with us (though less so with me -I was 15 years older, with toddlers at home, a house in the suburbs, and zero tattoos).

By the time I arrived, the product itself was in rough shape. Customers had slightly customized setups running on slightly different Gentoo configurations. Shared storage from CORAID, a budget vendor, was a frequent point of failure, causing blackouts or brownouts. Much of my job involved writing postmortems and negotiating with frustrated customers.

Our customer base was impressive: GitHub, New Relic, and Groupon were all on our platform. Hosting GitHub for free gave us credibility in the Rails community -it was marketing gold. But years went by, and GitHub never paid us a dime. It became an inside joke: Engine Yard was "selling dollars for 99 cents."  

When I read quotes from GitHub’s founders about "never needing venture funding," it still stings. Of course, they didn’t -we paid their infrastructure bills.

---

## The New Guard  

By 2009, when I joined, things were changing. Investors wanted profitability and a scalable product. The new leadership was tasked with cleaning up the platform, retiring the pizza boxes, and migrating customers to something sustainable.  

We gave customers three options:  

1. Migrate to Engine Yard on Terremark Cloud for a premium.  
2. Refactor their apps into "12-factor apps" (the precursor to "cloud-native") and move to Engine Yard on AWS.  
3. Leave Engine Yard entirely.  

Some migrated, but many left -including GitHub. For those who stayed, the process was messy but necessary. To celebrate the end of the migrations, we smashed an old pizza box with a sledgehammer in the parking lot of Tres Agaves, a nearby Mexican restaurant. It was more gimmicky than satisfying.  

---

## The Decline  

Even after the migrations, things didn’t go well. Heroku, our biggest competitor, had been acquired by Salesforce and was dominating the market. They’d gone cloud-native from the start and supported more than just Rails. Their platform was easier to use, and they had the resources to outpace us.

There were also missed opportunities. VMware once offered to buy Engine Yard for $200 million. Our founders turned it down, thinking it wasn’t enough. Ezra told me about the offer -in the bathroom, of all places. He was crushed. He wanted the payout. Not long after, he left Engine Yard to work on Cloud Foundry at VMware. Tragically, a few years later, he took his own life, leaving behind a wife and a newborn son.

In the end, Engine Yard couldn’t survive. The energy of the Rails community that once made us special wasn’t enough to keep us afloat. Like so many startups, our story ended with a worthless stock certificate and lessons learned the hard way.

---

> *The image of the train is licensed under the Creative Commons Attribution-Share Alike 2.0 Generic license.  
> Original photo by train_photos. Source: [Flickr](https://
