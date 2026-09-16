import uuid


def generate_uuid():
    """
    Generate a UUID4 value.
    """
    return uuid.uuid4()


def generate_uuid_string():
    """
    Generate a UUID4 string.
    """
    return str(uuid.uuid4())


def is_valid_uuid(value):
    """
    Check whether a value is a valid UUID.
    """

    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError, AttributeError):
        return False
