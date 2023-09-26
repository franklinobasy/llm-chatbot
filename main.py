from bot.bot import main
from api import app

if __name__ == '__main__':
    main(model="gpt-3.5-turbo-0301", load_history=False)
