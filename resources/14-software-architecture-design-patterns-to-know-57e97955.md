# 14 software architecture design patterns to know

Source: https://www.redhat.com/en/blog/14-software-architecture-patterns

## Identified Architecture Patterns

### Microservices

- The [**microservices**](https://www.redhat.com/architect/5-essential-patterns-software-architecture#microservices) pattern combines design patterns to create multiple services that work interdependently to create a larger application.
- While it helps make systems more fault tolerant to prevent accidents, it also requires sophisticated testing and using an infrastructure-management technology like service mesh.

### Event Driven

- ]***

The [**event sourcing**](https://www.redhat.com/architect/pros-and-cons-event-sourcing-architecture-pattern) pattern is good for applications that use real-time data.

### Data Storage

- It separates read and write activities to provide greater stability, scalability, and performance, but it requires more database technologies and therefore may increase costs.
- It stores static content (information that doesn't change often, like an author's bio or an MP3 file) separately from dynamic content (like stock prices).
- It places the old system behind an intermediary to support incremental transformation, which reduces risk compared to making larger changes.

### Api Design

- If one piques your interest, click the link to learn more.
- One advantage is that you can read data from the responder without affecting the data in the controller, but if the controller fails, you may lose data and need to restart the application.

### Api Security

- The [**throttling**](https://www.redhat.com/architect/pros-and-cons-throttling) (or rate-limiting) pattern controls how fast data flows into a target.

### Performance

- The [**throttling**](https://www.redhat.com/architect/pros-and-cons-throttling) (or rate-limiting) pattern controls how fast data flows into a target.


---

14 software architecture design patterns to know
================================================

March 16, 2022[Vicki Walker](/en/authors/vwalker "See more by Vicki Walker")*4*-minute read

[Professional development](/en/blog?f[0]=taxonomy_topic_tid:107491#rhdc-search-listing) [Culture and process](/en/blog?f[0]=taxonomy_topic_tid:27021#rhdc-search-listing)

Share



Subscribe

If you design software architectures, chances are that you come across the same goals and problems over and over again. Architectural patterns make it easier to solve these issues by providing repeatable designs that address common situations. As [Anand Butani explains](https://www.redhat.com/architect/5-essential-patterns-software-architecture):

> "The architectural pattern captures the design structures of various systems and elements of software so that they can be reused. During the process of writing software code, developers encounter similar problems multiple times within a project, within the company, and within their careers. One way to address this is to create design patterns that give engineers a reusable way to solve these problems, allowing software engineers to achieve the same output structurally for a given project."

***[ Download [the automation architect's handbook](https://www.redhat.com/en/engage/automation-architect?intcmp=7013a0000025wJwAAI). ]***

There are numerous advantages to using architectural patterns in your software designs. They increase your efficiency, productivity, and speed; optimize development costs; improve planning; and more.

There are many different types of enterprise architect design patterns you can tap into. To help you decide what's right for your project, I've rounded up 14 previous articles about architectural design patterns and summarized them below. If one piques your interest, click the link to learn more.

14 software architecture patterns
---------------------------------

The [**circuit breaker**](https://www.redhat.com/architect/circuit-breaker-architecture-pattern) pattern minimizes the effects of a hazard by rerouting traffic to another service. While it helps make systems more fault tolerant to prevent accidents, it also requires sophisticated testing and using an infrastructure-management technology like service mesh.

The [**client-server**](https://www.redhat.com/architect/5-essential-patterns-software-architecture#client-server) pattern is a peer-to-peer architecture that is comprised of a *client*, which requests a service, and a *server*, which provides the the service. Examples include banking, file sharing, email, and the World Wide Web. One advantage of this pattern is that data and network peripherals are centrally managed, however, the server is expensive.

The [**command query responsibility segregation**](https://www.redhat.com/architect/pros-and-cons-cqrs) (CQRS) pattern handles the situation where database queries happen more often than the data changes. It separates read and write activities to provide greater stability, scalability, and performance, but it requires more database technologies and therefore may increase costs.

The [**controller-responder**](https://www.redhat.com/architect/5-essential-patterns-software-architecture#controller-responder) pattern divides the architecture into two components: The controller handles the data and distributes workloads, and the responder replicates data from the controller and generates results. One advantage is that you can read data from the responder without affecting the data in the controller, but if the controller fails, you may lose data and need to restart the application.

***[ Learn more about cloud-native development in the eBook [Kubernetes Patterns: Reusable elements for designing cloud-native applications](https://www.redhat.com/en/engage/kubernetes-containers-architecture-s-201910240918?intcmp=7013a0000025wJwAAI). ]***

The [**event sourcing**](https://www.redhat.com/architect/pros-and-cons-event-sourcing-architecture-pattern) pattern is good for applications that use real-time data. It sends a continuous stream of messages to a database, web server, log, or another target. It's very flexible but demands a highly efficient and reliable network infrastructure to minimize latency.

The [**layered**](https://www.redhat.com/architect/5-essential-patterns-software-architecture#layered) pattern is good for e-commerce, desktop, and other applications that include groups of subtasks that execute in a specific order. The layered pattern makes it easy to write applications quickly, but a disadvantage is that it can be hard to split up the layers later.

The [**microservices**](https://www.redhat.com/architect/5-essential-patterns-software-architecture#microservices) pattern combines design patterns to create multiple services that work interdependently to create a larger application. Because each application is small, it's easier to update them when needed, but the complexity means you need greater architectural expertise to make everything work correctly.

The [**model-view-controller**](https://www.redhat.com/architect/5-essential-patterns-software-architecture#MVC) (MVC) pattern divides an application into three components. The *model* contains the application's data and main functionality; the *view* displays data and interacts with the user; and the *controller* handles user input and acts as the mediator between the model and the view. This pattern enables the application to generate various views, but its layers of abstraction increase complexity.

***[ Learn more about [validated patterns](https://www.redhat.com/en/topics/cloud-computing/what-are-validated-patterns?intcmp=7013a0000025wJwAAI). ]***

The [**pub-sub**](https://www.redhat.com/architect/pub-sub-pros-and-cons) pattern sends (*publishes*) relevant messages to places that have *subscribed* to a topic. It's easy to configure but more challenging to test because interactions between the publisher and the subscriber are asynchoronous.

The [**saga**](https://www.redhat.com/architect/pros-and-cons-saga-architecture-pattern) pattern is used for transactions with multiple steps, such as travel reservation services. A "saga" includes the various steps that must happen for the transaction to complete. This pattern enables transactions (ideally with five or fewer steps) to happen in loosely coupled, message-driven environments, but it requires a lot of programming and can be complex to manage.

The [**sharding**](https://www.redhat.com/architect/pros-and-cons-sharding) pattern segments data in a database to speed commands or queries. It ensures storage is consumed equally across instances but demands a skilled and experienced database administrator to manage sharding effectively.

The [**static content hosting**](https://www.redhat.com/architect/pros-and-cons-static-content-hosting-architecture-pattern) pattern is used to optimize webpage loading time. It stores static content (information that doesn't change often, like an author's bio or an MP3 file) separately from dynamic content (like stock prices). It's very efficient for delivering content and media that doesn't change often, but downsides include data consistency and higher storage costs.

The [**strangler**](https://www.redhat.com/architect/pros-and-cons-strangler-architecture-pattern) pattern is used when you're making incremental changes to a system. It places the old system behind an intermediary to support incremental transformation, which reduces risk compared to making larger changes. However, you need to pay close attention to routing and network management and make sure you have a rollback plan in place in case things go wrong.

The [**throttling**](https://www.redhat.com/architect/pros-and-cons-throttling) (or rate-limiting) pattern controls how fast data flows into a target. It's often used to prevent failure during a distributed denial of service attack or to manage cloud infrastructure costs. To use this pattern successfully, you need good redundancy mechanisms in place, and it's often used alongside the circuit breaker pattern to maintain service performance.

Summary
-------

The next time you're embarking on a new software architecture, consider which of these (or the many other) architectural design patterns you can use to make your work more efficient.

***[ Working at the edge? [Learn more about validated patterns](https://www.redhat.com/en/products/edge/validated-patterns?intcmp=7013a0000025wJwAAI). ]***

---



### About the author

[![Vicki Walker](https://www.redhat.com/rhdc/managed-files/styles/media_thumbnail/private/sysadmin/pictures/2021-07/VW_headshot.jpg?itok=PxXt1J6U)](/en/authors/vwalker)

[### Vicki Walker](/en/authors/vwalker)



Vicki Walker is Managing Editor of Enable Sysadmin and Enable Architect for Red Hat. She has more than 20 years of experience in technology publishing for companies including InformationWeek.com, Dark Reading, SAP, BlackBerry, and Network Computing. She is a liberal arts graduate of the University of Florida and earned a certificate in core public health concepts from the University of North Carolina at Chapel Hill. She lives in Charlotte, N.C. with her husband, two children, a dog, and a cat, and avidly follows Carolina Panthers football.


[Read full bio](/en/authors/vwalker)

Enter keywords here to search blogs


UI\_Icon-Red\_Hat-Close-A-Black-RGB

Search

More like this
--------------

### [Blog post](/en/blog/building-and-scaling-ai-models-machine-learning-engineer)

#### [Building and scaling AI models as a machine learning engineer](/en/blog/building-and-scaling-ai-models-machine-learning-engineer)

### [Blog post](/en/blog/how-ansible-automation-platform-supports-your-automation-community-practice)

#### [How Ansible Automation Platform supports your automation community of practice](/en/blog/how-ansible-automation-platform-supports-your-automation-community-practice)

### [Original shows](/en/compiler-podcast/diagnosing-and-dispelling-ai-hallucinations)

#### [Diagnosing and Dispelling AI Hallucinations | Compiler](/en/compiler-podcast/diagnosing-and-dispelling-ai-hallucinations)

### [Original shows](/en/compiler-podcast/ai-feedback-loops)

#### [Chasing Its Own Tail | Compiler](/en/compiler-podcast/ai-feedback-loops)

Browse by channel
-----------------

[Explore all channels](/en/blog/channels "Explore all channels")

![automation icon](https://www.redhat.com/cms/managed-files/automation.svg)

### [Automation](/en/blog/channel/management-and-automation)

The latest on IT automation for tech, teams, and environments

![AI icon](https://www.redhat.com/cms/managed-files/AI.svg)

### [Artificial intelligence](/en/blog/channel/artificial-intelligence)

Updates on the platforms that free customers to run AI workloads anywhere

![open hybrid cloud icon](https://www.redhat.com/cms/managed-files/open-hybrid-cloud.svg)

### [Open hybrid cloud]([[url-nid:292921;title:Open Hybrid Cloud]])

Explore how we build a more flexible future with hybrid cloud

![security icon](https://www.redhat.com/cms/managed-files/security.svg)

### [Security](/en/blog/channel/security)

The latest on how we reduce risks across environments and technologies

![edge icon](https://www.redhat.com/cms/managed-files/edge_2.svg)

### [Edge computing](/en/blog/channel/edge-computing)

Updates on the platforms that simplify operations at the edge

![Infrastructure icon](https://www.redhat.com/cms/managed-files/infrastructure.svg)

### [Infrastructure](/en/blog/channel/infrastructure)

The latest on the world’s leading enterprise Linux platform

![application development icon](https://www.redhat.com/cms/managed-files/application-development.svg)

### [Applications](/en/blog/channel/applications)

Inside our solutions to the toughest application challenges

![Original series icon](https://www.redhat.com/cms/managed-files/original-series.svg)

### [Original shows](/en/red-hat-original-series)

Entertaining stories from the makers and leaders in enterprise tech