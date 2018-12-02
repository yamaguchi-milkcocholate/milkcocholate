class Order:

    def __init__(self, order_id, pair, side,
                 type, price, start_amount,
                 remaining_amount, executed_amount,
                 average_price, ordered_at, status
                 ):
        self.id = order_id
        self.pair = pair
        self.side = side
        self.type = type
        self.price = price
        self.start_amount = start_amount
        self.remaining_amount = remaining_amount
        self.executed_amount = executed_amount
        self.average_price = average_price
        self.ordered_at = ordered_at
        self.status = status
