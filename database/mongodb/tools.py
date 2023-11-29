# tools
from database.mongodb import collection

from database.mongodb.models import (
    PromptModel,
    ConversationModel
)

from uuid import uuid4
import logging
from pymongo.collection import Collection
from datetime import datetime
from typing import List


def create_conversation(
    user_id: str,
    collection: Collection = collection
) -> str:
    """
    Create a new conversation for a user.

    :param user_id: User ID.
    :param collection: MongoDB collection.
    :return: Conversation ID if created, None if already exists.
    """
    conversation_id = uuid4().hex
    existing_user = collection.find_one({"_id": user_id})
    if not existing_user:
        current_time = datetime.utcnow()
        conversation_data = ConversationModel(
            date_created=current_time,
            date_modified=current_time,
            conversation_id=conversation_id,
            prompts=[]
        )
        collection.insert_one({
            "_id": user_id,
            "conversations": [conversation_data.model_dump()]
        })
        return conversation_id
    else:
        collection.update_one(
            {"_id": user_id},
            {"$push": {"conversations": {
                "conversation_id": conversation_id,
                "date_created": datetime.utcnow(),
                "date_modified": datetime.utcnow(),
                "prompts": []
            }}}
        )
        logging.info(f"Conversation '{conversation_id}' added to user '{user_id}'.")
        return conversation_id


def delete_conversation(
    user_id: str,
    conversation_id: str,
    collection: Collection = collection
) -> bool:
    """
    Delete a conversation for a user.

    :param user_id: User ID.
    :param conversation_id: Conversation ID.
    :param collection: MongoDB collection.
    :return: True if deleted, False if not found.
    """
    result = collection.update_one(
        {"_id": user_id},
        {"$pull": {"conversations": {"conversation_id": conversation_id}}}
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
    collection: Collection = collection
) -> bool:
    """
    Add a prompt to a conversation for a user.

    :param user_id: User ID.
    :param conversation_id: Conversation ID.
    :param prompt: PromptModel.
    :param collection: MongoDB collection.
    :return: True if added, False if user or conversation not found.
    """
    # Check if the user exists, create if not
    user_exists = collection.find_one({"_id": user_id})
    if not user_exists:
        # Create a new user
        user_data = {
            "_id": user_id,
            "conversations": [{
                "conversation_id": conversation_id,
                "date_created": datetime.utcnow(),
                "date_modified": datetime.utcnow(),
                "prompts": [prompt.model_dump()]
            }]
        }
        collection.insert_one(user_data)
        logging.info(f"User '{user_id}' created.")
        return True

    # Check if the conversation exists for the user
    conversation_exists = collection.find_one({"_id": user_id, "conversations.conversation_id": conversation_id})
    if not conversation_exists:
        # Add the conversation for the user
        collection.update_one(
            {"_id": user_id},
            {"$push": {"conversations": {
                "conversation_id": conversation_id,
                "date_created": datetime.utcnow(),
                "date_modified": datetime.utcnow(),
                "prompts": [prompt.model_dump()]
            }}}
        )
        logging.info(f"Conversation '{conversation_id}' added to user '{user_id}'.")
        return True

    # Add prompt to the existing conversation
    result = collection.update_one(
        {"_id": user_id, "conversations.conversation_id": conversation_id},
        {
            "$push": {
                "conversations.$.prompts": prompt.model_dump()
            },
            "$set": {
                "conversations.$.date_modified": datetime.utcnow()
            }
        }
    )

    if result.modified_count > 0:
        logging.info("Prompt added to the conversation.")
        return True
    else:
        logging.error(f"User '{user_id}' or conversation '{conversation_id}' not found.")
        return False


def get_user_conversations(
    user_id: str,
    collection: Collection = collection
) -> List[ConversationModel]:
    """
    Get conversations for a user.

    :param user_id: User ID.
    :param collection: MongoDB collection.
    :return: List of ConversationModel.
    """
    user_data = collection.find_one({"_id": user_id})
    if user_data:
        conversations = user_data.get("conversations", [])
        return [ConversationModel(**conv) for conv in conversations]
    else:
        logging.info(f"User '{user_id}' not found.")
        return []


def process_prompt(prompt: PromptModel) -> tuple:
    '''process prompt to readable format'''
    prompt = prompt.model_dump()
    return (prompt["question"], prompt["answer"])


def get_prompts_from_conversation(
    user_id: str,
    conversation_id: str,
    collection: Collection = collection,
    use_model: bool = True,
) -> List[PromptModel]:
    """
    Get all prompts from a specific conversation for a user.

    :param user_id: User ID.
    :param conversation_id: Conversation ID.
    :param collection: MongoDB collection.
    :return: List of PromptModel.
    """
    user_data = collection.find_one({"_id": user_id})
    if user_data:
        conversations = user_data.get("conversations", [])
        target_conversation = next((conv for conv in conversations if conv["conversation_id"] == conversation_id), None)
        if target_conversation:
            prompts = target_conversation.get("prompts", [])
            if use_model:
                return [PromptModel(**prompt) for prompt in prompts]
            return [process_prompt(PromptModel(**prompt)) for prompt in prompts]
        else:
            logging.info(f"Conversation '{conversation_id}' not found for user '{user_id}'.")
            return []
    else:
        logging.info(f"User '{user_id}' not found.")
        return []
