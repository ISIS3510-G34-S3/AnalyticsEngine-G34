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

def ref_to_id(v):

    if isinstance(v, str):
        return v
    
    if hasattr(v, "id"):
        try:
            return v.id  
        except Exception:
            pass
    return v 