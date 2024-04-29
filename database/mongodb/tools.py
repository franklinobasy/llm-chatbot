"""
Module: database.mongodb.tools

The `tools.py` module provides functions for interacting with MongoDB collections, including user and conversation management.

Functions:
    - create_user_if_not_exists: Creates a new user if not already exists in the database.
    - create_conversation: Creates a new conversation for a user.
    - delete_conversation: Deletes a conversation for a user.
    - add_prompt_to_conversation: Adds a prompt to a conversation for a user.
    - get_user_conversations: Retrieves conversations for a user.
    - process_prompt: Processes a prompt to a readable format.
    - get_prompts_from_conversation: Retrieves prompts from a specific conversation for a user.

Usage:
    from database.mongodb.tools import (
        create_user_if_not_exists,
        create_conversation,
        delete_conversation,
        add_prompt_to_conversation,
        get_user_conversations,
        process_prompt,
        get_prompts_from_conversation,
    )

    # Example usage of functions
    create_user_if_not_exists(user_id="123")
    conversation_id = create_conversation(user_id="123")
    delete_conversation(user_id="123", conversation_id=conversation_id)
    add_prompt_to_conversation(user_id="123", conversation_id=conversation_id, prompt=prompt)
    conversations = get_user_conversations(user_id="123")
    processed_prompt = process_prompt(prompt)
    prompts = get_prompts_from_conversation(user_id="123", conversation_id=conversation_id)
"""
import logging
from pymongo.collection import Collection
from datetime import datetime
from uuid import uuid4
from typing import List
from database.mongodb import collection
from database.mongodb.models import PromptModel, ConversationModel, UserModel

def create_user_if_not_exists(user_id: str, collection: Collection = collection):
    """
    Creates a new user if not already exists in the database.

    Args:
        - user_id (str): The ID of the user.
        - collection (pymongo.collection.Collection): MongoDB collection to operate on.

    Returns:
        bool: True if user created, False if user already exists.
    """
    existing_user = collection.find_one({"user_id": user_id})
    if not existing_user:
        user_data = UserModel(user_id=user_id)
        collection.insert_one(user_data.model_dump())
        logging.info(f"User '{user_id}' created.")
        return True
    return False


def create_conversation(user_id: str, collection: Collection = collection) -> str:
    """
    Creates a new conversation for a user.

    Args:
        - user_id (str): The ID of the user.
        - collection (pymongo.collection.Collection): MongoDB collection to operate on.

    Returns:
        str: The ID of the created conversation.
    """
    conversation_id = uuid4().hex
    existing_user = collection.find_one({"user_id": user_id})

    if not existing_user:
        # If user doesn't exist, create the user
        create_user_if_not_exists(user_id, collection)

    current_time = datetime.utcnow()
    conversation_data = ConversationModel(
        date_created=current_time,
        date_modified=current_time,
        conversation_id=conversation_id,
        prompts=[],
    )
    collection.update_one(
        {"user_id": user_id},
        {"$push": {"conversations": conversation_data.model_dump()}},
    )
    logging.info(f"Conversation '{conversation_id}' added to user '{user_id}'.")
    return conversation_id


def delete_conversation(
    user_id: str, conversation_id: str, collection: Collection = collection
) -> bool:
    """
    Deletes a conversation for a user.

    Args:
        - user_id (str): The ID of the user.
        - conversation_id (str): The ID of the conversation to delete.
        - collection (pymongo.collection.Collection): MongoDB collection to operate on.

    Returns:
        bool: True if conversation deleted, False if user or conversation not found.
    """
    result = collection.update_one(
        {"user_id": user_id},
        {"$pull": {"conversations": {"conversation_id": conversation_id}}},
    )
    if result.modified_count > 0:
        logging.info(f"Conversation '{conversation_id}' deleted successfully.")
        return True
    else:
        logging.info(f"User '{user_id}' or conversation '{conversation_id}' not found.")
        return False


