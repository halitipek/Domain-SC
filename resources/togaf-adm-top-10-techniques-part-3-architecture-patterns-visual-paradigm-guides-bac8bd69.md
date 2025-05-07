# TOGAF ADM: Top 10 techniques – Part 3: Architecture Patterns - Visual Paradigm Guides

Source: https://guides.visual-paradigm.com/togaf-adm-top-10-techniques-part-3-architecture-patterns/

## Identified Architecture Patterns

### Agent Task Allocation

- The key elements of the pattern include:

* Load balancing: distributing incoming requests across multiple servers to ensure that no single server is overloaded.
- Additionally, implementing load balancing and caching can add complexity to the application architecture.

### Layered Architecture

- Examples of enterprise architecture patterns include Service-Oriented Architecture (SOA), Business Process Management (BPM), and Enterprise Integration Patterns (EIP), while examples of software architecture patterns include Model-View-Controller (MVC), Microservices, and Layered Architecture.
- Some examples of software architecture patterns include Model-View-Controller (MVC), Microservices, Layered Architecture, Service-Oriented Architecture (SOA), and Event-Driven Architecture (EDA).
- Layered Architecture: This pattern divides an application into logical layers, each responsible for a specific aspect of the application’s functionality, to provide modularity and separation of concerns.

### Microservices

- Related Patterns:** Related patterns that may be useful in conjunction with the Scalable Web Application pattern include:

* Microservices architecture: breaking the application down into smaller, more manageable services that can be independently scaled.
- Examples of enterprise architecture patterns include Service-Oriented Architecture (SOA), Business Process Management (BPM), and Enterprise Integration Patterns (EIP), while examples of software architecture patterns include Model-View-Controller (MVC), Microservices, and Layered Architecture.
- Some examples of software architecture patterns include Model-View-Controller (MVC), Microservices, Layered Architecture, Service-Oriented Architecture (SOA), and Event-Driven Architecture (EDA).

### Event Driven

- Some examples of software architecture patterns include Model-View-Controller (MVC), Microservices, Layered Architecture, Service-Oriented Architecture (SOA), and Event-Driven Architecture (EDA).
- Event-Driven Architecture (EDA): This pattern emphasizes the production, detection, consumption, and reaction to events that occur within a system, enabling a more flexible and scalable architecture.

### Data Storage

- This should include information about the organization, the system or application being developed, and any relevant constraints or limitations.
- Benefits:** By using the Scalable Web Application pattern, the company can ensure that their application can handle a large number of concurrent users without experiencing performance issues or downtime.
- Implementation:** To implement the Scalable Web Application pattern, the company should consider using a load balancer such as NGINX, implementing caching using a technology like Redis or Memcached, and horizontally scaling the application using a cloud platform like AWS or Azure.

### Api Design

- * API gateway: providing a single entry point for accessing the application’s services and managing traffic.

### Api Security

- ### Example of an Architecture Pattern in the Context of Single Sign On

Here’s an example of an Architecture Pattern in the context of Single Sign-On (SSO):

