from chatbot.auto_response.auto_response import process_prompt
from chatbot.auto_response.prompts import AVAILABLE_PROMPTS
from chatbot.config.instructions import (
    APPLICATION_START_INSTRUCTIONS,
)
from chatbot.generate_proposal.autofill import AutoFill
from chatbot.generate_proposal.auto_fields import AutoField


# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class CLI():
    '''
    Command Line Interface for chatbot
    '''

    __RUNNING = True
    AUTOMATED_RESPONSE_RUNNNING = False
    AUTOMATED_PROPOSAL_GENERATING = False

    def automated_respone(self):
        def stdin_check(prompt):
            if prompt == "c":
                self.AUTOMATED_RESPONSE_RUNNNING = False
            elif prompt == "":
                print(RED + "❌ No command received" + RESET)
            else:
                response = process_prompt("1", prompt, use_history=True)
                print(response)

        while self.AUTOMATED_RESPONSE_RUNNNING:
            print("Enter 'c' to close the Auto Response\n")
            prompt = input(YELLOW + "Question: " + RESET)
            stdin_check(prompt)

    def generate_proposal(self):
        def user_flow(d, item):
            if item[1] == str():
                _input = input("\t" + item[0] + ": ")
                d[item[0]] = _input
            elif item[1] == list():
                print(f"Provide a list of {item[0]}")
                _input = ""
                i = 1
                while True:
                    if _input.lower() == "done":
                        break

                    _input = input(f"\t{i}. {item[0]}: ")
                    if _input != "done":
                        d[item[0]].append(_input)
                    i += 1

        def stdin_check(prompt):
            if prompt == "c":
                self.AUTOMATED_PROPOSAL_GENERATING = False
            elif prompt == "":
                print(RED + "❌ No command received" + RESET)
            else:
                f = AutoFill("gpt-3.5-turbo-0301")
                f.get_text()
                print(f.fill_text(prompt))

        while self.AUTOMATED_PROPOSAL_GENERATING:
            prompt = input("Please provide a context for the proposal you want to generate: ")
            stdin_check(prompt)

    def stdin_check(self, stdin):
        if stdin == "quit":
            self.__RUNNING = False
            print(RED + "🔴 Application stopped!" + RESET)
        elif stdin == "":
            print(RED + "❌ No command received" + RESET)
        elif stdin not in ["1", "2"]:
            print(RED + "❌ Invalid command received" + RESET)
        else:
            if stdin == "1":
                self.AUTOMATED_RESPONSE_RUNNNING = True
                self.automated_respone()
            elif stdin == "2":
                # print(BLUE + "😥 Sorry, This feature is coming soon!" + RESET)
                self.AUTOMATED_PROPOSAL_GENERATING = True
                self.generate_proposal()

    def start(self):
        while self.__RUNNING:
            print(GREEN + APPLICATION_START_INSTRUCTIONS + RESET)
            stdin = input(YELLOW + "🤖 :: " + RESET)
            self.stdin_check(stdin)
