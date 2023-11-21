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
def get_conversation_prompts(sender_id: str, conversation_id):
    '''
    Get sender_id's coversation_id prompts
    '''

    result = get_prompts_from_conversation(
        user_id=sender_id,
        conversation_id=conversation_id
    )
    
    return result


@duration
def save_prompt(sender_id: str, coversation_id, prompt:PromptModel) -> bool:
    '''
    Saves prompt from sender_id to conversation_id
    '''

    result = add_prompt_to_conversation(
        user_id=sender_id,
        conversation_id=coversation_id,
        prompt=prompt
    )
    
    return result
    
