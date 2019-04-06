class DataNotUpdateException(Exception):
    """
    データをアップデートしてない時に投げる
    """
    def __init__(self, message=None):
        self.__message = message

    def get_message(self):
        return self.__message
