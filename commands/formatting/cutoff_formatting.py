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
    event_name = await get_event_name(event_id)
    current_event_cutoff_api = await get_sekai_current_event_standings_api(event_id)
    last_updated_time = time.time() - (current_event_cutoff_api['time'] / 1000)
    last_updated_time = f"{await format_time(last_updated_time)} ago"
    #print(f"Current time: {time.time() * 1000}\nAPI Time: {current_event_cutoff_api['time']}")
    if tier == '0': # all cutoffs
        for x in current_event_cutoff_api: 
            if x != 'time':
                for y in current_event_cutoff_api[x]:
                    name = string_check(y['name'])
                    entries.append([
                        "{:,}".format(y['rank']),
                        "{:,}".format(y['score']),
                        y['userId'],
                        str(name)   
                    ])   
        output = ("```" + f"  Event: {event_name}\n  Time: {now_time.strftime(fmt)}\n  Last Updated: {last_updated_time}" + "\n\n" + tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"]) + "```")
        return output
    elif tier == '10':
        for x in current_event_cutoff_api['first10']:
            name = string_check(x['name'])
            entries.append([
                "{:,}".format(x['rank']),
                "{:,}".format(x['score']),
                x['userId'],
                str(name)   
            ])
        output = ("```" + f"  Event: {event_name}\n  Time: {now_time.strftime(fmt)}\n  Last Updated: {last_updated_time}" + "\n\n" + tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"]) + "```")
        return output
    elif f'rank{tier}' in current_event_cutoff_api:
        from commands.formatting.event_info import get_current_event_id,get_event_end_time, get_event_banner_name
        from api.api_functions import get_sekai_world_events_api
        event_banner_name = await get_event_banner_name(event_id)
        banner_url = f"https://sekai-res.dnaroma.eu/file/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"        
        event_id = await get_current_event_id()
        event_end_time = (await get_event_end_time(event_id)) / 1000
        current_time = time.time()
        if current_time > event_end_time:
            time_left = 'Event has ended'
        else:
            time_left = await format_time(event_end_time - current_time)
        event_url = f'https://sekai-world.github.io/sekai-viewer/#/event/{event_id}'
        embed=discord.Embed(title=f"{event_name} [t{tier}]", url=event_url, color=0x09d9fd)
        embed.set_thumbnail(url=banner_url)
        embed.add_field(name='Current', value="{:,}".format(current_event_cutoff_api[f'rank{tier}'][0]['score']), inline=True)
        embed.add_field(name='Player', value=current_event_cutoff_api[f'rank{tier}'][0]['name'], inline=True)
        embed.add_field(name='ID', value=current_event_cutoff_api[f'rank{tier}'][0]['userId'], inline=True)
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