![Two Factor Multi-Factor Authentication Security Concept](https://media.istockphoto.com/id/1180475665/vector/two-factor-multi-factor-authentication-security-concept.jpg?b=1&s=612x612&w=0&k=20&c=_tvIGfZMkUKe_D6R8LjogWTNNeSCMv6EMNrwGLxe76c=)

**1.
- Service Providers should be configured to rely on the IdP for authentication and authorization.
- Related Patterns:** Related patterns that may be useful in conjunction with the Single Sign-On pattern include:

* Federated Identity: extending the Single Sign-On pattern to support authentication across organizations or domains.

### Integration

- Examples of enterprise architecture patterns include Service-Oriented Architecture (SOA), Business Process Management (BPM), and Enterprise Integration Patterns (EIP), while examples of software architecture patterns include Model-View-Controller (MVC), Microservices, and Layered Architecture.

### Security

- Service Providers should be configured to rely on the IdP for authentication and authorization.
- ### Example of an Architecture Pattern in the Context of Single Sign On

Here’s an example of an Architecture Pattern in the context of Single Sign-On (SSO):

![Two Factor Multi-Factor Authentication Security Concept](https://media.istockphoto.com/id/1180475665/vector/two-factor-multi-factor-authentication-security-concept.jpg?b=1&s=612x612&w=0&k=20&c=_tvIGfZMkUKe_D6R8LjogWTNNeSCMv6EMNrwGLxe76c=)

**1.
- Related Patterns:** Related patterns that may be useful in conjunction with the Single Sign-On pattern include:

* Federated Identity: extending the Single Sign-On pattern to support authentication across organizations or domains.

### Scalability

- * Horizontal scaling: adding additional servers to the infrastructure to handle increased load.
- The key elements of the pattern include:

* Load balancing: distributing incoming requests across multiple servers to ensure that no single server is overloaded.
- Additionally, implementing load balancing and caching can add complexity to the application architecture.

### Performance

- * Caching: using in-memory caching to store frequently accessed data and reduce the load on the database.
- Additionally, implementing load balancing and caching can add complexity to the application architecture.
- Implementation:** To implement the Scalable Web Application pattern, the company should consider using a load balancer such as NGINX, implementing caching using a technology like Redis or Memcached, and horizontally scaling the application using a cloud platform like AWS or Azure.


---

**Table of Contents** 
[hide](#)

[1
What are Architecture Patterns](#What_are_Architecture_Patterns)

[1.1
Architecture Patterns in TOGAF ADM](#Architecture_Patterns_in_TOGAF_ADM)

[2
A Template for Documenting an Architecture Patterns](#A_Template_for_Documenting_an_Architecture_Patterns)

[3
An Example for Architecture Pattern in Business Context](#An_Example_for_Architecture_Pattern_in_Business_Context)

[3.1
Example of an Architecture Pattern in the Context of Single Sign On](#Example_of_an_Architecture_Pattern_in_the_Context_of_Single_Sign_On)

[3.2
Enterprise Architecture Patterns vs Software Architecture Patterns](#Enterprise_Architecture_Patterns_vs_Software_Architecture_Patterns)

[3.3
Software Architecture Patterns](#Software_Architecture_Patterns)

[4
Summary](#Summary)

In the field of enterprise architecture, Architecture Patterns are an important tool for building effective solutions to common problems. Patterns offer a way to put building blocks into context, and can provide architects with a blueprint for designing solutions that have been proven to work in the past. In this article, we explore the concept of Architecture Patterns in the context of the TOGAF ADM, and provide an example of an Architecture Pattern in the business application development context.

What are Architecture Patterns
------------------------------

A “pattern” has been defined as: “an idea that has been useful in one practical context and will probably be useful in others” (Source: Analysis Patterns – Re-usable Object Models, by M. Fowler).

In the TOGAF standard, patterns are considered to be a way of putting building blocks into context; for example, to describe a re-usable solution to a problem. Building blocks are what you use: patterns can tell you how you use them, when, why, and what trade-offs you have to make in doing so.

Patterns offer the promise of helping the architect to identify combinations of Architecture and/or Solution Building Blocks (ABBs/SBBs) that have been proven to deliver effective solutions in the past, and may provide the basis for effective solutions in the future.

Pattern techniques are generally acknowledged to have been established as a valuable architectural design technique by Christopher Alexander, a buildings architect, who described this approach in his book The Timeless Way of Building, published in 1979. This book provides an introduction to the ideas behind the use of patterns, and Alexander followed it with two further books (A Pattern Language and The Oregon Experiment) in which he expanded on his description of the features and benefits of a patterns approach to architecture.

### Architecture Patterns in TOGAF ADM

The Architecture Development Method (ADM) is a key component of the Open Group’s TOGAF standard, which provides a framework for creating and managing enterprise architecture. Within the ADM, Architecture Patterns are a powerful tool that can help architects identify proven solutions to common problems and accelerate the development of effective architectures.

At its core, an Architecture Pattern is simply a description of a re-usable solution to a problem that has been proven to work in practice. As the definition above suggests, a pattern is an idea that has been useful in one context and will likely be useful in others. Patterns can be used to describe solutions at different levels of abstraction, from high-level architecture patterns that describe the overall structure of a system to low-level design patterns that describe how individual components should be implemented.

One of the key benefits of using Architecture Patterns is that they can help architects to identify combinations of Architecture Building Blocks (ABBs) or Solution Building Blocks (SBBs) that have been proven to deliver effective solutions in the past. This can save time and effort by providing a starting point for architecture development, rather than starting from scratch with each new project.

In addition, Architecture Patterns can help to ensure that architectures are consistent and coherent. By using patterns to describe solutions to common problems, architects can create a common language and set of concepts that can be used across the organization. This can help to avoid misunderstandings and ensure that everyone is working towards a shared vision of the architecture.

Pattern techniques have been established as a valuable architectural design technique by Christopher Alexander, a buildings architect, who described this approach in his book The Timeless Way of Building. Alexander’s ideas were later expanded upon in two further books, A Pattern Language and The Oregon Experiment.

In the context of enterprise architecture, there are several different types of Architecture Patterns that can be used. Some of the most common include:

1. Reference Architectures – These describe the overall structure of a system or application, and provide a starting point for architecture development.
2. Solution Patterns – These describe how specific problems can be solved using a combination of ABBs and SBBs.
3. Process Patterns – These describe best practices and common workflows for developing and implementing architectures.
4. Design Patterns – These describe how individual components should be designed and implemented, and can help to ensure consistency and maintainability across the architecture.

Architecture Patterns are a powerful tool for architects looking to develop effective and efficient enterprise architectures. By identifying proven solutions to common problems, architects can save time and effort while ensuring that architectures are consistent, coherent, and aligned with organizational goals and objectives.

A Template  for Documenting an Architecture  Patterns
-----------------------------------------------------

**1. Pattern Name**

A descriptive name for the pattern, which should clearly communicate the problem being solved.

**2. Problem**

A description of the problem or challenge that the pattern is intended to address. This should be clear and specific, and provide context for the pattern.

**3. Context**

A description of the context in which the pattern is intended to be used. This should include information about the organization, the system or application being developed, and any relevant constraints or limitations.

**4. Solution**

A description of the solution that the pattern provides. This should be clear and specific, and explain how the pattern can be used to address the problem described in section 2.

**5. Benefits**

A description of the benefits of using the pattern. This should explain how the pattern can help to address the problem, and provide evidence to support its effectiveness.

**6. Trade-offs**

A description of any trade-offs or compromises that must be made when using the pattern. This should include any limitations or drawbacks of the pattern, and any risks that must be managed.

**7. Implementation**

A description of how the pattern can be implemented. This should include guidance on how to apply the pattern, and any relevant examples or use cases.

**8. Related Patterns**

A list of related patterns that may be useful in conjunction with the current pattern. This should include any patterns that are closely related or that may be used in combination with the current pattern.

**9. References**

A list of references and sources used in developing the pattern. This should include any relevant publications, articles, or other resources.

By using this template, architects can create clear and effective Architecture Patterns that can be easily shared and re-used across different projects and contexts.

An Example for Architecture Pattern in Business Context
-------------------------------------------------------

Let’s consider an example of an Architecture Pattern in the context of business application development.

Suppose a company needs to develop a new web-based application for managing customer relationships. One of the key challenges they face is how to ensure that the application is scalable and can handle a large number of concurrent users.

Using the Architecture Pattern template outlined above, we can create a pattern to address this problem:

**1. Pattern Name:** Scalable Web Application

**2. Problem:** Developing a web-based application for managing customer relationships that can handle a large number of concurrent users.

**3. Context:** A company needs to develop a new web-based application for managing customer relationships. The application will be accessed by a large number of users and must be scalable to handle peak usage periods.

**4. Solution:** The Scalable Web Application pattern provides a solution for developing a web-based application that can handle a large number of concurrent users. The key elements of the pattern include:

* Load balancing: distributing incoming requests across multiple servers to ensure that no single server is overloaded.
* Caching: using in-memory caching to store frequently accessed data and reduce the load on the database.
* Horizontal scaling: adding additional servers to the infrastructure to handle increased load.
* Database sharding: splitting the database into smaller partitions to distribute the load across multiple servers.

**5. Benefits:** By using the Scalable Web Application pattern, the company can ensure that their application can handle a large number of concurrent users without experiencing performance issues or downtime. This can improve customer satisfaction and increase revenue by ensuring that the application is always available.

**6. Trade-offs:** The Scalable Web Application pattern requires additional infrastructure and resources to implement, which can increase costs. Additionally, implementing load balancing and caching can add complexity to the application architecture.

**7. Implementation:** To implement the Scalable Web Application pattern, the company should consider using a load balancer such as NGINX, implementing caching using a technology like Redis or Memcached, and horizontally scaling the application using a cloud platform like AWS or Azure. Database sharding can be implemented using a database technology like MongoDB.

**8. Related Patterns:** Related patterns that may be useful in conjunction with the Scalable Web Application pattern include:

* Microservices architecture: breaking the application down into smaller, more manageable services that can be independently scaled.
* API gateway: providing a single entry point for accessing the application’s services and managing traffic.

**9. References:** Some references that may be useful in developing the Scalable Web Application pattern include:

* High Scalability ([blog](https://highscalability.com/)):
* Building Scalable Web Sites (book) by Cal Henderson

By using this Architecture Pattern, the company can save time and effort in developing a scalable web application for managing customer relationships. The pattern provides a proven solution to a common problem and can be easily adapted to meet the company’s specific needs and constraints.

### Example of an Architecture Pattern in the Context of Single Sign On

Here’s an example of an Architecture Pattern in the context of Single Sign-On (SSO):

![Two Factor Multi-Factor Authentication Security Concept](https://media.istockphoto.com/id/1180475665/vector/two-factor-multi-factor-authentication-security-concept.jpg?b=1&s=612x612&w=0&k=20&c=_tvIGfZMkUKe_D6R8LjogWTNNeSCMv6EMNrwGLxe76c=)

**1. Pattern Name:** Single Sign-On (SSO)

**2. Problem:** Multiple applications within an organization require users to authenticate separately, leading to a poor user experience and increased administrative overhead for managing user accounts.

**3. Context:** An organization has multiple applications that require users to authenticate separately, causing frustration and confusion for users. The organization wants to provide a seamless user experience by allowing users to authenticate once and access all applications without having to re-enter credentials.

**4. Solution:** The Single Sign-On pattern provides a solution for enabling users to authenticate once and access multiple applications without having to re-enter their credentials. The key elements of the pattern include:

* Identity Provider (IdP): a centralized service that authenticates users and provides tokens or assertions that can be used to access other applications.
* Service Provider (SP): an application or service that relies on the IdP to authenticate users and provides access based on the tokens or assertions provided by the IdP.
* Standard protocols: using industry-standard protocols such as SAML, OAuth, or OpenID Connect to enable communication between the IdP and SPs.

**5. Benefits:** By using the Single Sign-On pattern, the organization can provide a seamless user experience and reduce administrative overhead for managing user accounts. Users only need to authenticate once, and can then access all applications without having to remember multiple sets of credentials. This can improve user satisfaction and reduce helpdesk support costs.

**6. Trade-offs:** Implementing the Single Sign-On pattern requires additional infrastructure and resources to implement, which can increase costs. Additionally, integrating with existing applications may require custom development or configuration, which can add complexity.

**7. Implementation:** To implement the Single Sign-On pattern, the organization should select an Identity Provider that supports industry-standard protocols such as SAML, OAuth, or OpenID Connect. Service Providers should be configured to rely on the IdP for authentication and authorization. Existing applications may need to be integrated with the IdP, which may require custom development or configuration.

**8. Related Patterns:** Related patterns that may be useful in conjunction with the Single Sign-On pattern include:

* Federated Identity: extending the Single Sign-On pattern to support authentication across organizations or domains.
* Attribute-Based Access Control: using user attributes provided by the IdP to control access to resources within applications.

**9. References:** Some references that may be useful in developing the Single Sign-On pattern include:

* Single Sign-On (SSO) ([Wikipedia](https://en.wikipedia.org/wiki/Single_sign-on))
* SAML Technical Overview ([OASIS](https://www.oasis-open.org/committees/download.php/27819/sstc-saml-tech-overview-2.0-cd-02.pdf))

By using this Architecture Pattern, the organization can improve user experience and reduce administrative overhead by implementing a single sign-on solution that enables users to access multiple applications without having to re-enter credentials. The pattern provides a proven solution to a common problem and can be easily adapted to meet the organization’s specific needs and constraints.

### Enterprise Architecture Patterns vs Software Architecture Patterns

Enterprise architecture patterns and software architecture patterns are related but distinct concepts.

Software architecture patterns are focused on the design and implementation of individual software systems or applications. They provide a set of guidelines and best practices for designing and implementing the software components of a system, such as its modules, interfaces, and interactions.

Enterprise architecture patterns, on the other hand, are focused on the design and alignment of multiple software systems and applications within an organization. They provide a set of guidelines and best practices for designing and implementing the overall architecture of an enterprise, including its business processes, data structures, and technology infrastructure.

Enterprise architecture patterns typically address issues such as system integration, interoperability, and scalability, which are not typically covered by software architecture patterns. They also consider the broader business context in which software systems are deployed, and aim to align IT systems with organizational goals and objectives.

Examples of enterprise architecture patterns include Service-Oriented Architecture (SOA), Business Process Management (BPM), and Enterprise Integration Patterns (EIP), while examples of software architecture patterns include Model-View-Controller (MVC), Microservices, and Layered Architecture.

![](https://guides.visual-paradigm.com/wp-content/uploads/2023/03/img_641aacb2ea57f.png)

### Software Architecture Patterns

Software architecture patterns are reusable solutions to commonly occurring problems in software design. They provide a structured approach to designing and implementing software systems, by defining a set of rules and guidelines that help ensure the system is robust, scalable, and maintainable.

Software architecture patterns provide a high-level view of the system, identifying its key components and their interactions. They define the relationships between these components and provide a set of rules for how they should communicate and work together.

By using software architecture patterns, developers can save time and effort by reusing proven solutions to common problems, rather than starting from scratch with each new project. This can help to improve the quality of the resulting software, as well as reducing development time and costs.

Some examples of software architecture patterns include Model-View-Controller (MVC), Microservices, Layered Architecture, Service-Oriented Architecture (SOA), and Event-Driven Architecture (EDA).

Here are some popular software architecture patterns:

1. Model-View-Controller (MVC) Pattern: This pattern separates an application into three interconnected components – the Model, View, and Controller – to help manage complexity and achieve separation of concerns.
2. Microservices Architecture: This pattern breaks down an application into smaller, independently deployable services that can be developed, deployed, and scaled separately.
3. Layered Architecture: This pattern divides an application into logical layers, each responsible for a specific aspect of the application’s functionality, to provide modularity and separation of concerns.
4. Service-Oriented Architecture (SOA): This pattern is an architectural approach to building distributed systems that use services as the fundamental building blocks.
5. Event-Driven Architecture (EDA): This pattern emphasizes the production, detection, consumption, and reaction to events that occur within a system, enabling a more flexible and scalable architecture.
6. Domain-Driven Design (DDD): This pattern encourages the use of a common language and model for describing the domain of a problem, resulting in a more maintainable and understandable codebase.
7. Hexagonal Architecture: This pattern structures an application around a central core, with ports and adapters that enable communication between the core and external systems.
8. CQRS (Command Query Responsibility Segregation): This pattern separates the read and write models of an application, allowing for more efficient querying and improved scalability.
9. Reactive Architecture: This pattern is a set of design principles that aim to build resilient, scalable, and responsive systems that can react to changes in the environment.
10. Clean Architecture: This pattern emphasizes the separation of concerns between different layers of an application, with the goal of producing code that is easy to read, test, and maintain.

Summary
-------

Architecture Patterns are a valuable design technique in enterprise architecture that offer architects a way to design effective solutions to common problems. By providing a blueprint for designing solutions that have been proven to work in the past, Architecture Patterns can help architects save time and resources, while also improving the overall quality of the solution. In this article, we have provided an example of an Architecture Pattern in the business application development context, specifically in the context of Single Sign-On (SSO). By using the Single Sign-On pattern, organizations can provide a seamless user experience and reduce administrative overhead for managing user accounts, while also improving user satisfaction and reducing helpdesk support costs.

### Leave a Comment [Cancel reply](/togaf-adm-top-10-techniques-part-3-architecture-patterns/#respond)

You must be [logged in](https://guides.visual-paradigm.com/wp-login.php?redirect_to=https%3A%2F%2Fguides.visual-paradigm.com%2Ftogaf-adm-top-10-techniques-part-3-architecture-patterns%2F) to post a comment.