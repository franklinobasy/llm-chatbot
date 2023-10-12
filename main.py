from api import app
from bot.bot import main
from chatbot import app as cli
# from outlook.tools import get_outlook_emails, export_sender_email


if __name__ == '__main__':
    # main(model="gpt-3.5-turbo-0301", load_history=False)
    # sender_email = "tomsguide@smartbrief.com"
    # emails = get_outlook_emails(sender_email)
    # export_sender_email(emails, format='xlsx')
    # print("Done")
    cli.start()
