class Order:

    def __init__(self, id, pair, side, type, price, amount, ordered_at, status):
        self.id = id
        self.pair = pair
        self.side = side
        self.type = type
        self.price = price
        self.amount = amount
        self.ordered_at = ordered_at
        self.status = status
