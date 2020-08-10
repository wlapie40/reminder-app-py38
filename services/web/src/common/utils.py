import uuid


def generate_uuid4_hex():
    id = uuid.uuid4()
    return id.hex
