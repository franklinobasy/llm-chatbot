# CCL Official Chatbot Documentation :book:

This repository contains the source code for Cypher Crescent's comprehensive chatbot system.
This is a conversational/interactive AI chatbot designed to provide various functionalities including chat interaction, non-disclosure agreement (NDA) generation, proposal generation, and style guide enforcement. Below is an overview of the main components:

## [Dockerfile and Jenkinsfile](README.md)
These files provide instructions for building Docker images and defining the Jenkins pipeline for automation.

## [API](./api/Readme.md)
The `api/` directory contains code related to the API implementation, including versioning, models, and routes.

## [Chatbot_v2](./chatbot_v2/Readme.md)
The `chatbot_v2/` directory comprises the core components of the chat bot system. It includes functionalities for AI interaction, NDA generation, proposal generation, and style enforcement. Detailed breakdown:
- `ai/`: Contains AI-related functionalities such as chat agents and style engines.
- `configs/`: Holds configuration files including constants and prompt templates.
- `handlers/`: Implements various handlers for chat interactions, fields, questions, and templates.
- `nda/`: Implements NDA generation functionalities.
- `templates/`: Contains templates for various components of the chat interactions and generated documents.

## [Database](./Database/Readme.md)
The `database/` directory contains implementations related to database functionalities, including MongoDB integration, tests, tracking, and vector store.

## [Guardrails](./guardrails/Readme.md)
The `guardrails/` directory includes configurations and files for enforcing style guide rules.

## Other Files and Directories
- `data/`: Holds data files such as NDA templates and style guides.
- `test_streams/`: Contains tests for various components including chat, NDA, proposal generation, and style guide enforcement.
- `utilities/`: Provides utility functionalities including AWS tools.

For more detailed information on each component, refer to the respective directories and files in the repository.

