from datetime import timezone

def to_utc(ts):
    # Firestore timestamps are tz-aware in UTC; if not, enforce UTC
    if ts is None:
        return None
    if ts.tzinfo is None:
        return ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc)

def to_text_array(seq):
    return list(seq or [])
