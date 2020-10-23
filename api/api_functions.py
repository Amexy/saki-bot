import requests, json, aiohttp

async def get_sekai_current_event_standings_api(event_id):
    async with aiohttp.ClientSession() as session:
        from random import random
        # Use a random number to avoid caching issues 
        api = f'https://bitbucket.org/sekai-world/sekai-event-track/raw/main/event{event_id}.json?t={random()}'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_world_events_api():
    async with aiohttp.ClientSession() as session:
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_current_event_api():
    async with aiohttp.ClientSession() as session:
        api = 'https://sekaidb.xyz/l10n/event/en.json'
        async with session.get(api) as r:
            return await r.json()

async def get_sekai_master_api():
    async with aiohttp.ClientSession() as session:
        api = 'https://sekaidb.xyz/db/prod.json'
        async with session.get(api) as r:
            return await r.json()

async def get_sekai_events_api():
    async with aiohttp.ClientSession() as session:
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_event_deck_bonuses_api():
    async with aiohttp.ClientSession() as session:
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/eventDeckBonuses.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
   

1603219978749
1603219618762
1603220038751