from chatbot_v2.ai.style_engine import StyleGuide

style_guide = StyleGuide()
chain = style_guide.styleguide_modify_input()

while True:
    prompt = input("User 🤪: ")
    print("Bot 🤖:", end="")
    for chunk in chain.stream({"input": prompt}):
        print(chunk.content, end="")
    print()
