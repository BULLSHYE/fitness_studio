from datetime import datetime
import pytz

def convert_to_timezone(dt: datetime, target_tz: str = "Asia/Kolkata") -> datetime:
    local = pytz.timezone("Asia/Kolkata")
    local_dt = local.localize(dt)
    return local_dt.astimezone(pytz.timezone(target_tz))
