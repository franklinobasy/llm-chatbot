from utilities import duration

from database.mongodb.models import PromptModel
from database.mongodb.tools import (
    add_prompt_to_conversation,
    create_conversation,
    delete_conversation,
    get_prompts_from_conversation,
    get_user_conversations
)

@duration
def get_conversation_prompts(sender_id: str, conversation_id, k=2):
    """
    Get the latest prompts for the specified user and conversation.

    Parameters:
    - sender_id (str): The ID of the user.
    - conversation_id: The ID of the conversation.
    - k (int, optional): The number of latest prompts to retrieve (default is 2).

    Returns:
    list: A list of PromptModel objects representing the retrieved prompts.
    """
    result = get_prompts_from_conversation(
        user_id=sender_id,
        conversation_id=conversation_id,
        use_model=False
    )
    if k and len(result) > k:
        return result[-k:]
    return result

@duration
def save_prompt(sender_id: str, conversation_id, prompt: PromptModel) -> bool:
    """
    Save a prompt from a user to the specified conversation.

    Parameters:
    - sender_id (str): The ID of the user sending the prompt.
    - conversation_id: The ID of the conversation to which the prompt will be added.
    - prompt (PromptModel): The PromptModel object representing the prompt to be saved.

    Returns:
    bool: True if the prompt was successfully saved, False otherwise.
    """
    result = add_prompt_to_conversation(
        user_id=sender_id,
        conversation_id=conversation_id,
        prompt=prompt
    )
    return result
