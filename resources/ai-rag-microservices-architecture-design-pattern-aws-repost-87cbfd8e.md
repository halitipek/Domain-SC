# AI RAG microservices architecture design pattern | AWS re:Post

Source: https://repost.aws/questions/QU_eqmapujRpWltUeX3_lMfQ/ai-rag-microservices-architecture-design-pattern

## Identified Architecture Patterns

### Microservices

- # AI RAG microservices architecture design pattern | AWS re:Post

Source: https://repost.aws/questions/QU_eqmapujRpWltUeX3_lMfQ/ai-rag-microservices-architecture-design-pattern

Complete a 3 Question Survey and Earn a re:Post Badge

Help improve AWS Support Official channel in re:Post and share your experience - complete a quick [three-question survey](https://amazonexteu.qualtrics.com/jfe/form/SV_aWNzgGbZG7yzosC) to earn a re:Post badge!
- AI RAG microservices architecture design pattern
================================================

0

Hi!
- I'm building a stack of microservices with Java and SpringBoot to hold the main logic of my AI RAG service using langchain4j and Bedrock.

### Serverless

- Seehttps://medium.com/@chkamalsingh/microservices-core-principles-80e427261bc8 for best practices

Having small microservices (which is a pleonasm ;-) ) has multiple advantages on the side of NFRs (Non-Functional Requirements):

* better security: the execution roles associated to lambda can have reduced privileges
* performances and scalability can be managed in a more granular fashion
* high-availability: you can have different strategies for your different microservices.
- * [How do I upgrade boto3 and botocore in AWS Lambda to access newer AI models?](/knowledge-center/lambda-upgrade-boto3-botocore)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated a year ago
* [How do I use AWS SAM to build a Lambda-backed custom resource in Java for CloudFormation?](/knowledge-center/cloudformation-lambda-custom-java-resource)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated 2 years ago
* [How do I troubleshoot an algorithm error in my SageMaker AI processing job?](/knowledge-center/sagemaker-troubleshoot-algorithm-error)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated 6 days ago
* [How do I troubleshoot common issues with SageMaker AI JumpStart?](/knowledge-center/sagemaker-jumpstart-troubleshooting)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated 3 months ago
* [Architecting Real-Time Streaming for Generative AI Fraud Detection and Prevention](/articles/AR_4tfiCiKSxeZAe1PpujRcw/architecting-real-time-streaming-for-generative-ai-fraud-detection-and-prevention)

  ![profile picture](/media/profilePicture/thumbnails/small/IMxI-T4IbLQ4atD8RtGknYKw)![AWS](/static/icons/common/aws_logo_rgb_white.svg)

  EXPERT

  [Jatinder Singh](/community/users/USlq2IrkegQF2AlHhg1OfscQ)

  published 4 months agolg...

### Data Storage

- # AI RAG microservices architecture design pattern | AWS re:Post

Source: https://repost.aws/questions/QU_eqmapujRpWltUeX3_lMfQ/ai-rag-microservices-architecture-design-pattern

Complete a 3 Question Survey and Earn a re:Post Badge

