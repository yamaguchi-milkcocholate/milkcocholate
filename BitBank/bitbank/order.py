from datetime import datetime


class Order:

    def __init__(self, order_id, pair, side,
                 type, price, start_amount,
                 remaining_amount, executed_amount,
                 average_price, ordered_at, status
                 ):
        self.order_id = order_id
        self.pair = pair
        self.side = side
        self.type = type
        self.price = price
        self.start_amount = start_amount
        self.remaining_amount = remaining_amount
        self.executed_amount = executed_amount
        self.average_price = average_price
        self.ordered_at = datetime.fromtimestamp(
            ordered_at / 1000).strftime("%Y-%m-%d %H:%M:%S")
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "pair": self.pair,
            "side": self.side,
            "type": self.type,
            "price": self.price,
            "start_amount": self.start_amount,
            "remaining_amount": self.remaining_amount,
            "executed_amount": self.executed_amount,
            "average_price": self.average_price,
            "ordered_at": self.ordered_at,
            "status": self.status
        }
