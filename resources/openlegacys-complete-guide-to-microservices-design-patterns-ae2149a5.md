# OpenLegacy's Complete Guide to Microservices Design Patterns

Source: https://www.openlegacy.com/blog/microservices-architecture-patterns/

## Identified Architecture Patterns

### Agent Coordination

- They must also ensure coordination between services.

### Agent Task Allocation

- * **Load balancing**: The architecture can distribute incoming traffic evenly across servers.

### Agent Failure Handling

- * **Fault tolerance**: The system continues to function even if one or more services fail, ensuring a consistent user experience.
- At the same time, each service can still function autonomously, increasing data security and fault tolerance.
- * **Resilience**: If one service goes down, it doesn't affect the other services.

### Layered Architecture

- This separation of concerns allows the software development team to adapt models that are more manageable and offer greater flexibility.

### Microservices

- # OpenLegacy's Complete Guide to Microservices Design Patterns

Source: https://www.openlegacy.com/blog/microservices-architecture-patterns/

[Skip to main content](#main-content)

![blog_banner](https://462636.fs1.hubspotusercontent-na1.net/hubfs/462636/solutions_banner_bg.jpg)

Blog

Microservices design patterns are used in software development to fulfill different scenarios.
- ![img-54612334](https://462636.fs1.hubspotusercontent-na1.net/hub/462636/hubfs/img-54612334.png?width=1073&height=913&name=img-54612334.png)

An In-Depth Guide to Microservices Design Patterns
==================================================

Posted by [Angela Davis](https://www.openlegacy.com/blog/author/angela-davis) on December 28, 2023

Listen to audio version

23:40

[![icon](https://www.openlegacy.com/hubfs/2023/facebook.svg)](http://www.facebook.com/sharer.php?u=https://www.openlegacy.com/blog/microservices-architecture-patterns/)
[![icon](https://www.openlegacy.com/hubfs/2023/twitter.svg)](https://twitter.com/share?url=https://www.openlegacy.com/blog/microservices-architecture-patterns/&text=An%20In-Depth%20Guide%20to%20Microservices%20Design%20Patterns)
[![icon](https://www.openlegacy.com/hubfs/2023/linkedin.svg)](http://www.linkedin.com/shareArticle?mini=true&url=https://www.openlegacy.com/blog/microservices-architecture-patterns/)

Microservices design patterns are created to mitigate the challenges of microservice architectures.
- By breaking applications down into small autonomous services, microservices enable greater flexibility, innovation, and performance than monolithic legacy systems.

### Event Driven

- It’s often used alongside the event sourcing pattern.
- ### Event sourcing pattern

When dealing with requests, microservices need to exchange data.
- With event sourcing, any state-changing (or significant) events can be stored in place of entities.

### Data Storage

- By breaking applications down into small autonomous services, microservices enable greater flexibility, innovation, and performance than monolithic legacy systems.
- Observability patterns support the monitoring of applications, often in real time, which is essential for detecting faults and improving performance.
- This prevents overloads and improves performance.

### Api Design

- Common synchronous technology used includes API REST-based tech or gRPC.
- ### Integration patterns

The most commonly used microservices design patterns for integration are API Gateway and Backend for Frontend.
- ### API gateway

The API gateway microservices pattern is designed to solve the problems that can be caused by decomposing an application into separate services.

### Api Security

- It can also offload the responsibility for microservices’ authentication and authorization.

### Integration

- For example, integration patterns help to reduce complexity and improve service management.
- ### Integration patterns

The most commonly used microservices design patterns for integration are API Gateway and Backend for Frontend.

### Security

- It can also offload the responsibility for microservices’ authentication and authorization.

### Scalability

- * **Load balancing**: The architecture can distribute incoming traffic evenly across servers.


---

[Skip to main content](#main-content)

![blog_banner](https://462636.fs1.hubspotusercontent-na1.net/hubfs/462636/solutions_banner_bg.jpg)

Blog

Microservices design patterns are used in software development to fulfill different scenarios. We explain how they work and explore common examples.

![img-54612334](https://462636.fs1.hubspotusercontent-na1.net/hub/462636/hubfs/img-54612334.png?width=1073&height=913&name=img-54612334.png)

An In-Depth Guide to Microservices Design Patterns
==================================================

Posted by [Angela Davis](https://www.openlegacy.com/blog/author/angela-davis) on December 28, 2023

Listen to audio version

23:40

[![icon](https://www.openlegacy.com/hubfs/2023/facebook.svg)](http://www.facebook.com/sharer.php?u=https://www.openlegacy.com/blog/microservices-architecture-patterns/)
[![icon](https://www.openlegacy.com/hubfs/2023/twitter.svg)](https://twitter.com/share?url=https://www.openlegacy.com/blog/microservices-architecture-patterns/&text=An%20In-Depth%20Guide%20to%20Microservices%20Design%20Patterns)
[![icon](https://www.openlegacy.com/hubfs/2023/linkedin.svg)](http://www.linkedin.com/shareArticle?mini=true&url=https://www.openlegacy.com/blog/microservices-architecture-patterns/)

Microservices design patterns are created to mitigate the challenges of microservice architectures.

By breaking applications down into small autonomous services, microservices enable greater flexibility, innovation, and performance than monolithic legacy systems. However, they can also increase the risks of overcomplicated infrastructures and inconsistencies in data between services.

Understanding the most common microservices design patterns, as well as how and when to use them, is the best way to help reduce these risks. So, let’s take a closer look.

What are microservice design patterns?
--------------------------------------

Microservices design patterns are software patterns that generate reusable autonomous services. The aim is to allow developers who use [microservices](/product/microservices) to speed up application releases by letting teams deploy each microservice independently as needed.

There are numerous design patterns for microservices to choose from, each with specific advantages and drawbacks, and the best pattern (or patterns) to use will depend on business needs and other related factors.

This graphic demonstrates various design patterns for microservices:

![The main design patterns for microservices.](https://www.openlegacy.com/hs-fs/hubfs/Picture1-3.webp?width=567&height=565&name=Picture1-3.webp)

[Image source](https://medium.com/@madhukaudantha/microservice-architecture-and-design-patterns-for-microservices-e0e5013fd58a)

In this graphic, the different patterns are grouped according to their function. For instance, decomposition patterns help decompose applications into smaller, more manageable services. Observability patterns support the monitoring of applications, often in real time, which is essential for detecting faults and improving performance.

Understanding microservices patterns
------------------------------------

To understand the use of design patterns in microservices, you first need to understand the underlying principles of microservices design architecture. These are:

* **Autonomy**: Each service operates autonomously, eliminating the problems caused by interdependency. This also allows greater deployment flexibility.
* **Scalability**: Services can scale up or down instantly in response to demand, optimizing resource allocation and cost.
* **Resilience**: If one service goes down, it doesn't affect the other services. The software can also recover from failures more rapidly.
* **Decentralization**: Development teams can work independently, accelerating time-to-market and improving productivity.
* **Load balancing**: The architecture can distribute incoming traffic evenly across servers. This prevents overloads and improves performance.
* **DevOps integration**: By integrating DevOps into microservices architecture, you can ensure rapid delivery of high-quality services.
* **Continuous monitoring**: Real-time monitoring tools ensure the highest levels of performance, security, and availability.
* **Fault tolerance**: The system continues to function even if one or more services fail, ensuring a consistent user experience.

With the right microservice patterns and best practices, you can successfully implement microservices architecture and enjoy the benefits it provides.

Benefits of using microservices architecture patterns
-----------------------------------------------------

Microservices architecture design patterns are essential for achieving the benefits of microservices infrastructure.

For instance, design patterns enable the rapid scaling of services by ensuring they can be easily duplicated and distributed where needed. They also simplify the management of distributed data and streamline communication between services.

Design patterns also address many of the challenges associated with microservices architecture. For example, integration patterns help to reduce complexity and improve service management. At the same time, each service can still function autonomously, increasing data security and fault tolerance.

Exploring microservices architecture examples
---------------------------------------------

Let’s now look at some of the most common examples of microservices design patterns and when they should be used by developers.

### Integration patterns

The most commonly used microservices design patterns for integration are API Gateway and Backend for Frontend.

### API gateway

The API gateway microservices pattern is designed to solve the problems that can be caused by decomposing an application into separate services. These can include issues with requesting information from multiple microservices or handling several protocol requests simultaneously.

The API gateway design pattern can be considered a proxy service. It acts as the entry point for all microservices and routes a request to the correct service or services. The results can then be sent back to the composite or consumer service. By using an API gateway, microservices can communicate with each other via a stateless server, for example using either HTTP requests or a message bus.

![A graphic depicting a single API Gateway design pattern.](https://www.openlegacy.com/hs-fs/hubfs/Using%20a%20Single%20API%20Gateway.png?width=512&height=288&name=Using%20a%20Single%20API%20Gateway.png)

[Image source](https://jstobigdata.com/architecture/the-api-gateway-pattern-in-microservices/)

In addition, a microservices API gateway can expose the APIs specific to each client service and create a more tailored user experience. It can also offload the responsibility for microservices’ authentication and authorization. In this way, it can provide an extra layer of security for your sensitive data.

The downside of this pattern is that it adds an extra layer of complexity to the system. However, this is mitigated by the fact you can move some of the logic from the client application to the gateway. This simplifies the client application and reduces the number of requests to your backend systems.

### Backend for frontend

Backend for frontend, also known as BFF, is a variant of the API gateway design pattern that provides an extra layer between client applications and microservices.

Unlike the API gateway pattern, BFF isn’t a single point of entry. Instead, it introduces a separate gateway for each client. With this approach, you can add an API tailored to specific requirements.

For example, a company might have a web application, a mobile application, and a third-party application. With the BFF pattern, a separate API can be added for each app instead of a single bloated API being used for all three. This not only improves user experience but also enhances system performance as each app can call the backend in parallel.

A BFF approach provides extensive business capabilities and is ideal for the continuous delivery of microservice architecture on a large scale. This pattern can also be used to accommodate the functions of particularly complex apps or create separate gateways for different business domains.

Developers often like this model as it’s flexible and can be used to respond to most microservice situations. However, this doesn’t mean every microservices-based architecture should use a BFF pattern. After all, the more complexities there are in the design, the more setup you require.

### Cross-cutting concern patterns

Although microservices aim to allow applications to operate independently, there can still be issues with cross-cutting concerns. Microservice design patterns like blue-green deployment, the circuit breaker pattern, and service discovery can help mitigate these concerns.

### Blue-green deployment

A blue-green deployment strategy can reduce the risks of latency and downtime caused by multiple microservices falling under the umbrella of one application.

This pattern involves always running two identical production environments: blue and green. Only one of these environments is live at any time, serving all production traffic. When a developer is ready to upload a new version of the service, they can upload it to the inactive environment. This way, developers can perform any necessary tests without disrupting service.

Once the software is ready, the live environment is switched to the new version. The old version becomes inactive but remains operational. If the new version experiences any problems, the service can be switched back to the older version.

Many, if not all, [cloud-native architecture](/blog/what-is-cloud-native-architecture) platforms provide options for implementing blue-green deployment. This is beneficial as the pattern is a great way to reduce downtime and increase the resilience of microservices architecture.

![In this image, green is the live code version and blue is the new version of the application. ](https://www.openlegacy.com/hs-fs/hubfs/User%20Traffic.png?width=512&height=303&name=User%20Traffic.png)

[Image source](https://dev.to/mostlyjason/intro-to-deployment-strategies-blue-green-canary-and-more-3a3)

### Circuit breaker pattern

Microservice architectures involve a lot of calls between applications and services. If a service has failed, the unanswered calls can use up important resources and create a cascade of failures across the system. The circuit breaker pattern provides protection against this possibility.

Inspired by electrical circuit breakers, this microservice design pattern breaks the connection to failed services. Any calls to the breaker are routed to a different service or result in an error default message, preventing protected calls from being made and left ‘hanging’. This happens for a set ‘timeout’ period.

Once the circuit breaker’s timeout period is over, it will allow a small number of requests through again. If these are successful, the service will resume its normal functioning. However, if there is another failure, the timeout period will begin again.

This pattern can improve availability and performance by preventing network resources from becoming depleted. However, it is important to balance preventing failures and maintaining service levels.

### Service discovery

When it comes to container technology, IP addresses are allocated to service instances. This means each time an address changes, consumer services may break and will require manual adjustments.

A service database, known as the Service Registry, is created to store the metadata for each producer service and specification. A service instance should register to the Service Registry when starting and also de-register if shutting down.

There are two types of service discovery, each with pros and cons:

* **Client-side:** the client queries the Service Registry directly to find the location of a service instance. This model reduces the number of network hops needed. However, you must implement service discovery logic separately for each language or framework your application uses, increasing the complexity of the client code.
* **Server-side**: the client queries the Service Registry indirectly via a load balancer. In this model, the client code is simpler, but there are more moving parts to maintain and monitor. More network hops are also needed, which may introduce latency.

### Data management patterns

Since each microservice is autonomous, each service has a separate database. This can create problems if applications need to call more than one service. To manage data effectively, you need to implement one or more data management design patterns.

### CQRS design pattern

The command query responsibility segregation (CQRS) pattern can be useful if you have a large application reading data from an event store. It’s often used alongside the event sourcing pattern.

The CQRS pattern separates the ‘read’ and ‘update’ operations. This separation of concerns allows the software development team to adapt models that are more manageable and offer greater flexibility. The flexible nature of this design pattern can also be beneficial for systems that evolve over time.

A CQRS implementation can enhance microservice application performance, security, and scalability. It’s preferable in cases where the number of data reads is greater than the number of data writes. It’s also effective in scaling the read model separately.

However, developers should be mindful that the CQRS pattern has the potential for code duplication, which can introduce redundancies and add complexity.

### Event sourcing pattern

When dealing with requests, microservices need to exchange data. For stable, highly scalable systems, they should communicate asynchronously by exchanging ‘events’.

In some conventional databases, the business entity with the current ‘state’ is directly stored. With event sourcing, any state-changing (or significant) events can be stored in place of entities. This means changes are saved as a series of immutable events.

The state of a business entity can be deducted by reclaiming all the events in it. Different services can replay events from the event store to determine the correct state of their individual data stores (since data is stored as a series of events rather than by making direct updates to stores).

This pattern enables each service to maintain consistency without having to communicate synchronously. Developers can also query events to track changes and make any necessary adjustments to the application’s state.

### Saga design pattern

One of the biggest problems with microservices architecture is how to work around transactions that span multiple services. The saga pattern can help with this.

Saga allows developers to manage eCommerce transactions across multiple microservices using a sequence of local transactions. Each of these is accompanied by an event that will trigger the next stage.

As part of this approach, if one transaction fails, a rollback transaction is triggered to compensate.

The downside of this pattern is that it requires a more complex programming model. Developers must design rollback transactions to undo the change that caused a failure. They must also ensure coordination between services.

![A graphic depicting the SAGA pattern for microservices distributed transactions.](https://www.openlegacy.com/hs-fs/hubfs/SAGA%20Pattern.jpeg?width=512&height=249&name=SAGA%20Pattern.jpeg)

[Image source](https://medium.com/design-microservices-architecture-with-patterns/saga-pattern-for-microservices-distributed-transactions-7e95d0613345)

### Observability patterns

As we’ve mentioned previously, continuous monitoring is one of the cornerstones of microservices architecture. Observability patterns like the ones below can help you achieve this.

### Distributed tracing

Microservices are the intersection of [DevOps and legacy IT](/blog/microservices-the-intersection-of-devops-and-legacy-it). In a microservice architecture, requests may span multiple services. Each service deals with a client request by performing one or more operations across multiple services. This can make troubleshooting difficult, as it’s hard to track end-to-end requests.

Distributed tracing is one solution to this problem. With this pattern, a distributed tracer gives each request a unique ID. It also records information about the requests, such as which services are called and which operations are performed.

Developers can use this information to trace requests from beginning to end, helping them find the root cause of any issues. They can also monitor how services interact and how long it takes each service to process requests, which is useful for pinpointing latency.

![A graphic depicting a distributed tracing microservices design pattern.](https://www.openlegacy.com/hs-fs/hubfs/Distributed%20tracing.png?width=512&height=249&name=Distributed%20tracing.png)

[Image source](https://www.simform.com/blog/observability-design-patterns-for-microservices/)

### Log aggregation

Each microservice generates a standardized log file about its activities. This can be useful in cases where an application may consist of several services. Requests often require multiple service instances.

However, there needs to be a centralized logging service that can compile logs from each service instance. This is where log aggregation comes in: it normalizes and consolidates logs from different microservices and stores them on a centralized platform.

Developers can search and analyze logs on the platform. They can also create alerts that are triggered when certain problem messages appear, simplifying issue resolution.

Put simply, the log aggregation design pattern is a useful monitoring and troubleshooting tool that eliminates hours of manual labor.

### Performance metrics

It’s important to keep an eye on transactions so that patterns can be monitored and problems identified. However, the increased service portfolio of microservices architectures can make this difficult.

With the performance metrics pattern, you can gather data about individual operations (such as latency and CPU performance) and consolidate it. The pattern aggregates the metrics of different services into a single metrics service that offers reporting and altering capabilities.

This pattern provides a consolidated view of how microservices infrastructure is performing. There are two models for this: push (which pushes metrics to the metrics service) and pull (which pulls metrics from the metrics service).

### Decomposition patterns

Microservices decomposition is the process of breaking down applications into smaller independent services. This must be done logically, so it’s wise to implement one of the following decomposition design patterns.

#### By business capability

‘Business capability’ generates value for a business. The particular mix of business capabilities depends on the nature of the enterprise.

For instance, the capabilities of an online tech sales company include sales, marketing, accounting, etc. Each business capability may be thought of as a service (but one that’s business-oriented as opposed to technical).

To decompose an application into smaller services, it can be beneficial to use the business capability pattern

This pattern results in a stable microservices architecture as business capabilities are generally stable. However, its success relies on the ability to identify each specific business capability.

Users can also encounter problems with so-called ‘God Classes’, which aren’t as easy to decompose. This is because these classes are common among multiple services. For instance, the ‘order’ class can apply to order management, order delivery, order tracking, etc.

#### By subdomain

Domain-driven design (DDD) can resolve the God Class issue by using subdomains and bounded context concepts.

This pattern starts by breaking the domain model into subdomains, such as ‘core’ and ‘supporting’ activities or features. Each subdomain has a model with a scope known as the ‘bounded context’. Microservices are developed based on this.

This pattern is ideal for decomposing complex applications and supporting agile development. It’s also a great way to increase the flexibility and scalability of your architecture.

Bear in mind, though, that you need to be able to understand exactly how the business works to identify relevant subdomains. This means developers should analyze a company, including its organizational structure and areas of expertise, before acting.

#### By transactions

Another pattern involves decomposing via transactions. With this pattern, each transaction and its supporting components belong to a single microservice. For instance, you could create an order management microservice and a payment processing microservice.

This pattern solves many problems that arise when transactions span multiple services, like increased latency and complexity. This in turn can simplify the process of developing, testing, and maintaining the system.

On the other hand, this pattern has the potential for an excessive proliferation of microservices that may actually increase complexity. So, developers must carefully consider the scope of each transaction and whether decomposing with this pattern is feasible.

#### Sidecar pattern

During the sidecar pattern (also known as the sidekick pattern), components of an application are positioned in a separate processor container. This provides isolation and encapsulation, which aids fault isolation.

You can use this pattern to encapsulate an app’s supporting functions, like monitoring and configuration, or it can enable applications to be composed of heterogeneous components and technologies.

The sidecar is attached to a ‘parent application’ and provides assisting features for this. It also shares the same lifecycle as the parent since it’s created and retired alongside it.

#### Bulkhead pattern

The bulkhead pattern is so named because it resembles the sectioned partitions of a ship’s hull. It works by isolating elements of an application into separate sections. If one fails, the others can continue to function.

These partitions are created based on consumer load and availability. It helps to isolate failures, allowing you to keep a service functioning for some customers, even while others are experiencing failure.

This can be a useful pattern for businesses that receive large volumes of customers at once. It can also be combined with the circuit breaker pattern for enhanced fault isolation.

#### Vine pattern

It’s difficult to apply the patterns we’ve discussed so far to [legacy applications](/blog/legacy-systems-migration) since these applications are already live. That’s not to say cloud-based microservices can’t [support legacy systems](/blog/how-cloud-native-architectures-support-legacy-systems), you just need the right pattern.

The vine pattern, also known as the strangler pattern, resembles a vine wrapping itself around a tree. When it’s applied to web applications, a message goes back and forth for every Uniform Resource Identifier (URI) call, and the services can then be broken down into different domains. Unlike some services, these domains are hosted separately.

The two separate services can stay side by side in the same URI space, with a single domain taken into account at any one time. The new refactored app wraps around or ’strangles‘ the original app until you’re able to shut down the older, monolith application.

This pattern lets you migrate data and features gradually from the monolith to the new microservices without interrupting the user experience. For the duration of the [migration](/blog/legacy-systems-migration), developers should make sure both systems can access the relevant resources.

![Applying the vine or strangler microservices design pattern to web applications.](https://www.openlegacy.com/hs-fs/hubfs/Strangling%20the%20monolith.jpeg?width=512&height=384&name=Strangling%20the%20monolith.jpeg)

[Image source](https://microservices.io/patterns/refactoring/strangler-application.html)

Getting started with the principles of microservices design patterns
--------------------------------------------------------------------

To successfully get started with design patterns in microservices, it comes down to choosing the right option for each scenario. It’s not a one-size-fits-all solution, which is why there are so many patterns to pick from.

It can be beneficial to use software such as OpenLegacy to help you along the way. This solution offers enterprise developers a true end-to-end ‘API factory’ for creating digital services, which means you get the most out of your core systems without having to make drastic changes.

One major upside is that microservices design patterns can deliver a significant reduction in maintenance expenses in the long term. This should be enough to pay for the upfront costs of microservices within a few years.

Quality is also improved with OpenLegacy’s innovative approach, as microservices make for a much cleaner testing process (their simpler build makes it easier to review their code). Add to this the [90% average increase](https://explore.openlegacy.com/c/accelerating-the-dig-1?x=mGuie7&lx=Ed2Qs0#page=1) in delivered services per year when using them, and you begin to see their appeal.

---

Microservices architecture patterns FAQs
----------------------------------------

### What patterns are used in microservices?

There are many microservices architecture patterns, which each offer differing functionality. Some of the commonly used patterns explored in this article include API gateways, CQRS, blue-green deployment, event sourcing, and the saga design pattern.   

### What are the different types of microservices architecture?

There are many ways to implement different microservices’ architectural styles. [Cloud-native architectures support legacy systems](/blog/how-cloud-native-architectures-support-legacy-systems), for example. They can be used to split a complex system into smaller, manageable sub-systems.

To do this, you can use synchronous or asynchronous technology. Common synchronous technology used includes API REST-based tech or gRPC. Asynchronous technology includes messaging.

### How many design patterns are there in microservices?

Decomposition, integration, database, observability, and cross-cutting concern are the five main microservices architecture design patterns, but these can be split into many more subgroups.

All of them come under two main types of microservices patterns: client-side and server-side.

We’d love to give you a demo.
-----------------------------

Please leave us your details and we'll be in touch shortly

###








![Google Ad](//googleads.g.doubleclick.net/pagead/viewthroughconversion/966442323/?value=0&guid=ON&script=0)









![](https://px.ads.linkedin.com/collect/?pid=1986162&fmt=gif)