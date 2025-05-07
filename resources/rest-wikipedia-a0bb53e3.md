# REST - Wikipedia

Source: https://en.wikipedia.org/wiki/REST

## Identified Architecture Patterns

### Layered Architecture

- The REST architectural style emphasises uniform [interfaces](/wiki/API "API"), independent deployment of [components](/wiki/Software_component "Software component"), the [scalability](/wiki/Scalability "Scalability") of interactions between them, and creating a [layered architecture](/wiki/Multitier_architecture "Multitier architecture") to promote [caching](/wiki/Caching "Caching") to reduce user-perceived [latency](/wiki/Latency_(engineering) "Latency (engineering)"), enforce [security](/wiki/Computer_security "Computer security"), and encapsulate [legacy systems](/wiki/Legacy_system "Legacy system").[[1]](#cite_note-Fielding-Ch5-1)

REST has been employed throughout the software industry to create [stateless](/wiki/Stateless_protocol "Stateless protocol"), reliable [web-based applications](/wiki/Web_application "Web application").

### Microservices

- There is no need for the client to be hard-coded with information regarding the structure of the server.[[11]](#cite_note-RESTfulAPI.net-11)

Classification models
---------------------

[[edit](/w/index.php?title=REST&action=edit&section=6 "Edit section: Classification models")]

Several models have been developed to help classify REST APIs according to their adherence to various principles of REST design, such as

* the [Richardson Maturity Model](/wiki/Richardson_Maturity_Model "Richardson Maturity Model")
* the Classification of HTTP-based APIs[[12]](#cite_note-12)
* the W S3 maturity model[[13]](#cite_note-13)

See also
--------

[[edit](/w/index.php?title=REST&action=edit&section=7 "Edit section: See also")]

* [Clean URL](/wiki/Clean_URL "Clean URL") – URL intended to improve the usability of a website
* [Content delivery network](/wiki/Content_delivery_network "Content delivery network") – Layer in the internet ecosystem addressing bottlenecks
* [Domain application protocol](/wiki/Domain_application_protocol "Domain application protocol") (DAP)
* [List of URI schemes](/wiki/List_of_URI_schemes "List of URI schemes") – Namespace identifier assigned by IANA
* [Microservices](/wiki/Microservices "Microservices") – Collection of loosely coupled services used to build computer applications
* [Overview of RESTful API Description Languages](/wiki/Overview_of_RESTful_API_Description_Languages "Overview of RESTful API Description Languages") – descriptions of computer network interfacesPages displaying wikidata descriptions as a fallback
* [Resource-oriented architecture](/wiki/Resource-oriented_architecture "Resource-oriented architecture") – Architectural pattern in software design
* [Resource-oriented computing](/wiki/Resource-oriented_computing "Resource-oriented computing") – Architectural pattern in software design
* [Service-oriented architecture](/wiki/Service-oriented_architecture "Service-oriented architecture") – Architectural pattern in software design
* [Web-oriented architecture](/wiki/Web-oriented_architecture "Web-oriented architecture") – Architectural pattern in software design
* [Web service](/wiki/Web_service "Web service") – Service offered between electronic devices via the internet

References
----------

[[edit](/w/index.php?title=REST&action=edit&section=8 "Edit section: References")]

1.

### Data Storage

- The REST architectural style emphasises uniform [interfaces](/wiki/API "API"), independent deployment of [components](/wiki/Software_component "Software component"), the [scalability](/wiki/Scalability "Scalability") of interactions between them, and creating a [layered architecture](/wiki/Multitier_architecture "Multitier architecture") to promote [caching](/wiki/Caching "Caching") to reduce user-perceived [latency](/wiki/Latency_(engineering) "Latency (engineering)"), enforce [security](/wiki/Computer_security "Computer security"), and encapsulate [legacy systems](/wiki/Legacy_system "Legacy system").[[1]](#cite_note-Fielding-Ch5-1)

REST has been employed throughout the software industry to create [stateless](/wiki/Stateless_protocol "Stateless protocol"), reliable [web-based applications](/wiki/Web_application "Web application").
- An application that adheres to the [REST architectural constraints](#Architectural_constraints) may be informally described as *RESTful*, although this term is more commonly associated with the design of [HTTP](/wiki/HTTP "HTTP")-based [APIs](/wiki/API "API") and what are widely considered best practices regarding the "verbs" ([HTTP methods](/wiki/Hypertext_Transfer_Protocol#Request_methods "Hypertext Transfer Protocol")) a [resource](/wiki/Web_resource "Web resource") responds to, while having little to do with REST as originally formulated—and is often even at odds with the concept.[[2]](#cite_note-2)

Principle
---------

[[edit](/w/index.php?title=REST&action=edit&section=1 "Edit section: Principle")]

The term *representational state transfer* was introduced and defined in 2000 by computer scientist [Roy Fielding](/wiki/Roy_Fielding "Roy Fielding") in his doctoral dissertation.
- This means that those identifiers can change without the need to inform the client beforehand and that client and server must be inherently [loosely coupled](/wiki/Loose_coupling "Loose coupling").

### Api Design

- # REST - Wikipedia

Source: https://en.wikipedia.org/wiki/REST

**Checked**

From Wikipedia, the free encyclopedia

This is the [latest accepted revision](/wiki/Wikipedia:Pending_changes "Wikipedia:Pending changes"), [reviewed](https://en.wikipedia.org/w/index.php?title=Special:Log&type=review&page=REST) on *5 April 2025*.
- Architectural style for client-server applications

For other uses, see [Rest (disambiguation)](/wiki/Rest_(disambiguation) "Rest (disambiguation)").
- **REST** (**Re**presentational **S**tate **T**ransfer) is a [software architectural style](/wiki/Software_architectural_style "Software architectural style") that was created to describe the design and guide the development of the architecture for the [World Wide Web](/wiki/World_Wide_Web "World Wide Web").

### Performance

- The REST architectural style emphasises uniform [interfaces](/wiki/API "API"), independent deployment of [components](/wiki/Software_component "Software component"), the [scalability](/wiki/Scalability "Scalability") of interactions between them, and creating a [layered architecture](/wiki/Multitier_architecture "Multitier architecture") to promote [caching](/wiki/Caching "Caching") to reduce user-perceived [latency](/wiki/Latency_(engineering) "Latency (engineering)"), enforce [security](/wiki/Computer_security "Computer security"), and encapsulate [legacy systems](/wiki/Legacy_system "Legacy system").[[1]](#cite_note-Fielding-Ch5-1)

REST has been employed throughout the software industry to create [stateless](/wiki/Stateless_protocol "Stateless protocol"), reliable [web-based applications](/wiki/Web_application "Web application").
- He also surveyed many existing architectural styles for network-based applications, identifying which features are shared with other styles, such as caching and client–server features, and those which are unique to REST, such as the concept of resources.
- For example, Fielding identified the embedding of session information in URIs as a violation of the constraints of REST which can negatively affect shared caching and server scalability.


---

**Checked**

From Wikipedia, the free encyclopedia

This is the [latest accepted revision](/wiki/Wikipedia:Pending_changes "Wikipedia:Pending changes"), [reviewed](https://en.wikipedia.org/w/index.php?title=Special:Log&type=review&page=REST) on *5 April 2025*.

Architectural style for client-server applications

For other uses, see [Rest (disambiguation)](/wiki/Rest_(disambiguation) "Rest (disambiguation)").

**REST** (**Re**presentational **S**tate **T**ransfer) is a [software architectural style](/wiki/Software_architectural_style "Software architectural style") that was created to describe the design and guide the development of the architecture for the [World Wide Web](/wiki/World_Wide_Web "World Wide Web"). REST defines a set of constraints for how the architecture of a distributed, [Internet](/wiki/Internet "Internet")-scale [hypermedia](/wiki/Hypermedia "Hypermedia") system, such as the Web, should behave. The REST architectural style emphasises uniform [interfaces](/wiki/API "API"), independent deployment of [components](/wiki/Software_component "Software component"), the [scalability](/wiki/Scalability "Scalability") of interactions between them, and creating a [layered architecture](/wiki/Multitier_architecture "Multitier architecture") to promote [caching](/wiki/Caching "Caching") to reduce user-perceived [latency](/wiki/Latency_(engineering) "Latency (engineering)"), enforce [security](/wiki/Computer_security "Computer security"), and encapsulate [legacy systems](/wiki/Legacy_system "Legacy system").[[1]](#cite_note-Fielding-Ch5-1)

REST has been employed throughout the software industry to create [stateless](/wiki/Stateless_protocol "Stateless protocol"), reliable [web-based applications](/wiki/Web_application "Web application"). An application that adheres to the [REST architectural constraints](#Architectural_constraints) may be informally described as *RESTful*, although this term is more commonly associated with the design of [HTTP](/wiki/HTTP "HTTP")-based [APIs](/wiki/API "API") and what are widely considered best practices regarding the "verbs" ([HTTP methods](/wiki/Hypertext_Transfer_Protocol#Request_methods "Hypertext Transfer Protocol")) a [resource](/wiki/Web_resource "Web resource") responds to, while having little to do with REST as originally formulated—and is often even at odds with the concept.[[2]](#cite_note-2)

Principle
---------

[[edit](/w/index.php?title=REST&action=edit&section=1 "Edit section: Principle")]

The term *representational state transfer* was introduced and defined in 2000 by computer scientist [Roy Fielding](/wiki/Roy_Fielding "Roy Fielding") in his doctoral dissertation. It means that a server will respond with the representation of a resource (today, it will most often be an [HTML](/wiki/HTML "HTML") document) and that resource will contain [hypermedia](/wiki/Hypermedia "Hypermedia") links that can be followed to make the state of the system change. Any such request will in turn receive the representation of a resource, and so on.

An important consequence is that the only identifier that needs to be known is the identifier of the first resource requested, and all other identifiers will be discovered. This means that those identifiers can change without the need to inform the client beforehand and that client and server must be inherently [loosely coupled](/wiki/Loose_coupling "Loose coupling").

History
-------

[[edit](/w/index.php?title=REST&action=edit&section=2 "Edit section: History")]

[![](//upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Roy_Fielding_at_OSCON_2008.jpg/250px-Roy_Fielding_at_OSCON_2008.jpg)](/wiki/File:Roy_Fielding_at_OSCON_2008.jpg)

[Roy Fielding](/wiki/Roy_Fielding "Roy Fielding") speaking at [OSCON](/wiki/O%27Reilly_Open_Source_Convention "O'Reilly Open Source Convention") 2008

The Web began to enter everyday use in 1993–1994, when [websites for general use](/wiki/List_of_websites_founded_before_1995 "List of websites founded before 1995") started to become available.[[3]](#cite_note-3) At the time, only a fragmented description existed of the Web's architecture, and there was pressure within the industry to agree on a standard for the Web interface protocols. For instance, several experimental extensions had been added to the communication protocol (HTTP) to support [proxies](/wiki/Proxy_server "Proxy server"), and more extensions were being proposed, but there was a need for a formal Web architecture with which to evaluate the impact of these changes.[[4]](#cite_note-:0-4)

The [W3C](/wiki/W3C "W3C") and [IETF](/wiki/IETF "IETF") [working groups](/wiki/Working_group#Technical_working_groups "Working group") together started work on creating formal descriptions of the Web's three primary standards: [URI](/wiki/URI "URI"), [HTTP](/wiki/HTTP "HTTP"), and [HTML](/wiki/HTML "HTML"). Roy Fielding was involved in the creation of these standards (specifically HTTP 1.0 and 1.1, and URI), and during the next six years he created the REST architectural style, testing its constraints on the Web's  [protocol standards](/wiki/Software_standard "Software standard") and using it as a means to define architectural improvements — and to identify architectural mismatches. Fielding defined REST in his 2000 PhD dissertation "Architectural Styles and the Design of Network-based Software Architectures"[[1]](#cite_note-Fielding-Ch5-1)[[5]](#cite_note-5) at [UC Irvine](/wiki/University_of_California,_Irvine "University of California, Irvine").

To create the REST architectural style, Fielding identified the requirements that apply when creating a world-wide network-based application, such as the need for a low entry barrier to enable global adoption. He also surveyed many existing architectural styles for network-based applications, identifying which features are shared with other styles, such as caching and client–server features, and those which are unique to REST, such as the concept of resources. Fielding was trying to both categorise the existing architecture of the current implementation and identify which aspects should be considered central to the behavioural and performance requirements of the Web.

By their nature, architectural styles are independent of any specific implementation, and while REST was created as part of the development of the Web standards, the implementation of the Web does not obey every constraint in the REST architectural style. Mismatches can occur due to ignorance or oversight, but the existence of the REST architectural style means that they can be identified before they become standardised. For example, Fielding identified the embedding of session information in URIs as a violation of the constraints of REST which can negatively affect shared caching and server scalability. [HTTP cookies](/wiki/HTTP_cookies "HTTP cookies") also violate REST constraints[[4]](#cite_note-:0-4) because they can become out of sync with the browser's application state, making them unreliable; they also contain opaque data that can be a concern for [privacy](/wiki/Internet_privacy "Internet privacy") and [security](/wiki/Internet_security "Internet security").

Architectural properties
------------------------

[[edit](/w/index.php?title=REST&action=edit&section=3 "Edit section: Architectural properties")]

The REST architectural style is designed for network-based applications, specifically client-server applications. But more than that, it is designed for Internet-scale usage, so the coupling between the *user agent* (client) and the *origin server* must be as [loose](/wiki/Loose_coupling "Loose coupling") as possible to facilitate large-scale adoption.

The strong decoupling of client and server together with the text-based transfer of information using a uniform addressing protocol provided the basis for meeting the requirements of the Web: [extensibility](/wiki/Extensibility "Extensibility"), anarchic scalability[[6]](#cite_note-6) and independent deployment of components, large-grain data transfer, and a low entry-barrier for content readers, content authors and developers.

[![](//upload.wikimedia.org/wikipedia/commons/thumb/9/9e/REST_information_model.svg/960px-REST_information_model.svg.png)](/wiki/File:REST_information_model.svg)

An [entity–relationship model](/wiki/Entity%E2%80%93relationship_model "Entity–relationship model") of the concepts expressed in the REST architectural style

The constraints of the REST architectural style affect the following architectural properties:[[1]](#cite_note-Fielding-Ch5-1)[[7]](#cite_note-SOA_with_REST-7)

* Performance in component interactions, which can be the dominant factor in user-perceived performance and network efficiency;[[8]](#cite_note-Fielding-Ch2-8)
* [Scalability](/wiki/Scalability "Scalability") allowing the support of large numbers of components and interactions among components;
* Simplicity of a uniform interface;
* Modifiability of components to meet changing needs (even while the application is running);
* Visibility of communication between components by service agents;
* Portability of components by moving program code with the data;
* Reliability in the resistance to failure at the system level in the presence of failures within components, connectors, or data.[[8]](#cite_note-Fielding-Ch2-8)

Architectural constraints
-------------------------

[[edit](/w/index.php?title=REST&action=edit&section=4 "Edit section: Architectural constraints")]

The REST architectural style defines six guiding constraints.[[7]](#cite_note-SOA_with_REST-7)[[9]](#cite_note-Richardson_2007-9) When these constraints are applied to the system architecture, it gains desirable [non-functional properties](/wiki/Non-functional_requirement "Non-functional requirement"), such as performance, scalability, simplicity, modifiability, visibility, portability, and reliability.[[1]](#cite_note-Fielding-Ch5-1)

The formal REST constraints are as follows:[[10]](#cite_note-10)

* Client/Server – Clients are separated from servers by a well-defined interface
* Stateless – A specific client does not consume server storage when the client is "at rest"
* Cache – Responses indicate their own cacheability
* Uniform interface
* Layered system – A client cannot ordinarily tell whether it is connected directly to the end server, or to an intermediary along the way
* Code on demand (optional) – Servers are able to temporarily extend or customize the functionality of a client by transferring logic to the client that can be executed within a standard virtual machine

### Uniform interface

[[edit](/w/index.php?title=REST&action=edit&section=5 "Edit section: Uniform interface")]

The uniform interface constraint is fundamental to the design of any RESTful system.[[1]](#cite_note-Fielding-Ch5-1) It simplifies and decouples the architecture, which enables each part to evolve independently. The four constraints for this uniform interface are:

* Resource identification in requests: Individual resources are identified in requests using [URIs](/wiki/Uniform_resource_identifier "Uniform resource identifier"). The resources themselves are conceptually separate from the representations that are returned to the client. For example, the server could send data from its database as [HTML](/wiki/HTML "HTML"), [XML](/wiki/XML "XML") or as [JSON](/wiki/JSON "JSON")—none of which are the server's internal representation.
* Resource manipulation through representations: When a client holds a representation of a resource, including any [metadata](/wiki/Metadata "Metadata") attached, it has enough information to modify or delete the resource's state.
* Self-descriptive messages: Each message includes enough information to describe how to process the message. For example, which parser to invoke can be specified by a [media type](/wiki/Media_type "Media type").[[1]](#cite_note-Fielding-Ch5-1)
* Hypermedia as the engine of application state ([HATEOAS](/wiki/HATEOAS "HATEOAS")) – Having accessed an initial URI for the REST application—analogous to a human Web user accessing the [home page](/wiki/Home_page "Home page") of a website—a REST client should then be able to use server-provided links dynamically to discover all the available resources it needs. As access proceeds, the server responds with text that includes [hyperlinks](/wiki/Hyperlink "Hyperlink") to other resources that are currently available. There is no need for the client to be hard-coded with information regarding the structure of the server.[[11]](#cite_note-RESTfulAPI.net-11)

Classification models
---------------------

[[edit](/w/index.php?title=REST&action=edit&section=6 "Edit section: Classification models")]

Several models have been developed to help classify REST APIs according to their adherence to various principles of REST design, such as

* the [Richardson Maturity Model](/wiki/Richardson_Maturity_Model "Richardson Maturity Model")
* the Classification of HTTP-based APIs[[12]](#cite_note-12)
* the W S3 maturity model[[13]](#cite_note-13)

See also
--------

[[edit](/w/index.php?title=REST&action=edit&section=7 "Edit section: See also")]

* [Clean URL](/wiki/Clean_URL "Clean URL") – URL intended to improve the usability of a website
* [Content delivery network](/wiki/Content_delivery_network "Content delivery network") – Layer in the internet ecosystem addressing bottlenecks
* [Domain application protocol](/wiki/Domain_application_protocol "Domain application protocol") (DAP)
* [List of URI schemes](/wiki/List_of_URI_schemes "List of URI schemes") – Namespace identifier assigned by IANA
* [Microservices](/wiki/Microservices "Microservices") – Collection of loosely coupled services used to build computer applications
* [Overview of RESTful API Description Languages](/wiki/Overview_of_RESTful_API_Description_Languages "Overview of RESTful API Description Languages") – descriptions of computer network interfacesPages displaying wikidata descriptions as a fallback
* [Resource-oriented architecture](/wiki/Resource-oriented_architecture "Resource-oriented architecture") – Architectural pattern in software design
* [Resource-oriented computing](/wiki/Resource-oriented_computing "Resource-oriented computing") – Architectural pattern in software design
* [Service-oriented architecture](/wiki/Service-oriented_architecture "Service-oriented architecture") – Architectural pattern in software design
* [Web-oriented architecture](/wiki/Web-oriented_architecture "Web-oriented architecture") – Architectural pattern in software design
* [Web service](/wiki/Web_service "Web service") – Service offered between electronic devices via the internet

References
----------

[[edit](/w/index.php?title=REST&action=edit&section=8 "Edit section: References")]

1. ^ [***a***](#cite_ref-Fielding-Ch5_1-0) [***b***](#cite_ref-Fielding-Ch5_1-1) [***c***](#cite_ref-Fielding-Ch5_1-2) [***d***](#cite_ref-Fielding-Ch5_1-3) [***e***](#cite_ref-Fielding-Ch5_1-4) [***f***](#cite_ref-Fielding-Ch5_1-5) Fielding, Roy Thomas (2000). ["Chapter 5: Representational State Transfer (REST)"](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm). *Architectural Styles and the Design of Network-based Software Architectures* (Ph.D.). University of California, Irvine. [Archived](https://web.archive.org/web/20210513160155/https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) from the original on 2021-05-13. Retrieved 2004-08-17.
2. **[^](#cite_ref-2)** Fielding, Roy T. (2008-10-20). ["REST APIs must be hypertext driven"](http://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven). roy.gbiv.com. [Archived](https://web.archive.org/web/20100318060707/http://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven) from the original on 2010-03-18. Retrieved 2016-07-06.
3. **[^](#cite_ref-3)** Couldry, Nick (2012). [*Media, Society, World: Social Theory and Digital Media Practice*](https://books.google.com/books?id=AcHvP9trbkAC&pg=PA2). London: Polity Press. p. 2. [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [9780745639208](/wiki/Special:BookSources/9780745639208 "Special:BookSources/9780745639208"). [Archived](https://web.archive.org/web/20240227165043/https://books.google.com/books?id=AcHvP9trbkAC&pg=PA2#v=onepage&q&f=false) from the original on 2024-02-27. Retrieved 2021-06-09.
4. ^ [***a***](#cite_ref-:0_4-0) [***b***](#cite_ref-:0_4-1) Fielding, Roy Thomas (2000). ["Chapter 6: Experience and Evaluation"](https://www.ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm). *Architectural Styles and the Design of Network-based Software Architectures* (Ph.D.). University of California, Irvine. [Archived](https://web.archive.org/web/20230326022001/https://www.ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm) from the original on 2023-03-26. Retrieved 2023-06-21.
5. **[^](#cite_ref-5)** ["Fielding discussing the definition of the REST term"](https://web.archive.org/web/20151105014201/https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/6735). groups.yahoo.com. Archived from [the original](https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/6735) on November 5, 2015. Retrieved 2017-08-08.
6. **[^](#cite_ref-6)** Fielding, Roy Thomas (2000). ["Chapter 4: Designing the Web Architecture: Problems and Insights"](https://ics.uci.edu/~fielding/pubs/dissertation/web_arch_domain.htm). *Architectural Styles and the Design of Network-based Software Architectures* (Ph.D.). University of California, Irvine. Retrieved 2025-01-28.`{{cite thesis}}`: CS1 maint: url-status ([link](/wiki/Category:CS1_maint:_url-status "Category:CS1 maint: url-status"))
7. ^ [***a***](#cite_ref-SOA_with_REST_7-0) [***b***](#cite_ref-SOA_with_REST_7-1) Erl, Thomas; Carlyle, Benjamin; Pautasso, Cesare; Balasubramanian, Raj (2012). "5.1". *SOA with REST: Principles, Patterns & Constraints for Building Enterprise Solutions with REST*. Upper Saddle River, New Jersey: Prentice Hall. [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [978-0-13-701251-0](/wiki/Special:BookSources/978-0-13-701251-0 "Special:BookSources/978-0-13-701251-0").
8. ^ [***a***](#cite_ref-Fielding-Ch2_8-0) [***b***](#cite_ref-Fielding-Ch2_8-1) Fielding, Roy Thomas (2000). ["Chapter 2: Network-based Application Architectures"](http://www.ics.uci.edu/~fielding/pubs/dissertation/net_app_arch.htm). *Architectural Styles and the Design of Network-based Software Architectures* (Ph.D.). University of California, Irvine. [Archived](https://web.archive.org/web/20141216114322/http://www.ics.uci.edu/~fielding/pubs/dissertation/net_app_arch.htm) from the original on 2014-12-16. Retrieved 2014-04-12.
9. **[^](#cite_ref-Richardson_2007_9-0)** Richardson, Leonard; Ruby, Sam (2007). [*RESTful Web Services*](https://archive.org/details/restfulwebservic00rich_0). Sebastopol, California: O'Reilly Media. [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [978-0-596-52926-0](/wiki/Special:BookSources/978-0-596-52926-0 "Special:BookSources/978-0-596-52926-0").
10. **[^](#cite_ref-10)** ["What is REST API?"](https://www.visual-paradigm.com/guide/development/what-is-rest-api/). *www.visual-paradigm.com*. [Archived](https://web.archive.org/web/20240224173920/https://www.visual-paradigm.com/guide/development/what-is-rest-api/) from the original on 2024-02-24. Retrieved 2024-02-24.
11. **[^](#cite_ref-RESTfulAPI.net_11-0)** Gupta, Lokesh (2 June 2018). ["REST HATEOAS"](http://restfulapi.net/hateoas/). *REST API Tutorial*. RESTfulAPI.net. [Archived](https://web.archive.org/web/20190407073345/https://restfulapi.net/hateoas/) from the original on 7 April 2019. Retrieved March 10, 2019.
12. **[^](#cite_ref-12)** ["Classification of HTTP APIs"](http://algermissen.io/classification_of_http_apis.html). *algermissen.io*. [Archived](https://web.archive.org/web/20230129022641/http://algermissen.io/classification_of_http_apis.html) from the original on 2023-01-29. Retrieved 2023-01-29.
13. **[^](#cite_ref-13)** Ivan Salvadori, Frank Siqueira (June 2015). ["A Maturity Model for Semantic RESTful Web APIs"](https://www.researchgate.net/publication/281287283). *Conference: Web Services (ICWS), 2015 IEEE International Conference OnAt*. New York. [Archived](https://web.archive.org/web/20240227165042/https://www.researchgate.net/publication/281287283_A_Maturity_Model_for_Semantic_RESTful_Web_APIs) from the original on 2024-02-27. Retrieved 2020-12-14 – via ResearchGate.

Further reading
---------------

[[edit](/w/index.php?title=REST&action=edit&section=9 "Edit section: Further reading")]

* Pautasso, Cesare; Wilde, Erik; Alarcon, Rosa (2014), [*REST: Advanced Research Topics and Practical Applications*](https://www.springer.com/engineering/signals/book/978-1-4614-9298-6), Springer, [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [9781461492986](/wiki/Special:BookSources/9781461492986 "Special:BookSources/9781461492986")
* Pautasso, Cesare; Zimmermann, Olaf; Leymann, Frank (April 2008), "Restful web services vs. "big"' web services", [*Proceedings of the 17th international conference on World Wide Web*](http://www.jopera.org/docs/publications/2008/restws), pp. 805–814, [doi](/wiki/Doi_(identifier) "Doi (identifier)"):[10.1145/1367497.1367606](https://doi.org/10.1145%2F1367497.1367606), [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [9781605580852](/wiki/Special:BookSources/9781605580852 "Special:BookSources/9781605580852"), [S2CID](/wiki/S2CID_(identifier) "S2CID (identifier)") [207167438](https://api.semanticscholar.org/CorpusID:207167438)
* Ferreira, Otavio (Nov 2009), [*Semantic Web Services: A RESTful Approach*](https://otaviofff.github.io/restful-grounding/), IADIS, [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [978-972-8924-93-5](/wiki/Special:BookSources/978-972-8924-93-5 "Special:BookSources/978-972-8924-93-5")
* Fowler, Martin (2010-03-18). ["Richardson Maturity Model: steps towards the glory of REST"](https://martinfowler.com/articles/richardsonMaturityModel.html). *martinfowler.com*. Retrieved 2017-06-26.

![](https://en.wikipedia.org/wiki/Special:CentralAutoLogin/start?type=1x1&usesul3=1)

Retrieved from "<https://en.wikipedia.org/w/index.php?title=REST&oldid=1284036074>"

[Categories](/wiki/Help:Category "Help:Category"):

* [Cloud standards](/wiki/Category:Cloud_standards "Category:Cloud standards")
* [Hypertext Transfer Protocol](/wiki/Category:Hypertext_Transfer_Protocol "Category:Hypertext Transfer Protocol")
* [Software architecture](/wiki/Category:Software_architecture "Category:Software architecture")
* [Web 2.0 neologisms](/wiki/Category:Web_2.0_neologisms "Category:Web 2.0 neologisms")

Hidden categories:

* [CS1 maint: url-status](/wiki/Category:CS1_maint:_url-status "Category:CS1 maint: url-status")
* [Articles with short description](/wiki/Category:Articles_with_short_description "Category:Articles with short description")
* [Short description matches Wikidata](/wiki/Category:Short_description_matches_Wikidata "Category:Short description matches Wikidata")
* [Pages displaying wikidata descriptions as a fallback via Module:Annotated link](/wiki/Category:Pages_displaying_wikidata_descriptions_as_a_fallback_via_Module:Annotated_link "Category:Pages displaying wikidata descriptions as a fallback via Module:Annotated link")