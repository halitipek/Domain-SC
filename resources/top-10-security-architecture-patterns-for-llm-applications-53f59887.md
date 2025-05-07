# Top 10 security architecture patterns for LLM applications

Source: https://www.redhat.com/en/blog/top-10-security-architecture-patterns-llm-applications

## Identified Architecture Patterns

### Data Storage

- Implement rate limiting**

Leverage AI platform components like [API](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces) gateways—for example, [3Scale APICast](https://github.com/3scale/APIcast)—and don’t reinvent the wheel.
- Consider using function calling and structured outputs to enforce specific formats.
- Additionally, leverage AI platform solutions like runtime guardrails, such as [TrustyAI](/en/blog/trustyai-open-source-project-looking-solve-ais-bias) or sandboxed environments to enhance reliability and safety.

### Api Design

- Use models from trusted sources and review their licensing**

AI models are released under a variety of different software licenses, some much more restrictive than others.
- Even if you choose to use models provided by organizations you trust, take the time needed to review the license restrictions so you are not surprised in the future.
- Harden AI components as you would harden traditional applications**

Some key AI components may prioritize usability over security by default, so you should carefully analyze the security restrictions of every component you use in your AI systems.

### Api Security

- Use sound authentication and authorization standards, such as [OpenID Connect](https://docs.redhat.com/en/documentation/red_hat_single_sign-on/7.0/html/securing_applications_and_services_guide/openid_connect_3) (OIDC) and OAuth2.
- Avoid allowing unauthenticated access or using API keys if possible.
- Implement rate limiting**

Leverage AI platform components like [API](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces) gateways—for example, [3Scale APICast](https://github.com/3scale/APIcast)—and don’t reinvent the wheel.

### Security

- Use sound authentication and authorization standards, such as [OpenID Connect](https://docs.redhat.com/en/documentation/red_hat_single_sign-on/7.0/html/securing_applications_and_services_guide/openid_connect_3) (OIDC) and OAuth2.


---

Top 10 security architecture patterns for LLM applications
==========================================================

December 9, 2024[Florencio Cano Gabarda](/en/authors/florencio-cano-gabarda "See more by Florencio Cano Gabarda")*3*-minute read

[Artificial intelligence](/en/blog?f[0]=taxonomy_topic_tid:75501#rhdc-search-listing)

Share



Subscribe

The software industry has started developing a vast array of [artificial intelligence](https://www.redhat.com/en/blog/channel/artificial-intelligence) (AI) applications based on [large language models](https://www.redhat.com/en/topics/ai/what-are-large-language-models) (LLMs). While many security threats to LLMs are similar to those affecting traditional software, LLMs and their applications also face unique security risks due to their specific characteristics. These risks can often be mitigated or reduced by applying specific security architecture patterns. Here are 10 ways to mitigate and reduce security risks in LLM applications.

### **1. Identify, authenticate and authorize all the principals**

This includes humans and agents that participate in the LLM application. Use sound authentication and authorization standards, such as [OpenID Connect](https://docs.redhat.com/en/documentation/red_hat_single_sign-on/7.0/html/securing_applications_and_services_guide/openid_connect_3) (OIDC) and OAuth2. Avoid allowing unauthenticated access or using API keys if possible.

### **2. Implement rate limiting**

Leverage AI platform components like [API](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces) gateways—for example, [3Scale APICast](https://github.com/3scale/APIcast)—and don’t reinvent the wheel. You can limit the number of requests that can be made to your LLM to 5 per second if you expect that only humans will access it.

### **3. Use open models**

And deploy them locally or on your own cloud instances. Open models provide a level of transparency that closed models cannot provide. If your use case requires that you use a cloud model offered as a service, choose a trusted provider, understand its security posture and leverage any security features it provides. [IBM Granite models](https://www.ibm.com/granite) are trustworthy and open enterprise models that you can fine-tune for your own purposes.

### **4. Validate LLM output**

LLM output cannot be fully predicted or controlled. Use mechanisms to validate it before presenting it to users or using it as input for other systems. Consider using function calling and structured outputs to enforce specific formats. Additionally, leverage AI platform solutions like runtime guardrails, such as [TrustyAI](/en/blog/trustyai-open-source-project-looking-solve-ais-bias) or sandboxed environments to enhance reliability and safety.

### **5. Use logging wisely**

LLMs are non-deterministic, so having a log of the inputs and outputs of the LLM might help when you have to investigate potential incidents and suspicious activity. When logging data, be careful with sensitive and personally identifiable information (PII) and do a privacy impact assessment (PIA).

### **6. Measure and compare the safety of the models you choose**

Some models respond with more hallucinations and harmful responses than others. This affects how much trust we can put on a model. The more harmful responses a model provides, the less safe the model is. The safety of a model can be measured and compared with the safety of other models. By doing this we know that the safety of the models we use is on par with the market and is generally what the users of the application expect. Remember that if you are fine-tuning a model independently of the fine-tuning data used, the safety of the resulting model might have changed. In order to measure the safety of a model, you can use open source software like [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness), [Project Moonshot](https://github.com/aiverify-foundation/moonshot) or [Giskard](https://github.com/Giskard-AI/giskard).

### **7. Use models from trusted sources and review their licensing**

AI models are released under a variety of different software licenses, some much more restrictive than others. Even if you choose to use models provided by organizations you trust, take the time needed to review the license restrictions so you are not surprised in the future.

### **8. Data is crucial on LLM applications**

Protect all data sources—such as training data, fine-tuning data, models and RAG data—against unauthorized access and log any attempts to access or modify it. If the data is modified, an attacker may be able to control the responses and behavior of the LLM system.

### **9. Harden AI components as you would harden traditional applications**

Some key AI components may prioritize usability over security by default, so you should carefully analyze the security restrictions of every component you use in your AI systems. Review the ports that each component opens, what services are listening and their security configuration. Tighten these restrictions as needed to properly harden your AI application.

### **10. Keep your LLM system up to date**

As your LLM system probably depends on many open source components, treat these as you would in any other software system and keep them updated to versions without known critical or important vulnerabilities. Also, where possible, try to stay aware of the health of the open source and upstream projects that create the components you are using. If you can, you should get involved and contribute to these projects, especially those that produce the key components in your system.

**Conclusion**
--------------

LLM applications pose specific security risks, many of which can be mitigated or eliminated using AI security architecture patterns we've discussed here. These patterns are often available through the AI platform itself. As a software architect or designer, it’s important to understand the platform's built-in functionality so you can avoid reinventing the wheel or adding unnecessary workload.

[Red Hat OpenShift AI](/en/products/ai/openshift-ai) is a flexible and scalable AI and machine learning (ML) platform that enables enterprises to develop and deploy AI-powered applications at scale across hybrid cloud environments, and can help achieve these security objectives.

product trial

Red Hat OpenShift AI (Self-Managed) | Product Trial
---------------------------------------------------

An open source machine learning (ML) platform for the hybrid cloud.

[Try it](/en/technologies/cloud-computing/openshift/openshift-ai/trial?intcmp=7013a000003Sq0iAAC "Red Hat OpenShift AI (Self-Managed) | Product Trial")

---



### About the author

[![Florencio Cano Gabarda, Principal Product Security Architect, Red Hat](https://www.redhat.com/rhdc/managed-files/styles/media_thumbnail/private/florencio%20-%20Florencio%20Cano%20Gabarda.png?itok=GYM9EEuU)](/en/authors/florencio-cano-gabarda)

[### Florencio Cano Gabarda

Principal Product Security Architect](/en/authors/florencio-cano-gabarda)



Florencio has had cybersecurity in his veins since he was a kid. He started in cybersecurity around 1998 (time flies!) first as a hobby and then professionally. His first job required him to develop a host-based intrusion detection system in Python and for Linux for a research group in his university. Between 2008 and 2015 he had his own startup, which offered cybersecurity consulting services. He was CISO and head of security of a big retail company in Spain (more than 100k RHEL devices, including POS systems). Since 2020, he has worked at Red Hat as a Product Security Engineer and Architect.


[Read full bio](/en/authors/florencio-cano-gabarda)

Enter keywords here to search blogs


UI\_Icon-Red\_Hat-Close-A-Black-RGB

Search

More like this
--------------

### [Blog post](/en/blog/no-math-ai-podcast-demystifying-impact-latest-ai-developments)

#### [The “No Math AI” podcast: demystifying the impact of the latest AI developments](/en/blog/no-math-ai-podcast-demystifying-impact-latest-ai-developments)

### [Blog post](/en/blog/model-context-protocol-discover-missing-link-ai-integration)

#### [Model Context Protocol: Discover the missing link in AI integration](/en/blog/model-context-protocol-discover-missing-link-ai-integration)

### [Original shows](/en/compiler-podcast/diagnosing-and-dispelling-ai-hallucinations)

#### [Diagnosing and Dispelling AI Hallucinations | Compiler](/en/compiler-podcast/diagnosing-and-dispelling-ai-hallucinations)

### [Original shows](/en/compiler-podcast/ai-feedback-loops)

#### [Chasing Its Own Tail | Compiler](/en/compiler-podcast/ai-feedback-loops)

Keep exploring
--------------

* [What is agentic AI?Article](https://www.redhat.com/en/topics/ai/what-is-agentic-ai?intcmp=7013a000003Sq0iAAC "What is agentic AI?")
* [Predictive AI vs. generative AIArticle](https://www.redhat.com/en/topics/ai/predictive-ai-vs-generative-ai?intcmp=7013a000003Sq0iAAC "Predictive AI vs. generative AI")
* [Top considerations for building a production-ready AI/ML environmentE-book](/en/resources/building-production-ready-ai-ml-environment-e-book?intcmp=7013a000003Sq0iAAC "Top considerations for building a production-ready AI/ML environment")
* [Generative AI, the Ansible wayVideo](https://tv.redhat.com/detail/6347396983112/generative-ai-the-ansible-way?intcmp=7013a000003Sq0iAAC "Generative AI, the Ansible way")
* [Innovate and transform with a modern application platformE-book](/en/engage/modern-application-platform-20230406?intcmp=7013a000003Sq0iAAC "Innovate and transform with a modern application platform")

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