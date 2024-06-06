# status_handler.py
class StatusHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StatusHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'status'):
            self.status = "READY"

    def set_status(self, new_status):
        self.status = new_status

    def get_status(self):
        return self.status
