from cherrycandy.utils.handler import Command, command


class Test(Command):
    name = "test"
    description = "시녕바부"
    guild_id = "457841749197586438"

    @command()
    async def base(self, ctx):
        await ctx.send("응애")


def get_command(bot):
    return Test(bot)
