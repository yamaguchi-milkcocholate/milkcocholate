from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError


class Line:

    def __init__(self):
        self.__line_bot_api = LineBotApi(
            'njVitXZSTHy/Kam5LO3tuGqasFta64atLoKj9bZGghEiHVFZQodrC5aQk6y8l2vQqIxM4JS0PJnmBdBALwquQ7LLRCS6CtnKYo+zMFFyCjYOhBdn0kVQx4MBA7/Bd7eJE1lG1d/jpYzFdIQfLfITZgdB04t89/1O/w1cDnyilFU='
        )

    def __call__(self, message):
        try:
            self.__line_bot_api.push_message('Uf96c8ff138dc3342aeb28971fc481881', TextSendMessage(text=message))
        except LineBotApiError as e:
            print(e.message)
