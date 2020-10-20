async def get_current_event_id():
    import re
    from api.api_functions import get_sekai_world_events_api
    event_api = await get_sekai_world_events_api()
    return event_api[-1]['id']

async def get_event_name(event_id):
    from api.api_functions import get_sekai_events_api
    event_api = await get_sekai_events_api()
    event_name = event_api[-1]['name']
    return event_name

async def get_event_type(event_id):
    from api.api_functions import get_sekai_events_api
    event_api = await get_sekai_events_api()
    event_name = event_api[-1]['eventType'].capitalize()
    return event_name

async def get_event_start_time(event_id):
    from api.api_functions import get_sekai_events_api
    event_api = await get_sekai_events_api()
    event_start_time = event_api[-1]['startAt']
    return event_start_time

async def get_event_end_time(event_id):
    from api.api_functions import get_sekai_events_api
    event_api = await get_sekai_events_api()
    event_end_time = event_api[-1]['aggregateAt']
    return event_end_time

async def get_event_banner_name(event_id):
    from api.api_functions import get_sekai_events_api
    event_api = await get_sekai_events_api()
    event_banner_name = event_api[-1]['assetbundleName']
    return event_banner_name

async def get_event_bonus_attribute():
    from api.api_functions import get_sekai_event_deck_bonuses_api
    event_api = await get_sekai_event_deck_bonuses_api()
    event_bonus_attribute = event_api[-1]['cardAttr'].capitalize()
    return event_bonus_attribute
