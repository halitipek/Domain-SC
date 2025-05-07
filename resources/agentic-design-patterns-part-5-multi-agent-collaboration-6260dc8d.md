# Agentic Design Patterns Part 5, Multi-Agent Collaboration

Source: https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/

## Identified Architecture Patterns

### Agent Communication

- This results in a cacophony of LLM calls and message passing between agents that can result in very complex workflows.

### Data Storage

- # Agentic Design Patterns Part 5, Multi-Agent Collaboration

Source: https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/

Dear friends,

Multi-agent collaboration is the last of the four [key AI agentic design patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua) that I’ve described in recent letters.
- Write code to perform the task .
- Further, ablation studies (for example, in the AutoGen paper cited below) show that multiple agents give superior performance to a single agent.

### Api Design

- If you're interested in playing with a fun multi-agent system, also check out ChatDev, an open source implementation of a set of agents that run a virtual software company.
- If you're interested in learning more, I recommend:

* “[Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua),” Qian et al.


---

Dear friends,

Multi-agent collaboration is the last of the four [key AI agentic design patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua) that I’ve described in recent letters. Given a complex task like writing software, a multi-agent approach would break down the task into subtasks to be executed by different roles — such as a software engineer, product manager, designer, QA (quality assurance) engineer, and so on — and have different agents accomplish different subtasks.  
  
Different agents might be built by prompting one LLM (or, if you prefer, multiple LLMs) to carry out different tasks. For example, to build a software engineer agent, we might prompt the LLM: “You are an expert in writing clear, efficient code. Write code to perform the task . . ..”

It might seem counterintuitive that, although we are making multiple calls to the same LLM, we apply the programming abstraction of using multiple agents. I’d like to offer a few reasons:

* It works! Many teams are getting good results with this method, and there’s nothing like results! Further, ablation studies (for example, in the AutoGen paper cited below) show that multiple agents give superior performance to a single agent.
* Even though some LLMs today can accept very long input contexts (for instance, Gemini 1.5 Pro accepts 1 million tokens), their ability to truly understand long, complex inputs is mixed. An agentic workflow in which the LLM is prompted to focus on one thing at a time can give better performance. By telling it when it should play software engineer, we can also specify what is important in that role’s subtask. For example, the prompt above emphasized clear, efficient code as opposed to, say, scalable and highly secure code. By decomposing the overall task into subtasks, we can optimize the subtasks better.
* Perhaps most important, the multi-agent design pattern gives us, as developers, a framework for breaking down complex tasks into subtasks. When writing code to run on a single CPU, we often break our program up into different processes or threads. This is a useful abstraction that lets us decompose a task, like implementing a web browser, into subtasks that are easier to code. I find thinking through multi-agent roles to be a useful abstraction as well.

In many companies, managers routinely decide what roles to hire, and then how to split complex projects — like writing a large piece of software or preparing a research report — into smaller tasks to assign to employees with different specialties. Using multiple agents is analogous. Each agent implements its own workflow, has its own memory (itself a rapidly evolving area in agentic technology: how can an agent remember enough of its past interactions to perform better on upcoming ones?), and may ask other agents for help. Agents can also engage in Planning and Tool Use. This results in a cacophony of LLM calls and message passing between agents that can result in very complex workflows.

While managing people is hard, it's a sufficiently familiar idea that it gives us a mental framework for how to "hire" and assign tasks to our AI agents. Fortunately, the damage from mismanaging an AI agent is much lower than that from mismanaging humans!

Emerging frameworks like AutoGen, Crew AI, and LangGraph, provide rich ways to build multi-agent solutions to problems. If you're interested in playing with a fun multi-agent system, also check out ChatDev, an open source implementation of a set of agents that run a virtual software company. I encourage you to check out their [GitHub repo](https://github.com/OpenBMB/ChatDev?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua) and perhaps clone the repo and run the system yourself. While it may not always produce what you want, you might be amazed at how well it does.

Like the design pattern of [Planning](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-4-planning/?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua), I find the output quality of multi-agent collaboration hard to predict, especially when allowing agents to interact freely and providing them with multiple tools. The more mature patterns of [Reflection](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua) and [Tool Use](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-3-tool-use/?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua) are more reliable. I hope you enjoy playing with these agentic design patterns and that they produce amazing results for you!

If you're interested in learning more, I recommend:

* “[Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua),” Qian et al. (2023) (the ChatDev paper)
* “[AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua),” Wu et al. (2023)
* “[MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8TZzur2df1qdnGx09b-Fg94DTsc3-xXao4StKvKNU2HR51el3n8yOm0CPSw6GiAoLQNKua),” Hong et al. (2023)

Keep learning!

Andrew

[Read "Agentic Design Patterns Part 1: Four AI agent strategies that improve GPT-4 and GPT-3.5 performance"](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io)

[Read "Agentic Design Patterns Part 2: Reflection"](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/?ref=dl-staging-website.ghost.io)

[Read "Agentic Design Patterns Part 3: Tool Use"](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-3-tool-use/?ref=dl-staging-website.ghost.io)

[Read "Agentic Design Patterns Part 4: Planning"](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-4-planning/?ref=dl-staging-website.ghost.io)

Subscribe to The Batch
----------------------

Stay updated with weekly AI News and Insights delivered to your inbox