from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time, re, discord


class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='timeleft',
                      aliases=['tl'],
                      description="Provides the amount of time left (in hours) for an event",
                      help=".timeleft")
    async def time_left(self, ctx):
        from commands.formatting.event_info import get_event_end_time, get_current_event_id, get_event_name, \
            get_event_start_time, get_event_banner_name
        from commands.formatting.time_formatting import format_time, format_date, format_progress
        event_id = await get_current_event_id()
        event_end_time = (await get_event_end_time(event_id)) / 1000
        current_time = time.time()
        if current_time > event_end_time:
            await ctx.send("There's no active event")
        else:
            event_end_date = await format_date(event_end_time * 1000)
            event_name = await get_event_name(event_id)
            event_start_time = await get_event_start_time(event_id)
            event_banner_name = await get_event_banner_name(event_id)
            banner_url = f"https://sekai-res.dnaroma.eu/file/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
            event_url = f'https://sekai-world.github.io/sekai-viewer/#/event/{event_id}'
            time_left = await format_time(event_end_time - current_time)
            event_prog = await format_progress(event_end_time, (event_start_time / 1000), current_time)
            embed = discord.Embed(title=event_name, url=event_url, color=0x09d9fd)
            embed.set_thumbnail(url=banner_url)
            embed.add_field(name='Time Left', value=time_left, inline=True)
            embed.add_field(name='Progress', value=event_prog, inline=True)
            embed.add_field(name='End Date', value=event_end_date, inline=True)
            await ctx.send(embed=embed)

    @commands.command(name='event',
                      description='Posts event info',
                      help='event\n.event jp\n.event en 12\n.event en Lisa\n.event jp 一閃')
    async def event(self, ctx, event_id=0):
        from commands.formatting.event_info import get_event_name, get_event_type, get_current_event_id, \
            get_event_bonus_attribute, get_event_banner_name, get_event_start_time, get_event_end_time
        from commands.formatting.time_formatting import format_date
        if event_id == 0:
            event_id = await get_current_event_id()
        event_name = await get_event_name(event_id)
        event_type = await get_event_type(event_id)
        event_banner_name = await get_event_banner_name(event_id)
        event_bonus_attribute = await get_event_bonus_attribute()
        event_start_time = await format_date(await get_event_start_time(event_id))
        event_end_time = await format_date(await get_event_end_time(event_id))
        banner_url = f"https://sekai-res.dnaroma.eu/file/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
        event_url = f'https://sekai-world.github.io/sekai-viewer/#/event/{event_id}'
        embed = discord.Embed(title=event_name, url=event_url, color=0x09d9fd)
        embed.set_thumbnail(url=banner_url)
        embed.add_field(name='Attribute', value=str(event_bonus_attribute), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='Event Type', value=str(event_type), inline=True)
        embed.add_field(name='Start', value=event_start_time, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='End', value=event_end_time, inline=True)
        await ctx.send(embed=embed)

    valid_tiers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000, 10000, 20000,
                   30000, 40000, 50000, 100000}

    @commands.command(name='cutoff',
                      brief="cutoff info",
                      description="Posts cutoff info",
                      help=".cutoff (posts cutoff info for all tiers)\n.cutoff 100",
                      aliases=[f't{tier}' for tier in valid_tiers] +
                              [f't{tier // 1000}k' for tier in valid_tiers if tier % 1000 == 0])
    async def cutoff(self, ctx, tier='0'):
        command_name = ctx.invoked_with.lower()
        tier_regex = re.compile(r"t?\d+k?")

        def parse_tier(tier_arg):
            if tier_arg[0] == 't':
                tier_arg = tier_arg[1:]
            if tier_arg[-1] == 'k':
                return 1000 * int(tier_arg[:-1])
            return int(tier_arg)

        if tier_regex.fullmatch(command_name):
            if tier != '0':
                await ctx.send(f"Tier already specified via alias")
                return
            tier = parse_tier(command_name)
        else:
            if not tier_regex.fullmatch(tier):
                await ctx.send(f"Tier `{tier}` isn't recognized")
                return
            tier = parse_tier(tier)

        from commands.formatting.cutoff_formatting import get_cutoff_formatting

        if tier == 0 or tier == 10:
            await ctx.send(await get_cutoff_formatting(str(tier)))
        elif tier in self.valid_tiers:
            await ctx.send(embed=await get_cutoff_formatting(str(tier)))
        else:
            await ctx.send(f"Tier `{tier}` isn't supported")


def setup(bot):
    bot.add_cog(event(bot))
