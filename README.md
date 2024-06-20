# CCL Official Chatbot Documentation :book:

This repository contains the source code for Cypher Crescent's comprehensive chatbot system.
This is a conversational/interactive AI chatbot designed to provide various functionalities including chat interaction, non-disclosure agreement (NDA) generation, proposal generation, and style guide enforcement. Below is an overview of the main components:

## [Dockerfile and Jenkinsfile](architecture.jpg)
These files provide instructions for building Docker images and defining the Jenkins pipeline for automation.

## [API](./api/)
The `api/` directory contains code related to the API implementation, including versioning, models, and routes.

## [Chatbot_v2](./chatbot_v2/)
The `chatbot_v2/` directory comprises the core components of the chat bot system. It includes functionalities for AI interaction, NDA generation, proposal generation, and style enforcement. Detailed breakdown:
- [`ai`](./chatbot_v2/ai/): Contains AI-related functionalities such as chat agents and style engines.
- [`configs`](./chatbot_v2/configs/): Holds configuration files including constants and prompt templates.
- [`handlers`](./chatbot_v2/handlers/): Implements various handlers for chat interactions, fields, questions, and templates.
- [`nda`](./chatbot_v2/nda/): Implements NDA generation functionalities.
- [`templates`](./chatbot_v2/templates/): Contains templates for various components of the chat interactions and generated documents.

## [Database](./database/)
The `database/` directory contains implementations related to database functionalities, including MongoDB integration, tests, tracking, and vector store.\


## [Guardrails](./guardrails/)
The `guardrails/` directory includes configurations and files for enforcing style guide rules.

## Other Files and Directories
- #### [`data`](./data/): 
Holds data files such as NDA templates and style guides.
 
- ### [`test_streams`](./test_streams/): 
Contains tests for various components including chat, NDA, proposal generation, and style guide enforcement.
- ### [`utilities`](./utilities/):
 Provides utility functionalities including AWS tools.

For more detailed information on each component, refer to the respective directories and files in the repository.

