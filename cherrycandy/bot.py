from typing import List

from dico import Client
from dico_interaction import InteractionClient

from cherrycandy.utils.handler import Command, search_files, gather_commands
from cherrycandy.utils.language import LanguageManager


class CherryCandy(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interaction = InteractionClient(client=self, auto_register_commands=True)

        self.lang = LanguageManager("cherrycandy/data/lang.json")

        self.commands: List[Command] = []

    def add_commands(self) -> List[Command]:
        self.commands = gather_commands(
            self,
            search_files("cherrycandy/commands")
        )
        return self.commands
