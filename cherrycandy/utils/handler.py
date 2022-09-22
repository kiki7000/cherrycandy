from typing import List
from os import listdir
from importlib import import_module

from dico import ApplicationCommandOption


class Group:
    name: str
    description: str

    def get_sub_commands(self):
        sub_commands = []
        for func in map(lambda key: getattr(self, key), dir(self)):
            if "name" not in dir(func):
                continue
            sub_commands.append(func)


class Command:
    name: str
    description: str
    guild_id: str = None

    def __init__(self, bot):
        self.bot = bot
        self.groups = []

    def add_group(self, group: Group) -> None:
        self.groups.append(group)

    def get_groups(self):
        return self.groups

    def get_sub_commands(self):
        sub_commands = []
        for func in map(lambda key: getattr(self, key), dir(self)):
            if "name" not in dir(func):
                continue
            sub_commands.append(func)
        return sub_commands

    def get_base_command(self):
        base_command = None
        for func in map(lambda key: getattr(self, key), dir(self)):
            if "default_permission" not in dir(func):
                continue
            if "name" not in dir(func):
                base_command = func
                break
        return base_command

    def register_commands(self) -> None:
        base_command = self.get_base_command()
        if base_command is not None:
            self.bot.interaction.slash(
                name=self.name,
                description=self.description,
                options=base_command.options,
                default_permission=base_command.default_permission,
                guild_id=self.guild_id
            )(base_command)
        else:
            for subcommand in self.get_sub_commands():
                self.bot.interaction.slash(
                    name=self.name,
                    description=self.description,
                    subcommand=subcommand.name,
                    subcommand_description=subcommand.description,
                    options=subcommand.options,
                    default_permission=subcommand.default_permission,
                    guild_id=self.guild_id
                )(subcommand)

            for group in self.get_groups():
                for subcommand in group.get_sub_commands():
                    self.bot.interaction.slash(
                        name=self.name,
                        description=self.description,
                        subcommand_group=group.name,
                        subcommand_group_description=group.description,
                        subcommand=subcommand.name,
                        subcommand_description=subcommand.description,
                        options=subcommand.options,
                        default_permission=subcommand.default_permission,
                        guild_id=self.guild_id
                    )(sub_command)


def command(
    *,
    options: List[ApplicationCommandOption] = None,
    default_permission: bool = True,
):
    def wrap(coro):
        coro.options = options
        coro.default_permission = default_permission
        return coro
    return wrap


def sub_command(
    name: str = None,
    *,
    description: str = None,
    options: List[ApplicationCommandOption] = None,
    default_permission: bool = True,
):
    def wrap(coro):
        coro.name = name
        coro.description = description
        coro.options = options
        coro.default_permission = default_permission
        return coro
    return wrap


def search_files(base: str, end: str = ".py", ignore=None) -> List[List[str]]:
    if ignore is None:
        ignore = ["__pycache__", ".idea"]

    files = [
        [f"{base}/{x}", base]
        for x in filter(
            lambda x: x.endswith(end) and x not in ignore,
            listdir(base)
        )
    ]
    for f in filter(
        lambda x: "." not in x and x not in ignore,
        listdir(base)
    ):
        files.extend(search_files(f"{base}/{f}"))
    return files


def gather_commands(bot, files: List[List[str]]):
    commands = []
    for file in files:
        mod = import_module(file[0].rstrip(".py").replace("/", "."))
        if "get_command" not in dir(mod):
            cmd = mod.Command(bot)
            cmd.register_commands()
            commands.append(cmd)
        else:
            cmd = mod.get_command(bot)
            cmd.register_commands()
            commands.append(cmd)
    return commands
