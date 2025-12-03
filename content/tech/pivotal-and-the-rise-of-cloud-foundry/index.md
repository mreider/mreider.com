---
title: "VMware, Pivotal, and the Rise of Kubernetes"
author: "Matt Reider"
date:  "2024-11-28"
image: "/images/matt/Tidal_Wave.jpg"
---

When I left Engine Yard ([see my earlier post](https://mreider.com/tech/Tales_from_Engineyard.html)), I joined VMware to work on the Cloud Foundry team. The idea was ambitious: create a PaaS (Platform as a Service) that allowed developers to write and deploy applications without worrying about infrastructure. It wasn’t revolutionary -Heroku and Engine Yard had similar goals -but it offered something enterprises hadn’t seen before.

The secret weapon was BOSH, a powerful orchestration tool that deployed Cloud Foundry on private or public clouds in a declarative, repeatable way. BOSH had a small but passionate following, with its precision and reliability appealing to those managing complex software deployments. Still, Cloud Foundry itself struggled to balance the needs of developers with the expectations of enterprises. For VMware, it was a critical play to stay relevant as Amazon reshaped the industry.

The Cloud Foundry team was stacked with talent, including Derek Collison (creator of NATS), Peter Noordhuis (a Redis contributor), and Dale Olds (an LDAP pioneer). But even with this star power, the platform had trouble finding its footing. Balancing a hosted PaaS with a self-managed enterprise platform proved overly ambitious, and execution suffered.

VMware eventually leaned toward the self-managed “Google in a box” model, which aligned better with their enterprise audience. But resources were consumed by the hosted PaaS vision, creating frustration, disagreements, and turnover. The slow pivot to focus on enterprise customers was a step in the right direction but came too late to avoid growing pains.

---

## Spinning Out  

The pivot coincided with VMware’s realization that Cloud Foundry didn’t belong inside the company. VMware’s enterprise culture clashed with the open-source ethos Cloud Foundry needed to thrive. Building developer-first tools required transparency, collaboration, and community engagement -values that didn’t align with VMware’s traditional approach.  

So, Cloud Foundry, along with Spring and RabbitMQ, was spun out into Pivotal, a standalone company backed by EMC.  

The transition wasn’t easy, especially for the original Cloud Foundry team. Pivotal’s headquarters in San Francisco made for a difficult commute for VMware-based employees. Pair programming, a cornerstone of Pivotal’s culture, required engineers to work in person, creating tension for those unable or unwilling to adapt. For some, the pairing requirement became a wedge, ensuring early cultural alignment but leading others to leave.  

Despite the challenges, Pivotal’s culture was inspiring. Agile practices were applied rigorously, creating a collaborative and respectful environment. Pair programming and test-driven development weren’t just buzzwords -they were baked into the company’s DNA. It was rewarding to work in a team that operated with such shared purpose, a stark contrast to the earlier Cloud Foundry struggles.

---

## The Kubernetes Wave  

For a while, Pivotal thrived. Agile collaboration and strong leadership created momentum, and big-name clients adopted Cloud Foundry as part of their digital transformations.  

But by 2015, Kubernetes was gaining traction. Backed by major cloud providers, Kubernetes had momentum Pivotal couldn’t match. Leadership debated replacing Cloud Foundry’s scheduler, Diego, with Kubernetes, but it never materialized.  

Pivotal’s customer base included some of the largest companies in the world, deeply invested in Cloud Foundry. But outside these key accounts, growth was slow. The rise of Kubernetes-based solutions like OpenShift created intense competition. OpenShift, once dismissed, pivoted from its “cartridge” model to Kubernetes, combining the simplicity of a PaaS with the flexibility of a cloud-native platform. Managed services from cloud providers only strengthened its appeal, leaving Cloud Foundry struggling to stay relevant.  

Eventually, VMware reacquired Pivotal, integrating Cloud Foundry into its Tanzu product line -a strategy heavily reliant on Kubernetes. The irony wasn’t lost: Cloud Foundry, once positioned as the enterprise solution to platform challenges, was now part of a Kubernetes-first strategy that had redefined the very market it aimed to lead.

---

> *The image of the tidal wave ride is licensed under the Creative Commons Attribution-Share Alike 2.0 Generic license.  
> Original photo reviewed by Wikimedia administrator Yarnalgo on 12 March 2009, confirming availability under the stated license.*
