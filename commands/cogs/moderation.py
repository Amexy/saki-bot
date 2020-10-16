from discord.ext import commands
from discord.guild import Guild

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setprefix',
                      description='Sets the command prefix the bot will use',
                      help='Example: .setprefix !')
    async def setprefix(self, ctx, prefix: str):
        from commands.formatting.database_formatting import add_prefix_to_database
        if ctx.message.author.guild_permissions.administrator:
            guild = ctx.message.guild
            await ctx.send(add_prefix_to_database(guild, prefix))
        else:
            msg = "You must have administrator rights to run this command, {0.author.mention}".format(
                ctx.message)
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(moderation(bot))
