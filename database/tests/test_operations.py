# test_combined.py
import pytest
from datetime import datetime
from pymongo import MongoClient
from database.mongodb.tools import (
    create_conversation,
    create_user_if_not_exists,
    delete_conversation,
    add_prompt_to_conversation,
    get_user_conversations,
    get_prompts_from_conversation
)
from database.mongodb.models import UserModel, ConversationModel, PromptModel

@pytest.fixture(scope="module")
def test_collection():
    # Setup: Create a test MongoDB collection and return it
    test_client = MongoClient('localhost', 27017)
    test_db = test_client['test_db']
    test_collection = test_db['test_collection']
    yield test_collection
    # Teardown: Drop the test collection after tests
    test_db.drop_collection('test_collection')

def test_create_user_if_not_exists(test_collection):
    user_id = "test_user_id"
    result = create_user_if_not_exists(user_id, collection=test_collection)
    assert result

def test_create_conversation(test_collection):
    user_id = "test_user_id"
    conversation_id = create_conversation(user_id, collection=test_collection)
    assert conversation_id is not None

def test_delete_conversation(test_collection):
    user_id = "test_user_id_delete"
    conversation_id = create_conversation(user_id, collection=test_collection)
    result = delete_conversation(user_id, conversation_id, collection=test_collection)
    assert result

def test_add_prompt_to_conversation(test_collection):
    user_id = "test_user_id_prompt"
    conversation_id = create_conversation(user_id, collection=test_collection)
    prompt = PromptModel(question="Test question", answer="Test answer")
    result = add_prompt_to_conversation(user_id, conversation_id, prompt, collection=test_collection)
    assert result

def test_get_user_conversations(test_collection):
    user_id = "test_user_id_get"
    create_conversation(user_id, collection=test_collection)
    conversations = get_user_conversations(user_id, collection=test_collection)
    assert len(conversations) == 1

def test_get_prompts_from_conversation(test_collection):
    user_id = "test_user_id_prompts"
    conversation_id = create_conversation(user_id, collection=test_collection)
    prompt1 = PromptModel(question="Question 1", answer="Answer 1")
    prompt2 = PromptModel(question="Question 2", answer="Answer 2")
    add_prompt_to_conversation(user_id, conversation_id, prompt1, collection=test_collection)
    add_prompt_to_conversation(user_id, conversation_id, prompt2, collection=test_collection)

    prompts = get_prompts_from_conversation(user_id, conversation_id, collection=test_collection)
    assert len(prompts) == 2
    assert prompts[0].question == "Question 1"
    assert prompts[1].answer == "Answer 2"
