# MongoDB

This subfolder, "MongoDB," contains Pydantic models for managing conversations and users as part of the CCL project.

## Table of Contents

- [Introduction](#introduction)
- [Models](#models)
  - [PromptModel](#promptmodel)
  - [ConversationModel](#conversationmodel)
  - [UserModel](#usermodel)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This subfolder includes Pydantic models designed for managing conversations, chats and users in the context of the CCL project. These models are part of the broader functionality provided by the Chatbot which is able to store user conversations and prompts including the dates and times that these conversations were made.

## Models

### PromptModel

```python
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List

class PromptModel(BaseModel):
    question: str
    answer: str

from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List

```
### ConversationModel

```python
class ConversationModel(BaseModel):
    date_created: datetime = Field(default_factory=datetime.utcnow)
    date_modified: datetime = Field(default_factory=datetime.utcnow)
    conversation_name: str = "New conversation"
    conversation_id: str = Field(default_factory=lambda: uuid4().hex)
    prompts: List[PromptModel] = []

```

### UserModel

```python
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List

class UserModel(BaseModel):
    user_id: str = Field(default_factory=lambda: uuid4().hex)
    conversations: List[ConversationModel] = []

```
## Usage


## Contributing 
Contributions can be made to these functionalities including issues, pull requests and contributions.

## License 
This sub-folder is part of the database folder that contains the files and codes for the CCL chatbot project under CypherCrescent ltd.


