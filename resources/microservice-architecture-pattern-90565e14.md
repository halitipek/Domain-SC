# Microservice Architecture pattern

Source: https://microservices.io/patterns/microservices.html

## Identified Architecture Patterns

### Microservices

- # Microservice Architecture pattern

Source: https://microservices.io/patterns/microservices.html

#### [Microservice Architecture](/index.html)

**Supported by [Kong](https://konghq.com/)**

Microservice Architecture pattern
=================================

[pattern](/tags/pattern) 

[application architecture](/tags/application architecture) 

[microservice architecture](/tags/microservice architecture) 
  


---

Pattern: Microservice Architecture
==================================

Want to learn how to design a microservice architecture?
- --------------------------------------------------------

Take a look at [Assemblage, a microservice architecture definition process](/post/architecture/2023/02/09/assemblage-architecture-definition-process.html).
- [![](/i/posts/assemblage-overview/Defining_Microservice_Architecture_V2.png)](/post/architecture/2023/02/09/assemblage-architecture-definition-process.html)

Context
-------

You are developing a business-critical enterprise application.

### Data Storage

- Fill in [this form](https://forms.gle/ppYDAF1JxHGec8Kn9).
- #### Consulting services

[Engage Chris](http://www.chrisrichardson.net/consulting.html) to create a microservices adoption roadmap and help you define your microservice architecture,

---

#### The Eventuate platform

Use the [Eventuate.io platform](https://eventuate.io) to tackle distributed data management challenges in your microservices architecture.

### Api Design

- ![](/i/posts/microservices-teams-subdomains.png)

An [API gateway](/patterns/apigateway.html) is typically the application’s entry point.
- * The [API Gateway pattern](apigateway.html) defines how clients access the services in a microservice architecture.

### Integration

- * Testing patterns: [Service Component Test](testing/service-component-test.html) and [Service Integration Contract Test](testing/service-integration-contract-test.html)
* [Circuit Breaker](/patterns/reliability/circuit-breaker.html)
* [Access Token](/patterns/security/access-token.html)
* Observability patterns:
  + [Log aggregation](/patterns/observability/application-logging.html)
  + [Application metrics](/patterns/observability/application-metrics.html)
  + [Audit logging](/patterns/observability/audit-logging.html)
  + [Distributed tracing](/patterns/observability/distributed-tracing.html)
  + [Exception tracking](/patterns/observability/exception-tracking.html)
  + [Health check API](/patterns/observability/health-check-api.html)
  + [Log deployments and changes](/patterns/observability/log-deployments-and-changes.html)
* UI patterns:
  + [Server-side page fragment composition](/patterns/ui/server-side-page-fragment-composition.html)
  + [Client-side UI composition](/patterns/ui/client-side-ui-composition.html)
* The [Single Service per Host](deployment/single-service-per-host.html) and [Multiple Services per Host](deployment/multiple-services-per-host.html) patterns are two different deployment strategies.

### Scalability

- A distributed system operation is implemented using the [service collaboration patterns](/post/patterns/2023/07/29/service-collaboration-patterns.html).


---

#### [Microservice Architecture](/index.html)

**Supported by [Kong](https://konghq.com/)**

Microservice Architecture pattern
=================================

[pattern](/tags/pattern) 

[application architecture](/tags/application architecture) 

[microservice architecture](/tags/microservice architecture) 
  


---

Pattern: Microservice Architecture
==================================

Want to learn how to design a microservice architecture?
--------------------------------------------------------

Take a look at [Assemblage, a microservice architecture definition process](/post/architecture/2023/02/09/assemblage-architecture-definition-process.html).

In my workshop, you will learn about to use Assemblage to design a microsevice architecture for your application.

[![](/i/posts/assemblage-overview/Defining_Microservice_Architecture_V2.png)](/post/architecture/2023/02/09/assemblage-architecture-definition-process.html)

Context
-------

You are developing a business-critical enterprise application.
You need to deliver changes rapidly, frequently and reliably - as measured by the [DORA metrics](/articles/glossary#dora-metrics) - in order for your business to thrive in today’s volatile, uncertain, complex and ambiguous world.
Consequently, your engineering organization is organized into small, loosely coupled, cross-functional teams as described by [Team Topologies](/tags/team%20topologies).
Each team delivers software using DevOps practices as defined by the [DevOps handbook](/tags/devops).
In particular, it practices continuous deployment.
The team delivers a stream of small, frequent changes that are tested by an automated deployment pipeline and deployed into production.

![](/i/posts/teams-own-subdomains.png)

A team is responsible for one or more subdomains.
A subdomain is an implementable model of a slice of business functionality, a.k.a. business capability.
It consists of business logic, which consists of business entities (a.k.a. DDD aggregates) that implement business rules, and adapters, which communicate with the outside world.
A Java-based subdomain, for example, consists of classes organized into packages that’s compiled into a JAR file.

The subdomains implement the application’s behavior, which consists of a set of (system) operations.
An operation is invoked in one of three ways: synchronous and asynchronous requests from clients; events published by other applications and services; and the passing of time.
It mutates and queries business entities in one or more subdomains.

Problem
-------

How to organize the subdomains into one or more deployable/executable components?

Forces
------

There are five [dark energy forces](/post/microservices/2021/11/30/dark-matter-dark-energy.html):

* [Simple components](/articles/dark-energy-dark-matter/dark-energy/simple-components.html) - simple components consisting of few subdomains are easier to understand and maintain than complex components
* [Team autonomy](/articles/dark-energy-dark-matter/dark-energy/team-autonomy.html) - a team needs to be able to develop, test and deploy their software independently of other teams
* [Fast deployment pipeline](/articles/dark-energy-dark-matter/dark-energy/fast-deployment-pipeline.html) - fast feedback and high deployment frequency are essential and are enabled by a fast deployment pipeline, which in turn requires components that are fast to build and test.
* [Support multiple technology stacks](/articles/dark-energy-dark-matter/dark-energy/multiple-technology-stacks.html) - subdomains are sometimes implemented using a variety of technologies; and developers need to evolve the application’s technology stack, e.g. use current versions of languages and frameworks
* [Segregate by characteristics](/articles/dark-energy-dark-matter/dark-energy/segregate-by-characteristics.html) - e.g. resource requirements to improve scalability, their availability requirements to improve availability, their security requirements to improve security, etc.

There are five [dark matter forces](/post/microservices/2021/11/30/dark-matter-dark-energy.html):

* [Simple interactions](/articles/dark-energy-dark-matter/dark-matter/simple-interactions.html) - an operation that’s local to a component or consists of a few simple interactions between components is easier to understand and troubleshoot than a distributed operation, especially one consisting of complex interactions
* [Efficient interactions](/articles/dark-energy-dark-matter/dark-matter/efficient-interactions.html) - a distributed operation that involves lots of network round trips and large data transfers can be too inefficient
* [Prefer ACID over BASE](/articles/dark-energy-dark-matter/dark-matter/prefer-acid-over-base.html) - it’s easier to implement an operation as an ACID transaction rather than, for example, eventually consistent sagas
* [Minimize runtime coupling](/articles/dark-energy-dark-matter/dark-matter/minimize-runtime-coupling.html) - to maximize the availability and reduce the latency of an operation
* [Minimize design time coupling](/articles/dark-energy-dark-matter/dark-matter/minimize-design-time-coupling.html) - reduce the likelihood of changing services in lockstep, which reduces productivity

Solution
--------

Design an architecture that structures the application as a set of two or more [independently deployable](/post/architecture/2022/05/04/microservice-architecture-essentials-deployability.html), [loosely coupled](/post/architecture/2023/03/28/microservice-architecture-essentials-loose-coupling.html), [components, a.k.a. services](/post/microservices/general/2019/02/16/whats-a-service-part-1.html).
Each service consists of one or more subdomains.
Each subdomain is part of a single service except for shared library subdomains that are used by multiple services.
A service is owned by the team (or teams) that owns the (non-library) subdomains.

![](/i/posts/microservices-teams-subdomains.png)

An [API gateway](/patterns/apigateway.html) is typically the application’s entry point.
Some system operations will be local to a single service, while others will be distributed across multiple services.
A distributed system operation is implemented using the [service collaboration patterns](/post/patterns/2023/07/29/service-collaboration-patterns.html).

In order to be independently deployable each service typically has its own source code repository and its own deployment pipeline, which builds, tests and deploys the service.

Examples
--------

### Fictitious e-commerce application

Let’s imagine that you are building an e-commerce application that takes orders from customers, verifies inventory and available credit, and ships them.
The application consists of several components including the StoreFrontUI, which implements the user interface, along with some backend services for checking credit,
maintaining inventory and shipping orders.
The application consists of a set of services.

![](/i/Microservice_Architecture.png)

### Show me the code

Please see the [example applications developed by Chris Richardson](http://eventuate.io/exampleapps.html).
These examples on Github illustrate various aspects of the microservice architecture.

Resulting context
-----------------

### Benefits

This solution has a number of benefits:

* Simple services - each service consists of a small number of subdomains - possibly just one - and so is easier to understand and maintain
* Team autonomy - a team can develop, test and deploy their service independently of other teams
* Fast deployment pipeline - each service is fast to test since it’s relatively small, and can be deployed independently
* Support multiple technology stacks - different services can use different technology stacks and can be upgraded independently
* Segregate subdomains by their characteristics - subdomains can be segregated by their characteristics into separate services in order to improve scalability, availability, security etc

### Drawbacks

This solution has a number of (**potential**) drawbacks:

* Some distributed operations might be complex, and difficult to understand and troubleshoot
* Some distributed operations might be potentially inefficient
* Some operations might need to be implemented using complex, eventually consistent (non-ACID) transaction management since loose coupling requires each [service to have its own database](/patterns/data/database-per-service.html).
* Some distributed operations might involve tight runtime coupling between services, which reduces their availability.
* Risk of tight design-time coupling between services, which requires time consuming lockstep changes

### Issues

There are many issues that you must address when designing an architecture.

#### Designing a good (monolithic or microservice) architecture with Assemblage

There are two key issues that you must address.
The first issue is whether to use the monolithic or microservice architecture.
And then, if you choose to use the microservice architecture, the next key challenge is to define a good [service architecture](/post/architecture/2023/09/19/assemblage-part-3-whats-a-service-architecture.html).
You must avoid (or at least minimize) the potential drawbacks: complex, inefficient interactions; complex eventually consistent transactions; and tight runtime coupling.

[Assemblage](/post/architecture/2023/02/09/assemblage-architecture-definition-process.html), is an architecture definition process that uses the [dark energy and dark matter forces](/post/architecture/2023/03/26/dark-energy-dark-matter-force-descriptions.html) to group the subdomains in a way that results in good microservice architecture.

[![](/i/posts/assemblage-overview/Defining_Microservice_Architecture_V2.png)](/post/architecture/2023/02/09/assemblage-architecture-definition-process.html)

The result of applying Assemblage is either a monolithic architecture or a microservice architecture.

The [dark energy and dark matter forces](/post/architecture/2023/03/26/dark-energy-dark-matter-force-descriptions.html) play a major role in shaping the service architecture and also heavily influence the design of the distributed operations mentioned below.

[![](/i/posts/dark-energy-dark-matter/Dark_Energy_Dark_Matter_overview.png)](/post/architecture/2023/03/26/dark-energy-dark-matter-force-descriptions.html)

#### Designing distributed operations

Another key design challenge when using microservices, is implementing distributed operations, which span multiple services.
This is especially challenging since each [service has its own database](/patterns/data/database-per-service.html).
The solution is to use the [service collaboration patterns](/post/patterns/2023/07/29/service-collaboration-patterns.html), which implement distributed operations as a series of local transactions:

[![](/i/patterns/data/service-collaboration-patterns.png)](/post/patterns/2023/07/29/service-collaboration-patterns.html)

There are four service collaboration patterns:

* [Saga](/patterns/data/saga.html), which implements a distributed command as a series of local transactions
* [Command-side replica](/patterns/data/cqrs.html), which replicas read-only data to the service that implements a command
* [API composition](/patterns/data/api-composition.html), which implements a distributed query as a series of local queries
* [CQRS](/patterns/data/cqrs.html), which implements a distributed query as a series of local queries

The Saga, Command-side replica and CQRS patterns use asynchronous messaging.
Services typically need to use the [Transaction Outbox pattern](/patterns/data/transactional-outbox.html) to atomically update persistent business entities and send a message.

Related patterns
----------------

There are many patterns related to the Microservices architecture pattern. The [Monolithic architecture](monolithic.html) is an alternative to the microservice architecture.
The other patterns in the Microservice architecture architecture pattern address issues that you will encounter when applying this pattern.



![](../i/PatternsRelatedToMicroservices.jpg)

* Sservice collaboration patterns:
  + [Saga](/patterns/data/saga.html), which implements a distributed command as a series of local transactions
  + [Command-side replica](/patterns/data/cqrs.html), which replicas read-only data to the service that implements a command
  + [API composition](/patterns/data/api-composition.html), which implements a distributed query as a series of local queries
  + [CQRS](/patterns/data/cqrs.html), which implements a distributed query as a series of local queries
* The [Messaging](/patterns/communication-style/messaging.html) and [Remote Procedure Invocation](/patterns/communication-style/rpi.html) patterns are two different ways that services can communicate.
* The [Database per Service pattern](data/database-per-service.html) describes how each service has its own database in order to ensure loose coupling.
* The [API Gateway pattern](apigateway.html) defines how clients access the services in a microservice architecture.
* The [Client-side Discovery](client-side-discovery.html) and [Server-side Discovery](server-side-discovery.html) patterns are used to route requests for a client to an available service instance in a microservice architecture.
* Testing patterns: [Service Component Test](testing/service-component-test.html) and [Service Integration Contract Test](testing/service-integration-contract-test.html)
* [Circuit Breaker](/patterns/reliability/circuit-breaker.html)
* [Access Token](/patterns/security/access-token.html)
* Observability patterns:
  + [Log aggregation](/patterns/observability/application-logging.html)
  + [Application metrics](/patterns/observability/application-metrics.html)
  + [Audit logging](/patterns/observability/audit-logging.html)
  + [Distributed tracing](/patterns/observability/distributed-tracing.html)
  + [Exception tracking](/patterns/observability/exception-tracking.html)
  + [Health check API](/patterns/observability/health-check-api.html)
  + [Log deployments and changes](/patterns/observability/log-deployments-and-changes.html)
* UI patterns:
  + [Server-side page fragment composition](/patterns/ui/server-side-page-fragment-composition.html)
  + [Client-side UI composition](/patterns/ui/client-side-ui-composition.html)
* The [Single Service per Host](deployment/single-service-per-host.html) and [Multiple Services per Host](deployment/multiple-services-per-host.html) patterns are two different deployment strategies.
* Cross-cutting concerns patterns: [Microservice chassis pattern](/patterns/microservice-chassis.html) and [Externalized configuration](/patterns/externalized-configuration.html)

Known uses
----------

Most large scale web sites including [Netflix](http://techblog.netflix.com/), [Amazon](http://highscalability.com/blog/2007/9/18/amazon-architecture.html)
and [eBay](http://www.addsimplicity.com/downloads/eBaySDForum2006-11-29.pdf) have evolved from a monolithic architecture to a microservice architecture.

Netflix, which is a very popular video streaming service that’s responsible for up to 30% of Internet traffic, has a large scale, service-oriented architecture.
They handle over a billion calls per day to their video streaming API from over 800 different kinds of devices.
Each API call fans out to an average of six calls to backend services.

Amazon.com originally had a two-tier architecture.
In order to scale they migrated to a service-oriented architecture consisting of hundreds of backend services.
Several applications call these services including the applications that implement the Amazon.com website and the web service API.
The Amazon.com website application calls 100-150 services to get the data that used to build a web page.

The auction site ebay.com also evolved from a monolithic architecture to a service-oriented architecture.
The application tier consists of multiple independent applications.
Each application implements the business logic for a specific function area such as buying or selling.
Each application uses X-axis splits and some applications such as search use Z-axis splits.
Ebay.com also applies a combination of X-, Y- and Z-style scaling to the database tier.

There are [numerous other examples](../articles/whoisusingmicroservices.html) of companies using the microservice architecture.

Examples
========

Chris Richardson has [examples](http://eventuate.io/exampleapps.html) of microservices-based applications.

See also
========

* [Jfokus 2020 - Cubes, Hexagons, Triangles, and More - Understanding Microservices](/microservices/2020/02/04/jfokus-geometry-of-microservices.html) - provides a good introduction to the microservice architecture.
* [Microservices patterns](/book)

---


[pattern](/tags/pattern) 

[application architecture](/tags/application architecture) 

[microservice architecture](/tags/microservice architecture) 
  


---

---

[Tweet](https://twitter.com/share)

[Follow @crichardson](https://twitter.com/crichardson)

Copyright © 2025 Chris Richardson • All rights reserved • Supported by [Kong](https://konghq.com/).

#### About Microservices.io

![](https://gravatar.com/avatar/a290a8643359e2495e1c6312e662012f)

Microservices.io is brought to you by [Chris Richardson](/about.html).
Experienced software architect, author of POJOs in Action, the creator of the original CloudFoundry.com, and the author of Microservices patterns.

#### ASK CHRIS

?

Got a question about microservices?

Fill in [this form](https://forms.gle/ppYDAF1JxHGec8Kn9). If I can, I'll write a blog post that answers your question.

#### NEED HELP?

![](/i/posts/cxo-wondering.webp)

I help organizations improve agility and competitiveness through better software architecture.

Learn more about my [consulting engagements](https://chrisrichardson.net/consulting.html), and [training workshops](https://chrisrichardson.net/training.html).

#### PREMIUM CONTENT

![](/i/posts/premium-logo.png)
Premium content now available for paid subscribers at [premium.microservices.io](https://premium.microservices.io).

#### MICROSERVICES WORKSHOPS

![](/i/workshop-kata_small.jpg)

Chris teaches [comprehensive workshops](http://chrisrichardson.net/training.html) for architects and developers that will enable your organization use microservices effectively.

Avoid the pitfalls of adopting microservices and learn essential topics, such as service decomposition and design and how to refactor a monolith to microservices.

[Learn more](http://chrisrichardson.net/training.html)

#### Remote consulting session

![](/i/posts/zoom-consulting.webp)

Got a specific microservice architecture-related question? For example:

* Wondering whether your organization should adopt microservices?
* Want to know how to migrate your monolith to microservices?
* Facing a tricky microservice architecture design problem?

Consider signing up for a [two hour, highly focussed, consulting session.](https://chrisrichardson.net/consulting-office-hours.html)

#### ASSESS your architecture

Assess your application's microservice architecture and identify what needs to be improved. [Engage Chris](http://www.chrisrichardson.net/consulting.html) to conduct an architect review.

#### LEARN about microservices

Chris offers numerous other resources for learning the microservice architecture.

#### Get the book: Microservices Patterns

Read Chris Richardson's book:
[![](/i/Microservices-Patterns-Cover-published.png)](/book)

---

#### Example microservices applications

Want to see an example? Check out Chris Richardson's example applications.
[See code](http://eventuate.io/exampleapps.html)

#### Virtual bootcamp: Distributed data patterns in a microservice architecture

![](/i/Chris_Speaking_Mucon_2018_a.jpg)

My virtual bootcamp, distributed data patterns in a microservice architecture, is now open for enrollment!

It covers the key distributed data management patterns including Saga, API Composition, and CQRS.

It consists of video lectures, code labs, and a weekly ask-me-anything video conference repeated in multiple timezones.

The regular price is $395/person but use coupon JIBFGJFJ to sign up for $95 (valid until May 16th, 2025).
There are deeper discounts for buying multiple seats.

[Learn more](https://chrisrichardson.net/virtual-bootcamp-distributed-data-management.html)

#### Learn how to create a service template and microservice chassis

Take a look at my [Manning LiveProject](/post/patterns/2022/03/15/service-template-chassis-live-project.html) that teaches you how to develop a service template and microservice chassis.

![](/i/patterns/microservice-template-and-chassis/Microservice_chassis.png)

[Signup for the newsletter](http://visitor.r20.constantcontact.com/d.jsp?llr=ula8akwab&p=oi&m=1123470377332&sit=l6ktajjkb&f=15d9bba9-b33d-491f-b874-73a41bba8a76)

For Email Marketing you can trust.

#### BUILD microservices

Ready to start using the microservice architecture?

#### Consulting services

[Engage Chris](http://www.chrisrichardson.net/consulting.html) to create a microservices adoption roadmap and help you define your microservice architecture,

---

#### The Eventuate platform

Use the [Eventuate.io platform](https://eventuate.io) to tackle distributed data management challenges in your microservices architecture.

[![](https://eventuate.io/i/logo.gif)](https://eventuate.io)

Eventuate is Chris's latest startup. It makes it easy to use the Saga pattern to manage transactions and the CQRS pattern to implement queries.



---

Join the [microservices google group](https://groups.google.com/forum/#!forum/microservices)

Please enable JavaScript to view the [comments powered by Disqus.](https://disqus.com/?ref_noscript)