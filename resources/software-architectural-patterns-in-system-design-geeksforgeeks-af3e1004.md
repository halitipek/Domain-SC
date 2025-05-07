# Software Architectural Patterns in System Design | GeeksforGeeks

Source: https://www.geeksforgeeks.org/design-patterns-architecture/

## Identified Architecture Patterns

### Layered Architecture

- Table of Content

* [Layered Architecture (N-Tier Architecture)](#layered-architecture-ntier-architecture)
* [Microservices Architecture](#microservices-architecture)
* [Service-Oriented Architecture (SOA)](#serviceoriented-architecture-soa)
* [Event-Driven Architecture (EDA)](#eventdriven-architecture-eda)
* [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture-ports-and-adapters)
* [Component-Based Architecture](#componentbased-architecture)
* [Blackboard Architecture](#blackboard-architecture)
* [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
* [Serverless architecture](#serverless-architecture)
* [Circuit Breaker Pattern](#10-circuit-breaker-pattern)
* [Model-view-controller pattern](#11-modelviewcontroller-pattern)

****1.
- Layered Architecture (N-Tier Architecture)****
-----------------------------------------------------

Layered Architecture (N-Tier Architecture) is a software design pattern that structures an application into multiple distinct layers, each responsible for specific tasks or concerns.
- ![layered-architecture](https://media.geeksforgeeks.org/wp-content/uploads/20241111112011432638/layered-architecture.webp)

Layered Architecture

* ****Presentation Layer (UI)**** : This is where the user interacts with the application.

### Microservices

- Table of Content

* [Layered Architecture (N-Tier Architecture)](#layered-architecture-ntier-architecture)
* [Microservices Architecture](#microservices-architecture)
* [Service-Oriented Architecture (SOA)](#serviceoriented-architecture-soa)
* [Event-Driven Architecture (EDA)](#eventdriven-architecture-eda)
* [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture-ports-and-adapters)
* [Component-Based Architecture](#componentbased-architecture)
* [Blackboard Architecture](#blackboard-architecture)
* [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
* [Serverless architecture](#serverless-architecture)
* [Circuit Breaker Pattern](#10-circuit-breaker-pattern)
* [Model-view-controller pattern](#11-modelviewcontroller-pattern)

****1.
- Microservices Architecture****
-------------------------------------

[Microservices Architecture](https://www.geeksforgeeks.org/microservices/) is a software architectural style where an application is structured as a collection of small, independent services, each focused on a specific business function.
- ![Microservices-](https://media.geeksforgeeks.org/wp-content/uploads/20241107182512879006/Microservices-.webp)

> ****For Example:**** A e-commerce store platform may have separate microservices for account service, inventory service and shipping service.

### Event Driven

- Table of Content

* [Layered Architecture (N-Tier Architecture)](#layered-architecture-ntier-architecture)
* [Microservices Architecture](#microservices-architecture)
* [Service-Oriented Architecture (SOA)](#serviceoriented-architecture-soa)
* [Event-Driven Architecture (EDA)](#eventdriven-architecture-eda)
* [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture-ports-and-adapters)
* [Component-Based Architecture](#componentbased-architecture)
* [Blackboard Architecture](#blackboard-architecture)
* [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
* [Serverless architecture](#serverless-architecture)
* [Circuit Breaker Pattern](#10-circuit-breaker-pattern)
* [Model-view-controller pattern](#11-modelviewcontroller-pattern)

****1.
- Event-Driven Architecture (EDA)****
------------------------------------------

[Event-Driven Architecture (EDA)](https://www.geeksforgeeks.org/event-driven-architecture-system-design/) is a software design pattern where the flow of a system is driven by events.
- ![event-driven-architecture-of-e-commerce-site](https://media.geeksforgeeks.org/wp-content/uploads/20241107184127944601/event-driven-architecture-of-e-commerce-site.webp)

> ****For Example:**** In a stock trading application, when a user places an order, an ****event**** is generated.

### Serverless

- Table of Content

* [Layered Architecture (N-Tier Architecture)](#layered-architecture-ntier-architecture)
* [Microservices Architecture](#microservices-architecture)
* [Service-Oriented Architecture (SOA)](#serviceoriented-architecture-soa)
* [Event-Driven Architecture (EDA)](#eventdriven-architecture-eda)
* [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture-ports-and-adapters)
* [Component-Based Architecture](#componentbased-architecture)
* [Blackboard Architecture](#blackboard-architecture)
* [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
* [Serverless architecture](#serverless-architecture)
* [Circuit Breaker Pattern](#10-circuit-breaker-pattern)
* [Model-view-controller pattern](#11-modelviewcontroller-pattern)

****1.
- Serverless architecture****
----------------------------------

Developers can create and execute apps using [serverless architecture](https://www.geeksforgeeks.org/serverless-architectures/), a cloud computing design style, without having to worry about maintaining the supporting infrastructure.
- > ****For Example:**** In a serverless web application, user profile data is processed by cloud functions.

### Data Storage

- * ****Data Access Layer (Database) :****Data is retrieved and stored.
- > ****For Example:**** In an online e-commerce application, the ****presentation layer**** handles user interaction, the ****business logic layer**** processes orders and payments, and the ****data access layer**** manages database interactions.
- It handles user input and displays information.

### Api Design

- Each service communicates over a network to provide a unified experience, often using SOAP or RESTful web services.
- These external systems interact with the core through specific ****adapters**** (e.g., REST API, database access).

### Scalability

- Circuit Breaker Pattern
---------------------------

The [Circuit Breaker Pattern](https://www.geeksforgeeks.org/what-is-circuit-breaker-pattern-in-microservices/) is a software design pattern that helps prevent cascading failures in distributed systems.


---

Software Architectural Patterns in System Design
================================================

Last Updated : 
11 Nov, 2024

Comments

Improve

Suggest changes

Like Article

Like



Report

Design patterns and architectural styles play a crucial role in shaping the structure and behavior of software systems. Let's explore several architectural patterns and styles, each with its characteristics and suitable diagrams.

Table of Content

* [Layered Architecture (N-Tier Architecture)](#layered-architecture-ntier-architecture)
* [Microservices Architecture](#microservices-architecture)
* [Service-Oriented Architecture (SOA)](#serviceoriented-architecture-soa)
* [Event-Driven Architecture (EDA)](#eventdriven-architecture-eda)
* [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture-ports-and-adapters)
* [Component-Based Architecture](#componentbased-architecture)
* [Blackboard Architecture](#blackboard-architecture)
* [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
* [Serverless architecture](#serverless-architecture)
* [Circuit Breaker Pattern](#10-circuit-breaker-pattern)
* [Model-view-controller pattern](#11-modelviewcontroller-pattern)

****1. Layered Architecture (N-Tier Architecture)****
-----------------------------------------------------

Layered Architecture (N-Tier Architecture) is a software design pattern that structures an application into multiple distinct layers, each responsible for specific tasks or concerns. This approach helps in separating different aspects of the application into modular, manageable, and reusable components. Each layer interacts with the one directly above or below it, but layers typically don’t interact with each other directly, promoting a clear separation of concerns.

![layered-architecture](https://media.geeksforgeeks.org/wp-content/uploads/20241111112011432638/layered-architecture.webp)

Layered Architecture

* ****Presentation Layer (UI)**** : This is where the user interacts with the application. It handles user input and displays information.
* ****Application Layer (Business Logic)**** : This layer contains the core logic of the application, such as processing user requests and managing business rules.
* ****Data Access Layer (Database) :****Data is retrieved and stored. It interacts with the database, ensuring separation of data concerns.

> ****For Example:**** In an online e-commerce application, the ****presentation layer**** handles user interaction, the ****business logic layer**** processes orders and payments, and the ****data access layer**** manages database interactions. This separation allows for clear responsibilities and easier maintenance.

This separation of concerns makes the system modular and easier to maintain.

****2. Microservices Architecture****
-------------------------------------

[Microservices Architecture](https://www.geeksforgeeks.org/microservices/) is a software architectural style where an application is structured as a collection of small, independent services, each focused on a specific business function. These services are loosely coupled, meaning they can be developed, deployed, and scaled independently of one another.

![Microservices-](https://media.geeksforgeeks.org/wp-content/uploads/20241107182512879006/Microservices-.webp)

> ****For Example:**** A e-commerce store platform may have separate microservices for account service, inventory service and shipping service. Each service is independently deployable and communicates via APIs, allowing for [scalability](https://www.geeksforgeeks.org/what-is-scalability/) and flexibility.

****3. Service-Oriented Architecture (SOA)****
----------------------------------------------

[Service-Oriented Architecture (SOA)](https://www.geeksforgeeks.org/service-oriented-architecture/) is an architectural pattern where an application is designed as a collection of loosely coupled, reusable services that communicate with each other over a network. Each service in an SOA performs a specific business function or operation and can be accessed by other services or external clients. Benefits of SOA include:

* Services are modular and can be developed, updated, and maintained independently.
* You can combine existing services to create new applications, improving time-to-market and reducing development costs.
* SOA allows systems using different technologies or platforms to work together through standardized communication.

![service-oriented-architecture](https://media.geeksforgeeks.org/wp-content/uploads/20241111112056897703/service-oriented-architecture.webp)

Service-Oriented Architecture (SOA)

> ****For Example:**** A healthcare system uses SOA where services like ****patient management****, ****appointment scheduling****, and ****billing**** are designed as independent services. Each service communicates over a network to provide a unified experience, often using SOAP or RESTful web services.

****4. Event-Driven Architecture (EDA)****
------------------------------------------

[Event-Driven Architecture (EDA)](https://www.geeksforgeeks.org/event-driven-architecture-system-design/) is a software design pattern where the flow of a system is driven by events. An event represents a change in state or an occurrence that other parts of the system can react to. In this architecture, components communicate by producing and consuming events, allowing them to act independently and asynchronously. This makes the system more flexible, scalable, and responsive to real-time actions.

![event-driven-architecture-of-e-commerce-site](https://media.geeksforgeeks.org/wp-content/uploads/20241107184127944601/event-driven-architecture-of-e-commerce-site.webp)

> ****For Example:**** In a stock trading application, when a user places an order, an ****event**** is generated. This event triggers other processes such as price updates, notifications, and transaction validation, allowing the system to respond asynchronously to user actions.

****5. Hexagonal Architecture (Ports and Adapters)****
------------------------------------------------------

The Ports and Adapters pattern, another name for Hexagonal Architecture, is a software design methodology that seeks to provide loosely linked application components. Isolating an application's essential logic (the "inside") from external systems or interfaces (the "outside") is the idea. This is accomplished by drawing distinct lines between the main logic of the application and the external systems—like databases, web services, user interfaces, or messaging systems—that communicate with it.

![TerraBrasilis-Hexagonal-Architecture-Ports-and-Adapters-Design-Pattern](https://media.geeksforgeeks.org/wp-content/uploads/20231001150152/TerraBrasilis-Hexagonal-Architecture-Ports-and-Adapters-Design-Pattern.png)

> ****For Example:**** A payment gateway uses hexagonal architecture where the ****core logic**** (payment processing) remains independent of external systems like databases, UI, or third-party services. These external systems interact with the core through specific ****adapters**** (e.g., REST API, database access).

****6. Component-Based Architecture****
---------------------------------------

According to the architectural design pattern known as "[component-based architecture](https://www.geeksforgeeks.org/component-based-architecture-system-design/)," an application is constructed by putting together separate, reusable parts that each contain a particular purpose. Every component is an independent unit that carries out a specific function and provides an open interface for communication. Because these parts can be created, tested, and implemented separately, the system becomes more adaptable, scalable, and modular.

> ****For Example:**** In a web application, reusable ****components**** like a ****login form****, ****navigation bar****, and ****product listing**** are created independently and combined to form the UI. Each component encapsulates specific functionality and can be reused across different pages.

****7. Blackboard Architecture****
----------------------------------

A software design pattern known as "[Blackboard Architecture](https://www.geeksforgeeks.org/blackboard-architecture/)" involves several components (sometimes referred to as "knowledge sources") working together to solve a complex problem by progressively improving a shared data structure termed the "blackboard." While several components (or modules) contribute their knowledge and procedures to alter or improve the answer, the blackboard serves as a common repository for interim findings.

![blackboard-architecture](https://media.geeksforgeeks.org/wp-content/uploads/20241111112123600586/blackboard-architecture.webp)

Blackboard Architecture

> ****For Example****: In a medical diagnosis system, different modules (e.g., ****symptom analysis****, ****patient history****, and ****lab tests****) analyze data and contribute to a shared ****blackboard****. As new information is added, other components update the shared knowledge to refine the diagnosis.

****8. CQRS (Command Query Responsibility Segregation)****
----------------------------------------------------------

[Common Querry Responsibility Segregation](https://www.geeksforgeeks.org/cqrs-command-query-responsibility-segregation/), or CQRS, is a design pattern that divides the task of managing commands and inquiries among several components. Separating the methods for reading and publishing data is the primary goal of the CQRS architectural pattern. It separates the read and update operations on a datastore into two separate models: Queries and Commands, respectively.

![What-is-CQRS-Design-Pattern-](https://media.geeksforgeeks.org/wp-content/uploads/20241107185211709472/What-is-CQRS-Design-Pattern-.webp)

> ****For Example:**** In an online shopping app, ****Commands**** like placing an order are processed and stored in one model (write model), while ****Queries**** to fetch order details or product listings are handled by a separate read model, optimizing performance and scalability.

****9. Serverless architecture****
----------------------------------

Developers can create and execute apps using [serverless architecture](https://www.geeksforgeeks.org/serverless-architectures/), a cloud computing design style, without having to worry about maintaining the supporting infrastructure. According to this paradigm, server administration, scaling, and resource allocation are automatically handled by cloud providers (like AWS, Azure, or Google Cloud). Developers just concentrate on writing code and designing functions that are run in response to events, rather than deploying and maintaining servers.

> ****For Example:**** In a serverless web application, user profile data is processed by cloud functions. Instead of managing servers, developers write functions that execute in response to events (e.g., an HTTP request) and scale automatically with demand, reducing overhead and cost.

10. Circuit Breaker Pattern
---------------------------

The [Circuit Breaker Pattern](https://www.geeksforgeeks.org/what-is-circuit-breaker-pattern-in-microservices/) is a software design pattern that helps prevent cascading failures in distributed systems. It monitors the health of a service, and if failures reach a certain threshold, it "trips" the circuit, stopping requests to the failing service. This prevents the system from overloading the service with more requests, giving it time to recover.

![Circuit-Breaker-Pattern-](https://media.geeksforgeeks.org/wp-content/uploads/20241107190107263052/Circuit-Breaker-Pattern-.webp)

> ****For Example:****
>
> * Just like an electrical circuit breaker, when an issue is detected, the circuit "opens" to stop the flow of requests.
> * After a set time, the circuit "closes" again if the service is healthy. This allows the system to fail gracefully and recover without spreading the failure to other parts of the system.

11. Model-view-controller pattern
---------------------------------

The [Model-View-Controller (MVC) pattern](https://www.geeksforgeeks.org/mvc-design-pattern/) is a software architectural design that separates an application into three interconnected components: Model, View, and Controller. This separation helps organize code by decoupling the business logic, user interface, and user input handling, which promotes modularity, maintainability, and scalability.

![MVC-Design-Pattern-](https://media.geeksforgeeks.org/wp-content/uploads/20241107190324501324/MVC-Design-Pattern-.webp)

* ****Model****: Represents the core data and business logic of the application. It is responsible for retrieving, storing, and processing data, and updating the ****View**** when data changes.
* ****View****: The user interface (UI) component that displays the data to the user and responds to user interactions. The ****View**** is updated whenever the ****Model**** changes.
* ****Controller****: Acts as an intermediary between the ****Model**** and the ****View****. It handles user input, updates the ****Model**** accordingly, and updates the ****View**** to reflect any changes in the ****Model****.

Conclusion
----------

These architectural patterns and styles provide a framework for designing and building robust, scalable, and maintainable software systems. The choice of architecture depends on the specific requirements and constraints of your project. Each of these patterns comes with its own advantages and trade-offs, so it's important to select the one that best fits your needs.

  

Comment

More info

[Advertise with us](https://www.geeksforgeeks.org/about/contact-us/?listicles)

[Next Article](https://www.geeksforgeeks.org/architecture-patterns-for-resilient-systems/)


[Architecture Patterns for Resilient Systems](https://www.geeksforgeeks.org/architecture-patterns-for-resilient-systems/)

[T](https://www.geeksforgeeks.org/user/thewebdevjwnb/)

[thewebdevjwnb](https://www.geeksforgeeks.org/user/thewebdevjwnb/)

Follow

Improve

Article Tags :

* [Design Pattern](https://www.geeksforgeeks.org/category/design-pattern/)
* [Geeks Premier League](https://www.geeksforgeeks.org/category/geeksforgeeks-initiatives/geeks-premier-league/)
* [System Design](https://www.geeksforgeeks.org/category/system-design/)
* [Geeks Premier League 2023](https://www.geeksforgeeks.org/tag/geeks-premier-league-2023/)