# ai
This folder contains the codes and tools that drive the ai functionalities of the chatbot. It contains the following files/modules:
1. [`Chat`](#chat)
2. [`chat_agent`](#chat_agent)
3. [`generate_letter`](#generate_letter)
4. [`generate_nda`](#generate_nda)
5. [`generate_proposal`](#generate_proposal_2)
6. [`style_engine`](#generate_proposal_2)
7. [`tools`](#tools)


### [`chat`](./chat.py)
This module contains functions for processing prompts and conducting chats using various methods such as retrieval-aided generation (RAG) and Guardrail mechanism.


Key Functions:
- process_prompt: Process a single prompt in a synchronous manner.
- process_prompt_stream: Process a single prompt in an asynchronous manner with streaming.
- rag_chat: Conduct a chat using Retrieval-Aided Generation (RAG) method.
- guardrail_chat: Conduct a chat using Guardrail mechanism.


### [`chat_agent`](./chat_agent.py)
This contains the codes for the CCL chat agent.


### [`generate_letter`](./generate_letter.py)
This is the Module for generating formal letters using language models. 
It contains functions that generate a formal letter synchronously using parameters as context strings from the user.

### [`generate_nda`](./generate_nda.py)
This is the Module for generating Non-Disclosure Agreements (NDAs) using language models.

Classes:
- GenerateNDA: A class for generating NDAs.

Functions:
- handle_section: Handle a single section of the NDA synchronously.
- handle_sections: Handle all sections of the NDA synchronously.
- handle_sections_2: Handle all sections of the NDA asynchronously with streaming.


### [`generate_proposal`](./generate_proposal_2.py)
This is the Module for auto-generating proposal sections.

Classes:
- AutoGenerateSection: A class for generating proposal sections.

Functions:
- section_template: Set the template for the proposal section.
- template_questions: Get the questions related to the proposal section.
- generate_section: Generate a proposal section synchronously.
- generate_section_2: Generate a proposal section asynchronously with streaming.
- generate_controller: Decide whether to generate the proposal section synchronously or asynchronously.
- stream_section_generation: Generate the proposal section asynchronously with streaming.


### [`style_engine`](./style_engine.py)
Module for language style correction and interpretation based on an editorial style guide manual.

Classes:
- StyleGuideParser: Pydantic BaseModel for parsing style guide suggestions.
- StyleGuideParserV2: Pydantic BaseModel for parsing style guide suggestions (alternate version).
- StyleGuide: A class for generating and managing style guide information.

Functions:
- styleguide_modify_input: Modify input text based on style guide suggestions.


### [`tools`](./tools.py)
This contains tools for searching and returning questions concerning CypherCrescent also called CCL.
