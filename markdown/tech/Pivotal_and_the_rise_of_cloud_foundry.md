+++
title = "VMware, Pivotal and the rise of Kubernetes"
date = "2024-11-28"
summary = "Building a successful platform, spinning out into something new, and facing big shifts in the industry"
author = "Matt Reider"
image = "/images/matt/Tidal_Wave.jpg"
+++

When I left Engine Yard ([see my first post from October](https://aligned.at/posts/engine-yard-and-the-cost-of-venture-capital/)), I joined VMware to work on the Cloud Foundry team. The idea was ambitious: create a PaaS (Platform as a Service) that let developers write and deploy applications without worrying about infrastructure. It wasn’t groundbreaking—Heroku and Engine Yard had similar goals—but it was something enterprises hadn’t seen before.

The secret weapon was BOSH, a powerful orchestration system designed to deploy Cloud Foundry on private or public clouds in a declarative, repeatable manner. BOSH’s approach resonated with a small but passionate audience who valued its ability to manage the complexity of software deployments with precision and reliability. However, Cloud Foundry itself faced challenges as it tried to balance the needs of developers with the expectations of enterprises. VMware viewed it as a critical play to remain relevant in an industry being transformed by Amazon’s dominance.

The Cloud Foundry crew was stacked with talent: Derek Collison (creator of NATS), Peter Noordhuis (a Redis contributor), and Dale Olds (an LDAP pioneer). Despite the star power, the platform struggled to find its footing. The vision—balancing a hosted PaaS and a self-managed enterprise platform—was overly ambitious, and the execution reflected that.

The marketing team, believed the self-managed model—“Google in a box”—was a better fit for VMware’s enterprise audience. But the hosted PaaS consumed most of our resources. The tension was palpable, and the misalignment created frustration, disagreements, and eventual resignations. The result? A slow pivot toward what should have been the focus all along: the enterprise-ready, self-managed platform.

## The Big Spin-Out  

That pivot coincided with VMware’s realization that Cloud Foundry didn’t belong inside the company. VMware’s culture didn’t align with the open-source ethos that Cloud Foundry needed to thrive. Building developer-first tools required a level of transparency, collaboration, and community engagement that was difficult to achieve within a traditional enterprise. So Cloud Foundry, along with Spring and RabbitMQ, was spun out into Pivotal, a standalone company backed by EMC.

The spin-out came with its own challenges, particularly for the original Cloud Foundry team. Pivotal’s headquarters in San Francisco created a tough commute for those who had been based in the Valley at VMware. Pair programming, a cornerstone of Pivotal’s culture, required engineers to be physically present, and while some made the move, others weren’t willing or able to make that adjustment. There was also resistance to the idea of pairing itself—many believed it didn’t make a significant difference. Looking back, it seems this rigid in-person pairing requirement may have been an intentional wedge, ensuring cultural alignment during Pivotal’s formative years. As the company matured, flexibility around pairing increased, but early on, it contributed to departures as some opted for less demanding setups.

Internally, Pivotal’s culture was both impressive and inspiring. The agile practices championed by Pivotal Labs were embraced with diligence and consistency, creating an environment of collaboration and respect. The staff’s loyalty to Rob Mee, the company’s co-founder and CEO, reflected genuine admiration for his leadership and vision. Practices like pair programming and test-driven development were not just policies—they were integrated into the company’s operations. For me, tech writingly, it was a rewarding time to be part of a team that operated with such focus and shared purpose, a welcome contrast to the challenges of Cloud Foundry’s earlier days. 

## Facing the Unstoppable Shift  

For a few years, things at Pivotal felt great. The agile practices, collaboration, and strong leadership created a sense of momentum and purpose. Big-name clients were adopting Cloud Foundry, and Pivotal seemed to be thriving as the go-to partner for enterprises embracing digital transformation.

By 2015, the rise of Kubernetes couldn’t be ignored. A lot of our leadership, including James Watters, saw the writing on the wall. They recognized Kubernetes’s momentum, fueled by its strong backing from major cloud providers. However, Pivotal was fundamentally an engineering-driven company, and that ultimately shaped our path. We debated replacing Cloud Foundry’s scheduler, Diego, with Kubernetes. It never came to be.

Pivotal’s portfolio wasn’t just a handful of customers—it included some of the largest and most influential companies in their respective sectors. These “elephants” were deeply invested in Cloud Foundry, and their adoption was a testament to its enterprise capabilities. However, growth outside of these key accounts was slow, leaving the company increasingly reliant on its existing base as the market evolved.

OpenShift, which initially wasn’t seen as a competitor, transformed dramatically by switching from its “cartridge” model to a Kubernetes-based architecture. This pivot turned OpenShift into a serious rival, offering the simplicity of a PaaS with a user-friendly CLI for deploying applications, backed by Kubernetes’s power and flexibility. Some cloud providers even offered OpenShift as a managed service, creating a strong mix of ease of use and cloud-native capabilities. The competition intensified, leaving Cloud Foundry struggling to stay relevant in a Kubernetes-dominated ecosystem.

Eventually, VMware reacquired Pivotal, folding Cloud Foundry into its Tanzu product line—a move that leaned heavily on Kubernetes. The irony of the shift wasn’t lost: Cloud Foundry, once seen as the enterprise answer to a platform dilemma, was now part of a Kubernetes-focused strategy that had redefined the market it aimed to lead.

> *The image of the tidal wave ride is licensed under the Creative Commons Attribution-Share Alike 2.0 Generic license.  
> The image, originally posted to Flickr, was reviewed on 12 March 2009 by the Wikimedia administrator or reviewer Yarnalgo, who confirmed that it was available on Flickr under the stated license on that date.