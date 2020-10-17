# Format time in Dd Hh Mm Ss format
async def format_time(seconds):
    days = int(seconds // 86400)
    hours = int(seconds // 3600 % 24)
    minutes = int(seconds // 60 % 60)
    seconds = int(seconds % 60)
    output = f"{days}d {hours}h {minutes}m {seconds}s"
    return output

# Format date in YYYY-MM-DD HH:MM:SS UTC format
async def format_date(seconds):
    from datetime import datetime
    date = datetime.fromtimestamp(seconds / 1000).strftime("%Y-%m-%d %H:%M:%S %Z%z") + ' CST'
    return date

async def format_progress(end_time, start_time, current_time):
    event_length = end_time - start_time
    time_left = end_time - current_time
    event_prog = round((((event_length - time_left) / event_length) * 100), 2)
    return f"{event_prog}%"

async def is_event_active(event_id):
    import time
    from commands.formatting.event_info import get_event_end_time
    current_time = time.time() * 1000
    event_end_time = await get_event_end_time(event_id)
    if current_time > event_end_time:
        return False
    else:
        return True
