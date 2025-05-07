# Messaging Patterns Overview - Enterprise Integration Patterns

Source: https://www.enterpriseintegrationpatterns.com/patterns/messaging/

## Identified Architecture Patterns

### Event Driven

- Processor](DistributionAggregate.html)

[Scatter-Gather](BroadcastAggregate.html)

[Routing Slip](RoutingTable.html)

[Process Manager](ProcessManager.html)

[Message Broker](MessageBroker.html)

[Message  
Transformation](MessageTransformationIntro.html)

[Message Translator](MessageTranslator.html)

[Envelope Wrapper](EnvelopeWrapper.html)

[Content Enricher](DataEnricher.html)

[Content Filter](ContentFilter.html)

[Claim Check](StoreInLibrary.html)

[Normalizer](Normalizer.html)

[Canonical Data Model](CanonicalDataModel.html)

[Messaging Endpoints](MessagingEndpointsIntro.html)

[Message Endpoint](MessageEndpoint.html)

[Messaging Gateway](MessagingGateway.html)

[Messaging Mapper](MessagingMapper.html)

[Transactional Client](TransactionalClient.html)

[Polling Consumer](PollingConsumer.html)

[Event-driven Consumer](EventDrivenConsumer.html)

[Competing Consumers](CompetingConsumers.html)

[Message Dispatcher](MessageDispatcher.html)

[Selective Consumer](MessageSelector.html)

[Durable Subscriber](DurableSubscription.html)

[Idempotent Receiver](IdempotentReceiver.html)

[Service Activator](MessagingAdapter.html)

[Messaging Channels](MessagingChannelsIntro.html)

[Message Channel](MessageChannel.html)

[Point-to-Point Channel](PointToPointChannel.html)

