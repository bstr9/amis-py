def is_default(value, default):
    if value is None and default is None:
        return True
    if value == default:
        return True
    return False
