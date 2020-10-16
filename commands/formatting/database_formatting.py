from discord.guild import Guild
from discord.channel import TextChannel
from tinydb import TinyDB, where, Query

prefix_db = 'databases/prefixdb.json'
one_minute_cutoff_updates_db = 'databases/one_minute_cutoff_updates.json'
one_hour_cutoff_updates_db = 'databases/one_hour_cutoff_updates.json'
bot_updates_db = 'databases/bot_updates.json'

#######################
#     Bot Updates     #
#######################
def add_channel_to_bot_updates_db(channel: TextChannel):
    db = TinyDB(bot_updates_db)
    success = True
    try:
        db.upsert({'name': channel.name,
                   'guild': channel.guild.id,
                   'guildName': channel.guild.name,
                   'id': channel.id
                   }, where('id') == channel.id)
    except Exception as e:
        print(e)
        success = False

    if success:
        text = "Channel " + channel.name + \
            " will receive bot updates" 
    else:
        text = "Failed adding " + channel.name + \
            " to the bot updates list" 
    return text


def rm_channel_from_bot_updates_db(channel: TextChannel):
    db = TinyDB(bot_updates_db)
    success = True
    try:
        db.remove((where('id') == channel.id) & (
            where('guild') == channel.guild.id))
    except Exception as e:
        print(e)
        success = False

    if success:
        text = "Channel " + channel.name + \
            " removed from receiving bot updates" 
    else:
        text = "Failed removing " + channel.name + \
            " from receiving bot updates" 
    return text

#######################
#     T10 Updates     #
#######################
def add_channel_to_cutoff_db(channel: TextChannel, interval: int):
    success = True
    if(interval == 1):
            db = TinyDB(one_minute_cutoff_updates_db)
            interval = '1 minute'
    elif(interval == 60):
            db = TinyDB(one_hour_cutoff_updates_db)
            interval = '1 hour'        
    try:
        db.upsert({'name': channel.name,
                'guild': channel.guild.id,
                'guildName': channel.guild.name,
                'id': channel.id
                }, where('id') == channel.id)
    except Exception as e:
        print(e)
        success = False
    if success:
        text = f"Channel {channel.name} will receive {interval} updates"
    else:
        text = f"Failed adding {channel.name} to the {interval} tracking list" 
    return text

def rm_channel_from_cutoff_db(channel: TextChannel, interval: int):
    success = True
    if(interval == 1):
            db = TinyDB(one_minute_cutoff_updates_db)
            interval = '1 minute'
    elif(interval == 60):
            db = TinyDB(one_hour_cutoff_updates_db)
            interval = '1 hour'        
    try:
        db.remove((where('id') == channel.id) & (where('guild') == channel.guild.id))
    except Exception as e:
        print(e)
        success = False
    if success:
        text = f"Channel {channel.name} will stop receiving {interval} updates"
    else:
        text = f"Failed removing {channel.name} from the {interval} tracking list" 
    return text

def get_cutoff_updates_channels(interval: int):
    ids = list()
    if(interval == 1):
        db = TinyDB(one_minute_cutoff_updates_db)
    if(interval == 60):
        db = TinyDB(one_hour_cutoff_updates_db)
    try:
        saved = db.all()
        for i in saved:
            ids.append(i['id'])
    except Exception as e:
        print(e)
    return ids

##################
#     Misc       #
##################
def add_prefix_to_database(guild: Guild, prefix: str):
    success = True
    try:
        db = TinyDB(prefix_db)
        db.upsert({'id': guild.id,
                   'prefix': prefix
        }, where('id') == guild.id)
    except Exception as e:
        print(e)
        success = False

    if success:
        text = "Prefix " + prefix + " set for server " + str(guild.name)
    else:
        text = "Failed adding " + prefix + " to the prefix list"

    return text
