from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time, re, asyncio

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite',
                      description='Posts the invite link for Sakibot')
    async def invite(self, ctx):
        await ctx.send('Step 1: Open https://discordapp.com/oauth2/authorize?client_id=766710147644915739&scope=bot&permissions=116736\nStep 2: Login to Discord if prompted\nStep 3: Select the server you wish to invite the bot to from the dropdown (required Admin privileges on the server)\nStep 4: Continue through the prompts as needed')

    @commands.command(name='reload',
                     description='In the event that the loops (in particular interval cutoff posting) stop working, run this command to restart that process. If you want access to this command, please use the .notify command')
    async def reload(self, ctx, cog: str = ''):
        if not cog: #By default, it will reload the Loops command since this is the most common one that fails and users need access to
            ValidUsers = [158699060893581313,766946395398995989,384333652344963074,222106235283963904]
            if ctx.message.author.id not in ValidUsers:
                await ctx.send("You are not authorized to use this command. If you'd like access, please use the .notify command requesting access")
            else: 
                for task in asyncio.Task.all_tasks():
                    if 'post' in str(task):
                        task.cancel()
                        print('Cancelled task ' + str(task._coro))
                try:
                    from commands.cogs.loops import loops
                    loops(self.bot)
                    c = self.bot.get_cog("loops")
                    self.bot.remove_cog(c)
                    self.bot.add_cog(c)
                    await ctx.send("Successfully reloaded the Loops cog")
                except:
                    await ctx.send("Failed reloading the Loops cog. Please use the `.notify` command to let Josh know")
        else:
            ValidUsers = [158699060893581313]
            if ctx.message.author.id not in ValidUsers:
                await ctx.send("You are not authorized to use this command. If you'd like access, please use the .notify command requesting access")
            else:
                try:
                    cog = f"commands.cogs.{cog}"
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                    await ctx.send(f"Successfully reloaded the {cog} cog")
                except:
                    await ctx.send(f"Failed reloading the {cog} cog.")


def setup(bot):
    bot.add_cog(misc(bot))
