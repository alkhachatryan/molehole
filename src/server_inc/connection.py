from .state import State

# Connection class to manage client-specific properties
class Connection:
    def __init__(self, sid, initial_path):
        self.sid = sid
        self.state = State(current_path=initial_path)