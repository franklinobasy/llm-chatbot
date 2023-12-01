# tools
from database.mongodb import collection
from database.mongodb.models import (
    PromptModel,
    ConversationModel,
    UserModel
)
from uuid import uuid4
import logging
from pymongo.collection import Collection
from datetime import datetime
from typing import List


def create_user_if_not_exists(user_id: str, collection: Collection=collection):
    existing_user = collection.find_one({"user_id": user_id})
    if not existing_user:
        user_data = UserModel(user_id=user_id)
        collection.insert_one(user_data.model_dump())
        logging.info(f"User '{user_id}' created.")
        return True
    return False


def create_conversation(user_id: str, collection: Collection = collection) -> str:
    """
    Create a new conversation for a user.

    :param user_id: User ID.
    :param collection: MongoDB collection.
    :return: Conversation ID if created, None if already exists.
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
        prompts=[]
    )
    collection.update_one(
        {"user_id": user_id},
        {"$push": {"conversations": conversation_data.model_dump()}}
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
        {"user_id": user_id},
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
    current_time = datetime.utcnow()

    # Check if the user exists, create if not
    user_exists = collection.find_one({"user_id": user_id})
    if not user_exists:
        # Create a new user
        create_user_if_not_exists(user_id)

    # Check if the conversation exists for the user
    conversation_exists = collection.find_one({"user_id": user_id, "conversations.conversation_id": conversation_id})
    if not conversation_exists:
        # Add the conversation for the user
        conversation = ConversationModel(
            conversation_id=conversation_id,
            conversation_name=prompt.model_dump().get("question"),
            prompts=[prompt.model_dump()]
        )
        collection.update_one(
            {"user_id": user_id},
            {"$push": {"conversations": conversation.model_dump()}}
        )
        logging.info(f"Conversation '{conversation_id}' added to user '{user_id}'.")
        return True
    else:
        # Update conversation_name based on the new prompt's question
        new_conversation_name = prompt.model_dump().get("question")
        
        # Check if the current conversation_name is still "New conversation"
        for conv in conversation_exists['conversations']:
            if conv['conversation_id'] == conversation_id and conv['conversation_name'] == "New conversation":
                collection.update_one(
                    {"user_id": user_id, "conversations.conversation_id": conversation_id},
                    {
                        "$set": {
                            "conversations.$.conversation_name": new_conversation_name,
                            "conversations.$.date_modified": current_time
                        },
                        "$push": {
                            "conversations.$.prompts": prompt.model_dump()
                        }
                    }
                )
                logging.info(f"Conversation '{conversation_id}' updated with new prompt for user '{user_id}'.")
                return True

        # If the conversation is not "New conversation," add the prompt to the existing conversation
        collection.update_one(
            {"user_id": user_id, "conversations.conversation_id": conversation_id},
            {
                "$push": {
                    "conversations.$.prompts": prompt.model_dump()
                },
                "$set": {
                    "conversations.$.date_modified": current_time
                }
            }
        )
        logging.info(f"Prompt added to the existing conversation '{conversation_id}' for user '{user_id}'.")
        return True


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
    user_data = collection.find_one({"user_id": user_id})
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
    user_data = collection.find_one({"user_id": user_id})
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
