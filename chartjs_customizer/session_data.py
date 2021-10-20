session_data = {}


def add(session_id, val):
    session_data[session_id] = val


def get(session_id):
    return session_id
