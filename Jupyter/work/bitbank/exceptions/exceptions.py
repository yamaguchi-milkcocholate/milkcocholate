class SettingError(Exception):

    def __init__(self, message='Setting Error'):
        self.message = message

    def __str__(self):
        return self.message
