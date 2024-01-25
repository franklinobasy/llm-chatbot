from chatbot_v2.ai.chat import doc_chat

while True:
    prompt = input("User 🤪: ")
    answer = doc_chat(
        user_id="2",
        conversation_id="1",
        prompt=prompt,
        record_chat=True,
        stream=True
    )
    print(f"bot 🤖: {answer}")
