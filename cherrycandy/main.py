from cherrycandy.bot import CherryCandy

from dico import Ready

from dotenv import load_dotenv
from os import getenv

from termcolor import colored


load_dotenv()
token = getenv("BOT_TOKEN")

bot = CherryCandy(token)

bot.add_commands()


@bot.on("ready")
async def on_ready(event: Ready):
    print(
        f"""
        +=======================================================================+
        |  Bot ID:     {colored(event.user.id, 'green').ljust(65)} |
        |  Bot Name:   {colored(event.user.username, 'green').ljust(65)} |
        |  Bot Token:  {colored(token[:20], 'green').ljust(65)} |
        +=======================================================================+
        """
    )

bot.run()
