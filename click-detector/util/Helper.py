def save_to_int(val, default=-1):
    try:
        return int(val)
    except(ValueError, TypeError):
        return default
