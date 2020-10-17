from discord.ext import commands
from discord import TextChannel

class updates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #################
    #  Bot Updates  #
    #################
    @commands.command(name='addbotupdates',
                      aliases=['abu'],
                      description="(Requires Admin Privileges) Given a channel input, this channel will receive bot updates/notifications",
                      help="You can specify either the channel's id, or by using the full channel name (e.g. #sakibot-updates\n\n.addbotupdates (defaults to channel the command was ran in\n.abu #sakibot-updates")
    async def addbotupdates(self, ctx, channel: TextChannel = None):
        from commands.formatting.database_formatting import add_channel_to_bot_updates_db
        if ctx.message.author.guild_permissions.administrator:
            if(channel == None):
                channel = ctx.channel
            await ctx.send(add_channel_to_bot_updates_db(channel))
        else:
            msg = "You must have administrator rights to run this command, {0.author.mention}".format(ctx.message)  
            await ctx.send(msg)
            
    @commands.command(name='removebotupdates',
                      aliases=['rbu'],
                      description="(Requires Admin Privileges) Given a channel input, this channel will receive bot updates/notifications",
                      help="You can specify either the channel's id, or by using the full channel name (e.g. #lisabot-updates\n\n.addbotupdates (defaults to channel the command was ran in\n.abu #lisabot-updates")
    async def removebotupdates(self, ctx, channel: TextChannel = None):
        from commands.formatting.database_formatting import rm_channel_from_bot_updates_db
        if ctx.message.author.guild_permissions.administrator:
            if(channel == None):
                channel = ctx.channel
            await ctx.send(rm_channel_from_bot_updates_db(channel))
        else:
            msg = "You must have administrator rights to run this command, {0.author.mention}".format(
                ctx.message)
            await ctx.send(msg)
            
    #######################
    #   Cutoff Commands   #
    #######################
    @commands.command(name='addtracking',
                      description="Given a channel and interval (1min or 1hour), this channel will receive cutoff updates in regular intervals",
                      help="You can specify either the channel's id, or by using the full channel name (e.g. #1min)\n\n.addtracking #1min-updates 1\n.addtracking 523339468229312555 60\n.addtracking (this defaults to 1 hour and channel the command is ran in)")
    async def add_cutoff_tracking(self, ctx, channel: TextChannel = None, interval: int = 60):
        from commands.formatting.database_formatting import add_channel_to_cutoff_db
        if ctx.message.author.guild_permissions.administrator:
            ValidIntervals = [1,60]
            if interval not in ValidIntervals:
                await ctx.send('Please enter a value of 1 for 1 minute updates or 60 for hourly updates')
            else:

                if(channel == None):
                    channel = ctx.channel
                await ctx.send(add_channel_to_cutoff_db(channel, interval))
        else:
            msg = "You must have administrator rights to run this command, {0.author.mention}".format(ctx.message)  
            await ctx.send(msg)
    
    @commands.command(name='removetracking',
                      description="Given a channel, interval (1min or 1hour), and server input, this channel will be removed from cutoff tracking updates",
                      help="You can specify either the channel's id, or by using the full channel name (e.g. #1min)\n\n.removetracking #1min-updates 2\n.removetracking 523339468229312555 60\n.removetracking (this defaults to 1 hour and channel the command is ran in")
    async def rm_cutoff_tracking(self, ctx, channel: TextChannel = None, interval: int = 60):
        from commands.formatting.database_formatting import rm_channel_from_cutoff_db
        if ctx.message.author.guild_permissions.administrator:
            ValidIntervals = [1,60]
            if interval not in ValidIntervals:
                await ctx.send('Please enter a value of 1 for 1 minute updates or 60 for hourly updates')
            else:
                if(channel == None):
                    channel = ctx.channel
            await ctx.send(rm_channel_from_cutoff_db(channel, interval))
        else:
            msg = "You must have administrator rights to run this command, {0.author.mention}".format(ctx.message)  
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(updates(bot))