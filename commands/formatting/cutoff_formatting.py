from datetime import datetime,timedelta
from pytz import timezone
from tabulate import tabulate
import re, time, discord

async def get_cutoff_formatting(tier: str = '0'):
    from api.api_functions import get_sekai_current_event_standings_api, get_sekai_current_event_api
    from commands.formatting.event_info import get_event_name, get_current_event_id
    from commands.formatting.time_formatting import format_time
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_time = datetime.now(timezone('US/Central'))
    entries = []
    event_id = await get_current_event_id()
    event_api = await get_sekai_current_event_api()
    event_name = await get_event_name(event_id)
    current_event_cutoff_api = await get_sekai_current_event_standings_api()
    last_updated_time = time.time() - current_event_cutoff_api['time'] 
    last_updated_time = f"{await format_time(last_updated_time)} ago"
    if tier == '0': # all cutoffs
        for x in current_event_cutoff_api: # subtract 1 because we don't care about the 'time' key for this
            if x != 'time':
                name = string_check(current_event_cutoff_api[x]['name'])
                entries.append([
                    "{:,}".format(int(x)),
                    "{:,}".format(current_event_cutoff_api[x]['score']),
                    current_event_cutoff_api[x]['userId'],
                    str(name)   
                ])
        output = ("```" + f"  Event: {event_name}\n  Time: {now_time.strftime(fmt)}\n  Last Updated: {last_updated_time}" + "\n\n" + tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"]) + "```")
        return output
    
    elif tier in current_event_cutoff_api:
        from commands.formatting.event_info import get_current_event_id
        from api.api_functions import get_sekai_master_api
        master_api = await get_sekai_master_api()
        banner_url = f"https://sekai-res.dnaroma.eu/file/sekai-assets/event/{master_api['events'][0]['assetbundleName']}/logo_rip/logo.webp"
        event_id = await get_current_event_id()
        time_left = await format_time((master_api['events'][0]['closedAt'] / 1000)- time.time())
        event_url = f'https://sekai-world.github.io/sekai-viewer/#/event/{event_id}'
        embed=discord.Embed(title=event_name, url=event_url, color=0x09d9fd)
        embed.set_thumbnail(url=banner_url)
        embed.add_field(name='Current', value="{:,}".format(current_event_cutoff_api[tier]['score']), inline=True)
        embed.add_field(name='Player', value=current_event_cutoff_api[tier]['name'], inline=True)
        embed.add_field(name='ID', value=current_event_cutoff_api[tier]['userId'], inline=True)
        embed.add_field(name='Last Updated', value=last_updated_time, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='Time Left', value=time_left, inline=True)
        embed.set_footer(text=f"{now_time.strftime(fmt)}")
        return embed

def string_check(string: str):
    import re
    string = string.replace('```','')
    string = string.replace("?",'')
    string = re.sub('(\[(\w{6}|\w{2})\])','', string)
    string = re.sub('\[([CcIiBbSsUu]|(sup|sub){1})\]', '', string) 
    return string