[Publish-Subscr.
- * **Cloud-based integration**, including [Amazon Simple Queue Service (SQS)](http://aws.amazon.com/sqs/), [Amazon EventBridge](https://aws.amazon.com/eventbridge/), [Google Cloud Pub/Sub](https://cloud.google.com/pubsub/), or [Azure Service Bus](https://azure.microsoft.com/en-us/products/service-bus).
- A list of [modern examples](/ramblings/eip1_examples_updated.html) shows how the patterns apply to integration technologies like Kafka, Google Cloud Pub/Sub, Amazon SQS or [REST](/ramblings/81_restconversation.html).

### Serverless

- What about REST / SOA / Serverless / EDA Patterns?
- I've also re-implemented the Loan Broker example application in [AWS Lambda, EventBridge, and Step Functions](/ramblings/loanbroker_stepfunctions.html) and [GCP PubSub and Workflows](/ramblings/loanbroker_gcp_workflows.html).

### Data Storage

- The [65 messaging patterns](toc.html) are organized as follows (click on the image or view the [Table of Contents](toc.html)):

Integration Pattern Language
----------------------------

[Message Construct.](MessageConstructionIntro.html)

[Message](Message.html)

[Command Message](CommandMessage.html)

[Document Message](DocumentMessage.html)

[Event Message](EventMessage.html)

[Request-Reply](RequestReply.html)

[Return Address](ReturnAddress.html)

[Correlation Identifier](CorrelationIdentifier.html)

[Message Sequence](MessageSequence.html)

[Message Expiration](MessageExpiration.html)

[Format Indicator](FormatIndicator.html)

[Message Routing](MessageRoutingIntro.html)

[Pipes-and-Filters](PipesAndFilters.html)

[Message Router](MessageRouter.html)

[Content-based Router](ContentBasedRouter.html)

[Message Filter](Filter.html)

[Dynamic Router](DynamicRouter.html)

[Recipient List](RecipientList.html)

[Splitter](Sequencer.html)

[Aggregator](Aggregator.html)

[Resequencer](Resequencer.html)

[Composed Msg.
- Processor](DistributionAggregate.html)

[Scatter-Gather](BroadcastAggregate.html)

[Routing Slip](RoutingTable.html)

[Process Manager](ProcessManager.html)

[Message Broker](MessageBroker.html)

[Message  
Transformation](MessageTransformationIntro.html)

[Message Translator](MessageTranslator.html)

[Envelope Wrapper](EnvelopeWrapper.html)

[Content Enricher](DataEnricher.html)

[Content Filter](ContentFilter.html)

[Claim Check](StoreInLibrary.html)

[Normalizer](Normalizer.html)

[Canonical Data Model](CanonicalDataModel.html)

[Messaging Endpoints](MessagingEndpointsIntro.html)

[Message Endpoint](MessageEndpoint.html)

[Messaging Gateway](MessagingGateway.html)

[Messaging Mapper](MessagingMapper.html)

[Transactional Client](TransactionalClient.html)

[Polling Consumer](PollingConsumer.html)

[Event-driven Consumer](EventDrivenConsumer.html)

[Competing Consumers](CompetingConsumers.html)

[Message Dispatcher](MessageDispatcher.html)

[Selective Consumer](MessageSelector.html)

[Durable Subscriber](DurableSubscription.html)

[Idempotent Receiver](IdempotentReceiver.html)

[Service Activator](MessagingAdapter.html)

[Messaging Channels](MessagingChannelsIntro.html)

[Message Channel](MessageChannel.html)

[Point-to-Point Channel](PointToPointChannel.html)

[Publish-Subscr.
- * [**Message Construction Patterns**](MessageConstructionIntro.html) describe the intent, form and content of the messages that travel across the messaging system.

### Api Design

- If you are interested in getting access to material for academic purposes, please [contact us](gregor.html).
- What about REST / SOA / Serverless / EDA Patterns?
- --------------------------------------------------

The integration problems we solve today remain [frustratingly similar](/ramblings/81_restconversation.html) to 20 years ago.

### Integration

- # Messaging Patterns Overview - Enterprise Integration Patterns

Source: https://www.enterpriseintegrationpatterns.com/patterns/messaging/

[![Enterprise Integration Patterns](/img/eip.gif)](https://www.enterpriseintegrationpatterns.com)

Messaging Patterns

[HOME](/index.html) [PATTERNS](/eaipatterns.html) [RAMBLINGS](/ramblings.html) [ARTICLES](/articles.html) [TALKS](/talks.html) [DOWNLOAD](/downloads.html) [BOOKS](/books1.html) [CONTACT](/gregor.html)

|  |  |  |
| --- | --- | --- |
|  | Messaging Patterns Overview[Messaging Patterns](index.html) | [Contents](toc.html "Table of Contents")[Next â](toc.html "Table of Contents") |

This pattern catalog includes 65 integration patterns that we collected from integration projects and updated over two decades.
- The [65 messaging patterns](toc.html) are organized as follows (click on the image or view the [Table of Contents](toc.html)):

Integration Pattern Language
----------------------------

[Message Construct.](MessageConstructionIntro.html)

[Message](Message.html)

[Command Message](CommandMessage.html)

[Document Message](DocumentMessage.html)

[Event Message](EventMessage.html)

[Request-Reply](RequestReply.html)

[Return Address](ReturnAddress.html)

[Correlation Identifier](CorrelationIdentifier.html)

[Message Sequence](MessageSequence.html)

[Message Expiration](MessageExpiration.html)

[Format Indicator](FormatIndicator.html)

[Message Routing](MessageRoutingIntro.html)

[Pipes-and-Filters](PipesAndFilters.html)

[Message Router](MessageRouter.html)

[Content-based Router](ContentBasedRouter.html)

[Message Filter](Filter.html)

[Dynamic Router](DynamicRouter.html)

[Recipient List](RecipientList.html)

[Splitter](Sequencer.html)

[Aggregator](Aggregator.html)

[Resequencer](Resequencer.html)

[Composed Msg.
- Why Enterprise Integration Patterns?

### Scalability

- * Â» [Read the latest in My Blog](/ramblings)
* Â» [Get more insights from My Articles](/articles.html)
* Â» [See me live in my Upcoming Talks](/talks)

[![Enterprise Integration Patterns book cover](/img/eip_cover_120.png)](https://amazon.com/o/asin/0321200683/ref=nosim/enterpriseint-20)

[Enterprise Integration Patterns](https://amazon.com/o/asin/0321200683/ref=nosim/enterpriseint-20)  
The de-facto language for designing asynchronous, distributed systems.


---

[![Enterprise Integration Patterns](/img/eip.gif)](https://www.enterpriseintegrationpatterns.com)

Messaging Patterns

[HOME](/index.html) [PATTERNS](/eaipatterns.html) [RAMBLINGS](/ramblings.html) [ARTICLES](/articles.html) [TALKS](/talks.html) [DOWNLOAD](/downloads.html) [BOOKS](/books1.html) [CONTACT](/gregor.html)

|  |  |  |
| --- | --- | --- |
|  | Messaging Patterns Overview[Messaging Patterns](index.html) | [Contents](toc.html "Table of Contents")[Next â](toc.html "Table of Contents") |

This pattern catalog includes 65 integration patterns that we collected from integration projects and updated over two decades. They provide technology-independent design guidance for developers and architects to develop and document robust integration solutions. The [65 messaging patterns](toc.html) are organized as follows (click on the image or view the [Table of Contents](toc.html)):

Integration Pattern Language
----------------------------

[Message Construct.](MessageConstructionIntro.html)

[Message](Message.html)

[Command Message](CommandMessage.html)

[Document Message](DocumentMessage.html)

[Event Message](EventMessage.html)

[Request-Reply](RequestReply.html)

[Return Address](ReturnAddress.html)

[Correlation Identifier](CorrelationIdentifier.html)

[Message Sequence](MessageSequence.html)

[Message Expiration](MessageExpiration.html)

[Format Indicator](FormatIndicator.html)

[Message Routing](MessageRoutingIntro.html)

[Pipes-and-Filters](PipesAndFilters.html)

[Message Router](MessageRouter.html)

[Content-based Router](ContentBasedRouter.html)

[Message Filter](Filter.html)

[Dynamic Router](DynamicRouter.html)

[Recipient List](RecipientList.html)

[Splitter](Sequencer.html)

[Aggregator](Aggregator.html)

[Resequencer](Resequencer.html)

[Composed Msg. Processor](DistributionAggregate.html)

[Scatter-Gather](BroadcastAggregate.html)

[Routing Slip](RoutingTable.html)

[Process Manager](ProcessManager.html)

[Message Broker](MessageBroker.html)

[Message  
Transformation](MessageTransformationIntro.html)

[Message Translator](MessageTranslator.html)

[Envelope Wrapper](EnvelopeWrapper.html)

[Content Enricher](DataEnricher.html)

[Content Filter](ContentFilter.html)

[Claim Check](StoreInLibrary.html)

[Normalizer](Normalizer.html)

[Canonical Data Model](CanonicalDataModel.html)

[Messaging Endpoints](MessagingEndpointsIntro.html)

[Message Endpoint](MessageEndpoint.html)

[Messaging Gateway](MessagingGateway.html)

[Messaging Mapper](MessagingMapper.html)

[Transactional Client](TransactionalClient.html)

[Polling Consumer](PollingConsumer.html)

[Event-driven Consumer](EventDrivenConsumer.html)

[Competing Consumers](CompetingConsumers.html)

[Message Dispatcher](MessageDispatcher.html)

[Selective Consumer](MessageSelector.html)

[Durable Subscriber](DurableSubscription.html)

[Idempotent Receiver](IdempotentReceiver.html)

[Service Activator](MessagingAdapter.html)

[Messaging Channels](MessagingChannelsIntro.html)

[Message Channel](MessageChannel.html)

[Point-to-Point Channel](PointToPointChannel.html)

[Publish-Subscr. Channel](PublishSubscribeChannel.html)

[Datatype Channel](DatatypeChannel.html)

[Invalid Message Channel](InvalidMessageChannel.html)

[Dead Letter Channel](DeadLetterChannel.html)

[Guaranteed Delivery](GuaranteedMessaging.html)

[Channel Adapter](ChannelAdapter.html)

[Messaging Bridge](MessagingBridge.html)

[Message Bus](MessageBus.html)

[Systems Mgmt.](SystemManagementIntro.html)

[Control Bus](ControlBus.html)

[Detour](Detour.html)

[Wire Tap](WireTap.html)

[Message History](MessageHistory.html)

[Message Store](MessageStore.html)

[Smart Proxy](SmartProxy.html)

[Test Message](TestMessage.html)

[Channel Purger](ChannelPurger.html)

![](/img/eip1_nav.png)

* [**Integration Styles**](IntegrationStylesIntro.html) document different ways applications can be integrated, providing a historical account of integration technologies. All subsequent patterns follow the [*Messaging*](Messaging.html) style.
* [**Channel Patterns**](MessagingChannelsIntro.html) describe how messages are transported across a [*Message Channel*](MessageChannel.html). Most messaging systems implement these patterns.
* [**Message Construction Patterns**](MessageConstructionIntro.html) describe the intent, form and content of the messages that travel across the messaging system. The [*Message*](Message.html) pattern is the base pattern for this section.
* [**Routing Patterns**](MessageRoutingIntro.html) discuss how messages are directed from a sender to the correct receiver(s). The patterns presented in this section are specializations of the [*Message Router*](MessageRouter.html) pattern.
* [**Transformation Patterns**](MessageTransformationIntro.html) change the content of a message, for example to accommodate different data formats used by the sending and the receiving system. Data may have to be added, taken away or existing data may have to be rearranged. The base pattern for this section is the [*Message Translator*](MessageTranslator.html).
* [**Endpoint Patterns**](MessagingEndpointsIntro.html) describe how applications produce or consume messages.
* [**System Management Patterns**](SystemManagementIntro.html) describe what's needed to keep a complex message-based system running smoothly.

Why Enterprise Integration Patterns?
------------------------------------

Integration is a long-running topic in all aspects of software and IT, and it's too multi-faceted to be tackled with a simple 'cookbook' approach. Patterns, in contrast, document knowledge and experience that usually lives only in architects' heads. As accepted solutions to recurring problems, patterns are abstract enough to apply across integration technologies, but specific enough to provide hands-on guidance. They also provide a vocabulary to accurately describe solutions.

Patterns are not 'invented'; they are harvested from repeated use in practice. If you have built integration solutions, you likely have used some of these patterns, maybe in slight variations and perhaps calling them by a different name. This site condenses that experience into a coherent collection of proven patterns that form an integration pattern language. Patterns live in a specific context. This first set of patterns focus on [*Messaging*](Messaging.html). We also started to [harvest Conversation patterns](/patterns/conversation).

What products implement or use Enterprise Integration Patterns?
---------------------------------------------------------------

The patterns are independent of a specific implementation and help you design better solutions with any of the following platforms:

* **Open source ESB's** like [Mule ESB](http://www.mulesoft.org/), [JBoss Fuse](http://www.jboss.org/products/fuse/overview/), [Open ESB](http://www.open-esb.net/), [WSo2](http://wso2.com/), [Spring Integration](http://projects.spring.io/spring-integration/), or [Talend ESB](http://www.talend.com/)
* **Message Brokers** like [ActiveMQ](http://activemq.apache.org), [Apache Kafka](https://kafka.apache.org/), or [RabbitMQ](https://www.rabbitmq.com)
* **EAI and SOA platforms**, such as [IBM WebSphere MQ](http://www.ibm.com/software/mqseries), [TIBCO](http://www.tibco.com), [Vitria](http://www.vitria.com), [Oracle Service Bus](http://www.oracle.com/technetwork/middleware/service-bus), [WebMethods](http://www.softwareag.com/corporate/products/webmethods_integration/integration/overview/default.asp) (now Software AG), [Microsoft BizTalk](http://www.microsoft.com/biztalk ), or [Fiorano](http://www.fiorano.com).
* **Cloud-based integration**, including [Amazon Simple Queue Service (SQS)](http://aws.amazon.com/sqs/), [Amazon EventBridge](https://aws.amazon.com/eventbridge/), [Google Cloud Pub/Sub](https://cloud.google.com/pubsub/), or [Azure Service Bus](https://azure.microsoft.com/en-us/products/service-bus).
* **JMS-based messaging systems**
* **Microsoft technologies** like [MSMQ](https://msdn.microsoft.com/en-us/library/ms711472) or [Windows Communication Foundation (WCF)](https://msdn.microsoft.com/library/vstudio/ms735119)

How can you use the Patterns?
-----------------------------

To encourage widespread use of the integration pattern language, many parts are available under open source licensing. You are free to use the pattern name, icon, problem and solution statements, and the sketches (the diagram below the solution statement) under the [Creative Commons Attribution](http://creativecommons.org/licenses/by/4.0/) license.

> *The [CC-BY](https://creativecommons.org/licenses/by/4.0/) license allows you share, use and modify these elements as long as you give proper attribution, such as a link to this site or a citation of the book. See the [license for more detail](https://creativecommons.org/licenses/by/4.0/)*.

You can do a lot more with the patterns:

* **Build**. Many open-source frameworks, such as [Mule](http://mule.codehaus.org/display/MULE/Architecture+Guide), [Apache Camel](http://activemq.apache.org/camel/), or [Spring Integration](http://projects.spring.io/spring-integration/) incorporate our patterns. You can not only think in integration patterns, but also to code in them!
* **Document**. You can create design documents using our icon language by downloading the [Visio stencil](downloads.html) or using the [OmniGraffle stencil](http://www.graffletopia.com/stencils/137) created by one of our readers.
* **Read**. The book [*Enterprise Integration Patterns*](http://amazon.com/o/asin/0321200683/ref=nosim/enterpriseint-20) (Addison-Wesley, ISBN 0321200683) contains the full description of each pattern with plenty of examples -- over 700 pages worth of material. You can also read the full text [on-line on Safari](http://safari.informit.com/0321200683) (with membership).
* **Teach**. A number of professors use our material in lectures. If you are interested in getting access to material for academic purposes, please [contact us](gregor.html).

What about REST / SOA / Serverless / EDA Patterns?
--------------------------------------------------

The integration problems we solve today remain [frustratingly similar](/ramblings/81_restconversation.html) to 20 years ago. The design knowledhe encapsulated in the patterns does not age like specific technologies. A list of [modern examples](/ramblings/eip1_examples_updated.html) shows how the patterns apply to integration technologies like Kafka, Google Cloud Pub/Sub, Amazon SQS or [REST](/ramblings/81_restconversation.html). I've also re-implemented the Loan Broker example application in [AWS Lambda, EventBridge, and Step Functions](/ramblings/loanbroker_stepfunctions.html) and [GCP PubSub and Workflows](/ramblings/loanbroker_gcp_workflows.html).

Be Part of the Community
------------------------

Feel free to connect on [LinkedIn](https://www.linkedin.com/in/ghohpe). We welcome your feedback!

Contributors
------------

The patterns on this site are the result of discussions involving numerous individuals. Kyle Brown (co-author of "Enterprise Java Programming for IBM WebSphere" and "The Design Patterns Smalltalk Companion"), John Crupi (co-author of "Core J2EE Patterns"), Martin Fowler (author of too many books to mention here), Rachel Reinitz, Mark Weitzel were part of the original discussions. Conrad D'Cruz, Sean Neville, Mike Rettig, Jonathan Simon ended up authoring examples, case studies, and a chapter on the future of integration.

* Â» [Read the latest in My Blog](/ramblings)
* Â» [Get more insights from My Articles](/articles.html)
* Â» [See me live in my Upcoming Talks](/talks)

[![Enterprise Integration Patterns book cover](/img/eip_cover_120.png)](https://amazon.com/o/asin/0321200683/ref=nosim/enterpriseint-20)

[Enterprise Integration Patterns](https://amazon.com/o/asin/0321200683/ref=nosim/enterpriseint-20)  
The de-facto language for designing asynchronous, distributed systems. Over 100,000 copies sold.

[![Software Architect Elevator book cover](/img/sae_cover.jpg "The Software Architect Elevator")](https://www.architectelevator.com/book)

[The Software Architect Elevator](https://www.architectelevator.com/book)  
Rethink the role of architects as a connecting element across organizational layers. Acquire the technical, communication, and organizational skills to succeed in this new role.

[![Cloud Strategy book cover](/img/cloud_strategy_cover.png "Cloud Strategy")](https://www.cloudstrategybook.com)

[Cloud Strategy](https://www.cloudstrategybook.com)  
Make your cloud migration a success by translating high-level goals into conscious decisions with well-understood trade-offs.

[![Platform Strategy book cover](/img/platform_strategy_cover.jpg "Platform Strategy")](https://www.platformstrategybook.info)

[Platform Strategy](https://www.platformstrategybook.info)  
Platforms can boost innovation through harmonization, but they aren't easy to build. Learn from over a decade of designing and rolling out IT platforms.

© 2003, 2023 • [Bobby Woolf](mailto:woolf@acm.org) • All rights reserved.