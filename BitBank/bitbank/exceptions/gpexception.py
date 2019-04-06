class NodeException(Exception):
    """
    何らかの問題でスケジュールをキャンセルするときの投げられる例外
    """
    def __init__(self, message=None):
        self.__message = message

    def get_message(self):
        return self.__message