def add_prompt_to_conversation(
    user_id: str,
    conversation_id: str,
    prompt: PromptModel,
    collection: Collection = collection,
) -> bool:
    """
    Adds a prompt to a conversation for a user.

    Args:
        - user_id (str): The ID of the user.
        - conversation_id (str): The ID of the conversation.
        - prompt (PromptModel): The prompt to add.
        - collection (pymongo.collection.Collection): MongoDB collection to operate on.

    Returns:
        bool: True if prompt added, False if user or conversation not found.
    """
    current_time = datetime.utcnow()

    # Check if the user exists, create if not
    user_exists = collection.find_one({"user_id": user_id})
    if not user_exists:
        # Create a new user
        create_user_if_not_exists(user_id)

    # Check if the conversation exists for the user
    conversation_exists = collection.find_one(
        {"user_id": user_id, "conversations.conversation_id": conversation_id}
    )
    if not conversation_exists:
        # Add the conversation for the user
        conversation = ConversationModel(
            conversation_id=conversation_id,
            conversation_name=prompt.model_dump().get("question"),
            prompts=[prompt.model_dump()],
        )
        collection.update_one(
            {"user_id": user_id},
            {"$push": {"conversations": conversation.model_dump()}},
        )
        logging.info(f"Conversation '{conversation_id}' added to user '{user_id}'.")
        return True
    else:
        # Update conversation_name based on the new prompt's question
        new_conversation_name = prompt.model_dump().get("question")

        # Check if the current conversation_name is still "New conversation"
        for conv in conversation_exists["conversations"]:
            if (
                conv["conversation_id"] == conversation_id
                and conv["conversation_name"] == "New conversation"
            ):
                collection.update_one(
                    {
                        "user_id": user_id,
                        "conversations.conversation_id": conversation_id,
                    },
                    {
                        "$set": {
                            "conversations.$.conversation_name": new_conversation_name,
                            "conversations.$.date_modified": current_time,
                        },
                        "$push": {"conversations.$.prompts": prompt.model_dump()},
                    },
                )
                logging.info(
                    f"Conversation '{conversation_id}' updated with new prompt for user '{user_id}'."
                )
                return True

        # If the conversation is not "New conversation," add the prompt to the existing conversation
        collection.update_one(
            {"user_id": user_id, "conversations.conversation_id": conversation_id},
            {
                "$push": {"conversations.$.prompts": prompt.model_dump()},
                "$set": {"conversations.$.date_modified": current_time},
            },
        )
        logging.info(
            f"Prompt added to the existing conversation '{conversation_id}' for user '{user_id}'."
        )
        return True


def get_user_conversations(
    user_id: str, collection: Collection = collection
) -> List[ConversationModel]:
    """
    Retrieves conversations for a user.

    Args:
        - user_id (str): The ID of the user.
        - collection (pymongo.collection.Collection): MongoDB collection to operate on.

    Returns:
        List[ConversationModel]: List of ConversationModel objects.
    """
    user_data = collection.find_one({"user_id": user_id})
    if user_data:
        conversations = user_data.get("conversations", [])
        return [ConversationModel(**conv) for conv in conversations]
    else:
        logging.info(f"User '{user_id}' not found.")
        return []


def process_prompt(prompt: PromptModel) -> tuple:
    """
    Processes a prompt to a readable format.

    Args:
        - prompt (PromptModel): The prompt to process.

    Returns:
        tuple: A tuple containing the question and answer of the prompt.
    """
    prompt = prompt.model_dump()
    return (prompt["question"], prompt["answer"])


def get_prompts_from_conversation(
    user_id: str,
    conversation_id: str,
    collection: Collection = collection,
    use_model: bool = True,
) -> List[PromptModel]:
    """
    Retrieves prompts from a specific conversation for a user.

    Args:
        - user_id (str): The ID of the user.
        - conversation_id (str): The ID of the conversation.
        - collection (pymongo.collection.Collection): MongoDB collection to operate on.
        - use_model (bool): Whether to return prompts as PromptModel objects (default) or as processed tuples.

    Returns:
        List[PromptModel]: List of PromptModel objects if use_model is True, else list of processed tuples.
    """
    user_data = collection.find_one({"user_id": user_id})
    if user_data:
        conversations = user_data.get("conversations", [])
        target_conversation = next(
            (
                conv
                for conv in conversations
                if conv["conversation_id"] == conversation_id
            ),
            None,
        )
        if target_conversation:
            prompts = target_conversation.get("prompts", [])
            if use_model:
                return [PromptModel(**prompt) for prompt in prompts]
            return [process_prompt(PromptModel(**prompt)) for prompt in prompts]
        else:
            logging.info(
                f"Conversation '{conversation_id}' not found for user '{user_id}'."
            )
            return []
    else:
        logging.info(f"User '{user_id}' not found.")
        return []
