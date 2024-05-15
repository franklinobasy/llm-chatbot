# ai
This folder contains the codes and tools that drive the ai functionalities of the chatbot. It contains the following files/modules:

- ## [`chat/`]:
This module contains functions for processing prompts and conducting chats using various methods such as retrieval-aided generation (RAG) and Guardrail mechanism.

Functions:
    - process_prompt: Process a single prompt in a synchronous manner.
    - process_prompt_stream: Process a single prompt in an asynchronous manner with streaming.
    - rag_chat: Conduct a chat using Retrieval-Aided Generation (RAG) method.
    - guardrail_chat: Conduct a chat using Guardrail mechanism.

##### Example
```python
    # Stream the response asynchronously
    try:
        async for token in callback.aiter():
            yield token
    finally:
        callback.done.set()

    await task
```

- ## [`chat_agent/`]: 
This contains the codes for the CCL chat agent.

##### Example
```python
async def process_chat(agentExecutor, user_input, chat_history):
    async for event in agentExecutor.astream_events(
        {
            "input": user_input,
            "chat_history": chat_history
        },
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield content
```

- ## generate_letter:
This is the Module for generating formal letters using language models. 
It contains functions that generate a formal letter synchronously using parameters as context strings from the user.

##### Example:
```python
    def generate(self, context):
        """
        Generate a formal letter synchronously.

        Parameters:
            context (str): The context or content to include in the letter.

        Returns:
            str: The generated formal letter.
        """
        messages = [
            SystemMessage(content=LETTER_SYSTEM_PROMPT),
            HumanMessage(content=f"context: {context}"),
        ]

        result = self.llm(messages)
        return result.content

```
- ## [`generate_nda/`]:
This is the Module for generating Non-Disclosure Agreements (NDAs) using language models.

Classes:
    - GenerateNDA: A class for generating NDAs.

Functions:
    - handle_section: Handle a single section of the NDA synchronously.
    - handle_sections: Handle all sections of the NDA synchronously.
    - handle_sections_2: Handle all sections of the NDA asynchronously with streaming.

##### Example:
```python
    def __init__(self, model_name=MODEL_NAME, answers=None):
        """
        Initialize the GenerateNDA class.

        Parameters:
            model_name (str): The name of the language model to use. Default is the value from constants.
            answers (list): A list of answers to the NDA questions. Must match the number of questions.
        """
        questions = templates.prepare_questions()
        if len(questions) != len(answers):
            raise ValueError(
                "Number of answers supplied mismatch number of questions")
        self.questions_answers = {
            question: answer for question, answer in zip(questions, answers)
        }
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
        )

```

- ## [`generate_proposal/`]:
This is the Module for filling fields into text using LLM (Large Language Model).

Classes:
    - AutoFillTemplate: A class for filling fields in a template.

Functions:
    - fill_template: Fill fields in a template synchronously.
    - fill_fields: Fill fields in a template asynchronously with streaming.

##### Example:
```python
    def __init__(self, model_name="str"):
        """
        Initialize the AutoFillTemplate class.

        Parameters:
            model_name (str): The name of the language model to use.
        """
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
        )
```
- ## [`generate_proposal_2/`]:
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

##### Example
```python
    def stream_section_generation(self, chunk_size):
        """
        Generate the proposal section asynchronously with streaming.

        Parameters:
            chunk_size (int): The size of each chunk of text to yield.

        Yields:
            str: A chunk of the generated proposal section.
        """
        text = self.ts
        chunks = [text[i: i + chunk_size]
                  for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            yield chunk
```
- ## [`style_engine/`]:
Module for language style correction and interpretation based on an editorial style guide manual.

Classes:
    - StyleGuideParser: Pydantic BaseModel for parsing style guide suggestions.
    - StyleGuideParserV2: Pydantic BaseModel for parsing style guide suggestions (alternate version).
    - StyleGuide: A class for generating and managing style guide information.

Functions:
    - styleguide_modify_input: Modify input text based on style guide suggestions.

##### Example:
```python
    def read_style_guide_files(self, path: List[str]) -> Dict[str, str]:
        """
        Read and store contents of style guide files.

        Parameters:
            path (List[str]): List of file paths.

        Returns:
            Dict[str, str]: Dictionary containing file contents indexed by file path.
        """
        file_contents = {
            file_path: open(file_path, "r", encoding="utf8").read()
            for file_path in path
        }
        return file_contents

```
- ## [`tools/`]:
This contains tools for searching and returning questions concerning CypherCrescent also called CCL.

##### Example:
```python
def about_cyphercrescent(query):
    """Use this to tool to answer any question that relates Cyphercresect, also known as CCL"""
    retriever = initiate_index(id="1", store_client="chromadb", persist=True)
    docs = retriever.similarity_search(query)
    return docs

```