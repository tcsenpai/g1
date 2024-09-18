# multi1: Using multiple AI providers to create o1-like reasoning chains

## Table of Contents
- [multi1: Using multiple AI providers to create o1-like reasoning chains](#multi1-using-multiple-ai-providers-to-create-o1-like-reasoning-chains)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Providers](#providers)
    - [Developer Resources for adding new providers](#developer-resources-for-adding-new-providers)
  - [Work in progress](#work-in-progress)
  - [Call to Action](#call-to-action)
  - [Example](#example)
  - [Description](#description)
    - [How it works](#how-it-works)
    - [Disclaimer](#disclaimer)
    - [Quickstart](#quickstart)
    - [Prompting Strategy](#prompting-strategy)
  - [Contributing](#contributing)
    - [Credits](#credits)

multi1 is a tool that uses several AI providers (with an emphasis on LiteLLM) to create a reasoning chain that significantly improves the current reasoning capabilities of LLMs. Although it does not use o1, it is capable of significantly improving the current reasoning capabilities of LLMs. Llama 3.1 8b and above models work much better than older ones, but this can be applied to many available models.

This is an early prototype of using prompting strategies to improve the LLM's reasoning capabilities through o1-like reasoning chains. This allows the LLM to "think" and solve logical problems that usually otherwise stump leading models. Unlike o1, all the reasoning tokens are shown.
 
## Features

- [x] Using an unified interface to try out different providers
- [x] LiteLLM default provider with local and remote support
- [x] Configuring the app from the sidebar
- [x] Modular design for quick provider adding 

## Providers

- [x] LiteLLM (local and remote)
- [x] Ollama (local)
- [x] Perplexity (remote, requires API key)
- [x] Groq (remote, requires API key)

### Developer Resources for adding new providers

- Instructions for adding new providers can be found in `app/utils/providers/instructions.md`
- A skeleton provider template is available at `app/utils/providers/skeleton_provider.py`

## Work in progress

- [ ] Further LiteLLM testing with remote providers
- [ ] Reliable JSON output schema (especially for LiteLLM)
- [ ] Create a better way to add new providers for developers


## Call to Action

We're looking for developers to help improve multi1! Here are some areas where you can contribute:

- Improve LiteLLM backend to have a consistent handler for most providers
- Test and implement new AI providers to expand the capabilities of multi1
- Conduct more extensive testing of LiteLLM with various remote providers
- Experiment with and refine the system prompt to enhance reasoning capabilities

Your contributions can help make multi1 a more robust and versatile tool for AI-powered reasoning chains.


## Example

![Simple Math](examples/maths.png)

## Description

***IMPORTANT: multi1 was created as a fork of [g1](https://github.com/bklieger-groq/g1/), made by [Benjamin Klieger](https://x.com/benjaminklieger).***

This is an early prototype of using prompting strategies to improve the LLM's reasoning capabilities through o1-like reasoning chains. This allows the LLM to "think" and solve logical problems that usually otherwise stump leading models. Unlike o1, all the reasoning tokens are shown, and the app uses an open source model.

multi1 is experimental and is made to help inspire the open source community to develop new strategies to produce o1-like reasoning. This experiment helps show the power of prompting reasoning in visualized steps, not a comparison to or full replication of o1, which uses different techniques. OpenAI's o1 is instead trained with large-scale reinforcement learning to reason using Chain of Thought, achieving state-of-the-art performance on complex PhD-level problems.

multi1 demonstrates the potential of prompting alone to overcome straightforward LLM logic issues like the Strawberry problem, allowing existing open source models to benefit from dynamic reasoning chains and an improved interface for exploring them.


### How it works

multi1 powered by one of the supported models creates reasoning chains, in principle a dynamic Chain of Thought, that allows the LLM to "think" and solve some logical problems that usually otherwise stump leading models.

At each step, the LLM can choose to continue to another reasoning step, or provide a final answer. Each step is titled and visible to the user. The system prompt also includes tips for the LLM. There is a full explanation under Prompt Breakdown, but a few examples are asking the model to “include exploration of alternative answers” and “use at least 3 methods to derive the answer”.

The reasoning ability of the LLM is therefore improved through combining Chain-of-Thought with the requirement to try multiple methods, explore alternative answers, question previous draft solutions, and consider the LLM’s limitations. This alone, without any training, is sufficient to achieve ~70% accuracy on the Strawberry problem (n=10, "How many Rs are in strawberry?"). Without prompting, Llama-3.1-70b had 0% accuracy and ChatGPT-4o had 30% accuracy.


### Disclaimer

> [!IMPORTANT]
> multi1 is not perfect, but it can perform significantly better than LLMs out-of-the-box. Accuracy has yet to be formally evaluated, especially considering the limitations of the prompting strategy and the amount of providers used. Each provider has its own limitations, and while multi1 tries to harmonise them all, there can (and will) be problems here and there. See [Contributing](#contributing) and [Call to Action](#call-to-action) for ways to help improve multi1 (and thank you in advance).



### Quickstart

To use multi1, follow the below steps:

1. Set up the environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

   or, if you prefer not using venv:

   ```
   pip3 install -r requirements.txt
   ```

2. Copy the example environment file:

   ```
   cp example.env .env
   ```

3. Edit the .env file with your API keys / models preferences (or do it from the app's configuration menu)

4. Run the main interface

   ```
   streamlit run app/main.py
   ```

---

### Prompting Strategy

The prompt is contained in app/system_prompt.txt and uses clear instructions to conduct the LLM behavior.


## Contributing

We welcome contributions to multi1! Here's how you can help:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear, descriptive messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please ensure your code adheres to the project's coding standards and include tests for new features or bug fixes.

For major changes, please open an issue first to discuss what you would like to change. This ensures that your efforts align with the project's goals and direction.


### Credits

multi1 is derived from g1.

g1 was originally developed by [Benjamin Klieger](https://x.com/benjaminklieger).
  