Help improve AWS Support Official channel in re:Post and share your experience - complete a quick [three-question survey](https://amazonexteu.qualtrics.com/jfe/form/SV_aWNzgGbZG7yzosC) to earn a re:Post badge!
- This documents will be saved in an S3 bucket and also transform to embeddings and saved in the DB.
- Should I separate this and create one microservice for the data ingest and another one for the chatbot Q&A logic to avoid performance issues in the future?

### Api Design

- + Share
* [Didier\_Durand](/community/users/US9EmCAaadQL6tAn_w_Q877w) EXPERT

  a year ago

  Interesting project that you are building with leading-edge techs!


---

Complete a 3 Question Survey and Earn a re:Post Badge

Help improve AWS Support Official channel in re:Post and share your experience - complete a quick [three-question survey](https://amazonexteu.qualtrics.com/jfe/form/SV_aWNzgGbZG7yzosC) to earn a re:Post badge!

AI RAG microservices architecture design pattern
================================================

0

Hi!

I'm building a stack of microservices with Java and SpringBoot to hold the main logic of my AI RAG service using langchain4j and Bedrock. For now since I'm starting I'm building one microservice that will hold the data ingest logic from the documents uploaded by the users. This documents will be saved in an S3 bucket and also transform to embeddings and saved in the DB. Then in this service I will put also the logic of the chatbot so the users can get the response of their answers when they send the requests.

Should I separate this and create one microservice for the data ingest and another one for the chatbot Q&A logic to avoid performance issues in the future?

Thanks!

FollowCommentShare

Topics

[Java Development](/topics/TAeLiug9wVSxO2AZWyjH70Cw/java-development)[AWS Well-Architected Framework](/topics/TA5g9gZfzuQoWLsZ3wxihrgw/aws-well-architected-framework)[Microservices](/topics/TAgVlBAsraT-a-kw5WIHr2HQ/microservices)[Machine Learning & AI](/topics/TAXwEBZll0TtWxbiOoSjJrfw/machine-learning-ai)[Generative AI on AWS](/topics/TA0veCRV2rQAmHpkzbMFojUA/generative-ai-on-aws)

Tags

[Java Development](/tags/TAeLiug9wVSxO2AZWyjH70Cw/java-development)[AWS Well-Architected Framework](/tags/TA5g9gZfzuQoWLsZ3wxihrgw/aws-well-architected-framework)[Microservices](/tags/TAgVlBAsraT-a-kw5WIHr2HQ/microservices)[Amazon Bedrock](/tags/TAQeKlaPaNRQ2tWB6P7KrMag/amazon-bedrock)

Language

English

[cao95](/community/users/USkLFIQcT4QXCemVkx21cLLA)

asked a year ago3.5K viewslg...

1 Answer

* Newest
* Most votes
* Most comments

1

Hi,

For multiple reasons, you want to have multiple microservices and keep them small and loosely coupled. It's all about separation of duties.

Seehttps://medium.com/@chkamalsingh/microservices-core-principles-80e427261bc8 for best practices

Having small microservices (which is a pleonasm ;-) ) has multiple advantages on the side of NFRs (Non-Functional Requirements):

* better security: the execution roles associated to lambda can have reduced privileges
* performances and scalability can be managed in a more granular fashion
* high-availability: you can have different strategies for your different microservices.

Yes, it's more work upfront but, if you build for the long-term, it will pay back multiple times over the course of the life of your service.

Best,

Didier

CommentShare

![profile picture](/media/profilePicture/thumbnails/small/IMuhQWvwMXSdCdMqLwPrwFgw)![AWS](/static/icons/common/aws_logo_rgb_white.svg)

EXPERT

[Didier\_Durand](/community/users/US9EmCAaadQL6tAn_w_Q877w)

answered a year agolg...

* [cao95](/community/users/USkLFIQcT4QXCemVkx21cLLA) 

  a year ago

  I see! Thanks man!
  One final question, if my chatbot microservice needs to access the db to get some data, it should call the main data ingest microservice that is inserting the data into the DB to get the response. Or should the second microservice also map the db and the same table to get that data directly without calling the data ingest microservice?

  + Share
* [Didier\_Durand](/community/users/US9EmCAaadQL6tAn_w_Q877w) EXPERT

  a year ago

  My take is that you should keep the ingest service independent from read requests: you can separate concerns and avoid write permission when unneeded. So, it is better from my standpoint to reads from the chatbot service.

  + Share
* [cao95](/community/users/USkLFIQcT4QXCemVkx21cLLA) 

  a year ago

  I see, thanks man!

  + Share
* [Didier\_Durand](/community/users/US9EmCAaadQL6tAn_w_Q877w) EXPERT

  a year ago

  Interesting project that you are building with leading-edge techs! Good luck. Thanks for accepting my answer.

  + Share

Add your answer

You are not logged in. [Log in](/account/signin "Log in") to post an answer.

A good answer clearly answers the question and provides constructive feedback and encourages professional growth in the question asker.

Guidelines for Answering Questions

ClearPost answer

Relevant content
----------------

* [Solutions Architecture Java/Python AI?](/questions/QUWWZSMMhXTtaeAL7TRVP_Uw/solutions-architecture-java-python-ai)

  Accepted Answer

  [cao95](/community/users/USkLFIQcT4QXCemVkx21cLLA)

  asked a year agolg...
* [Create a data ingestion pipeline in AWS?](/questions/QUIT7mGfsUSO6HTzgDK0ylbQ/create-a-data-ingestion-pipeline-in-aws)

  Accepted Answer

  [cao95](/community/users/USkLFIQcT4QXCemVkx21cLLA)

  asked 7 months agolg...
* [PostrgreSQL with Pgvector extension or Astra DB as a vector DB for RAG approach using Bedrock?](/questions/QUx-r3NMXrTLSZhJh_LgrERw/postrgresql-with-pgvector-extension-or-astra-db-as-a-vector-db-for-rag-approach-using-bedrock)

  Accepted Answer

  [cao95](/community/users/USkLFIQcT4QXCemVkx21cLLA)

  asked a year agolg...
* [Can we create an agent with an action group to perform custom retrievals on a KB? If not, can we do it on OpenSearch or define a custom RAG flow using either of them?](/questions/QUTF30Oc8nTP6KbMV-XWLqbg/can-we-create-an-agent-with-an-action-group-to-perform-custom-retrievals-on-a-kb-if-not-can-we-do-it-on-opensearch-or-define-a-custom-rag-flow-using-either-of-them)

  [Safal](/community/users/US_OIhtINBQyimbk1Vi6A5kA)

  asked 21 days agolg...
* [How do I upgrade boto3 and botocore in AWS Lambda to access newer AI models?](/knowledge-center/lambda-upgrade-boto3-botocore)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated a year ago
* [How do I use AWS SAM to build a Lambda-backed custom resource in Java for CloudFormation?](/knowledge-center/cloudformation-lambda-custom-java-resource)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated 2 years ago
* [How do I troubleshoot an algorithm error in my SageMaker AI processing job?](/knowledge-center/sagemaker-troubleshoot-algorithm-error)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated 6 days ago
* [How do I troubleshoot common issues with SageMaker AI JumpStart?](/knowledge-center/sagemaker-jumpstart-troubleshooting)

  [![AWS OFFICIAL](/static/images/aws.png)](/aws-official)

  [AWS OFFICIAL](/aws-official)Updated 3 months ago
* [Architecting Real-Time Streaming for Generative AI Fraud Detection and Prevention](/articles/AR_4tfiCiKSxeZAe1PpujRcw/architecting-real-time-streaming-for-generative-ai-fraud-detection-and-prevention)

  ![profile picture](/media/profilePicture/thumbnails/small/IMxI-T4IbLQ4atD8RtGknYKw)![AWS](/static/icons/common/aws_logo_rgb_white.svg)

  EXPERT

  [Jatinder Singh](/community/users/USlq2IrkegQF2AlHhg1OfscQ)

  published 4 months agolg...
* [Unlocking the Potential of AWS Bedrock: Understanding Customization, Throughput, and Pricing](/articles/ARnP5OWHbwRIaLiriTEw7Owg/unlocking-the-potential-of-aws-bedrock-understanding-customization-throughput-and-pricing)

  ![profile picture](/media/profilePicture/thumbnails/small/IMTVXn7S-7QBiFGqi1czVD1g)

  EXPERT

  [Vitor Castellani](/community/users/UShrXpDdK0SvCyA9t6jEVxkQ)

  published 8 months agolg...

FEEDBACK