# CCL Chatbot Official Documentation :book:

This is Cyphercrescent's official chatbot project. 
This is a conversational/interactive chatbot that utilises Large-language model(LLM) to interact with company data, generate proposals, letters and Non-disclosure aggreement  
 

## Table of Contents

1. Getting Started

2. Prerequisites

- Installation :cd:

- Usage

- Configuration

3. Contributing

4. *License*

This README file contains the following folders and files: 


- ## [API](api/v1/):
This section contains the API-related endpoints, and their corresponding handlers for the chatbot.
    - [v1](api/v1/)
- [models](api/v1/models/)
    - [_init_.py](api/__init__.py)

- ## [chatbot_v2](chatbot_v2/ai/)
This section contains the main chatbot logic and components.
- [ai]()
- [configs]()
- [handlers]()
- [nda]()
- [templates]()
- [vector_store]()
- [_init_.py]()

- ## [data](data/) 
This secton contains the datasets for NDA templates  and style guide training data, used in the chatbot project.

- ## [database](database/):
This section contains the database-related files and scripts for the chatbot.

- ## [test_streams](test_streams/):
This section contains the test data and scripts for the chatbot's streaming capabilities.

- ## [utilities](utilities/)
This section contains utility scripts and tools used in the project.

- ## [.gitignore](.gitignore/)
This specifies the files and directories that should be ignored by the version control system.

- ## architecture.jpg
![architecture](/architecture.jpg)
This is a blueprint/representation of the chatbot flow system.

- ## [Jenkinsfile](Jenkinsfile/)

- ### [main.py](main.py/)

- [README.md](README.md/)

- ## [requirements.txt](requirements.txt/):
This file contains a list of the required Python packages and libraries for the chatbot project.

#1.  Getting started
All the codes and documents can be found on the github repository.
Api keys and logins are strictly **confidential.**

#2. Prerequisites
To run these codes, you need to install the following softwares and libraries:
- Python 3.1.2
- MongoDB

Installation 
#### Clone the repository
git clone <link>

#### Change directory
cd our-repo

#### Install dependencies
pip install -r requirements.txt


# Usage
You can use some of the codes by interacting python environment.

# Configuration

Here are the configuration settings and environment variable you need for mongoDB and other packages.
ENV=prod
MONGO_DB_USERNAME=your_username
MONGO_DB_PASSWORD=your_password


# Database Configuration
Here are the codes for the mongoDB configuration. 

uri = "mongodb+srv://your_username:your_password@cluster0.n4hegjm.mongodb.net/?retryWrites=true&w=majority"
database_name = "chat_history_database"
collection_name = "ccl_collection"

# Contributing 
Contributions can be made on this project using report issues, pull request and discussions.
Kindly channel reports to the Digital Tech Team @Cypher crescent 

# License
This project is licensed under Cyphercrescent ltd.  




