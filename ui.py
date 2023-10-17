from textual.app import App
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.widgets import (
    Button,
    ContentSwitcher,
    Footer,
    Header,
    Input,
    Label,
)
from chatbot.auto_response.auto_response import process_prompt

from chatbot.generate_proposal.autofill import AutoFill


class ConversationBox(Label):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

    def render(self):
        return self.text


class OutputContainer(ScrollableContainer):
    ...


class InputContainer(Horizontal):
    def __init__(self, mode: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "send_button":
            if self.mode == "proposal":
                self.generate_proposal()
            elif self.mode == "automated_response":
                self.automated_respone()

    def compose(self):
        yield Input(
            placeholder="Tell me something to do...",
            id='input'
        )
        yield Button(
            "send",
            id="send_button",
            variant="success"
        )

    def generate_proposal(self):
        output_container = self.ancestors[0].query_one(OutputContainer)

        human_input = self.query_one(Input).value
        human_chat = ConversationBox(
            f"🤪You:\n{human_input}",
            classes="human-response"
        )

        f = AutoFill("gpt-3.5-turbo-0301")
        f.get_text()
        response = f.fill_text(human_input)

        ai_chat = ConversationBox(
            f"🤖Bot:\n{response}",
            classes="ai-response"
        )

        output_container.mount(human_chat)
        output_container.mount(ai_chat)

        self.query_one(Input).value = ""

    def automated_respone(self):
        output_container = self.ancestors[0].query_one(OutputContainer)

        human_input = self.query_one(Input).value
        human_chat = ConversationBox(
            f"🤪You:\n{human_input}",
            classes="human-response"
        )
        response = process_prompt("1", human_input, use_history=True)
        ai_chat = ConversationBox(
            f"🤖Bot:\n{response}",
            classes="ai-response"
        )

        output_container.mount(human_chat)
        output_container.mount(ai_chat)

        self.query_one(Input).value = ""


class ProposalContainer(Container):
    def compose(self):
        yield OutputContainer(id="conversation_area")
        yield InputContainer(mode="proposal")


class AutomatedResponseContainer(Container):
    def compose(self):
        yield OutputContainer(id="conversation_area")
        yield InputContainer(mode="automated_response")


class ChatBot(App):
    def compose(self):
        yield Header(show_clock=True, name="ChatBot")
        yield Footer()
        with Container():
            with Horizontal(id="buttons"):
                yield Button(
                    "Proposal Generation",
                    id="proposal-generation",
                    classes="switch-button",
                )
                yield Button(
                    "Chat",
                    id="chat",
                    classes="switch-button",
                )

            with ContentSwitcher(initial="proposal-generation"):
                yield ProposalContainer(id="proposal-generation")
                yield AutomatedResponseContainer(id="chat")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id in ['proposal-generation', 'chat']:
            if event.button.id == "proposal-generation'":
                event.button.add_class("active")
                event.button.ancestors[0].query_one(
                    "chat",
                    Button
                ).remove_class("active")
            elif event.button.id == "chat'":
                event.button.add_class("active")
                event.button.ancestors[0].query_one(
                    "proposal-generation",
                    Button
                ).remove_class("active")
            self.query_one(ContentSwitcher).current = event.button.id


if __name__ == "__main__":
    app = ChatBot(
        css_path="ui.css",
        watch_css=True
    )
    app.run()
