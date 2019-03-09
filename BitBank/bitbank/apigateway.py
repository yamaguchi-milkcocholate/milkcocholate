import python_bitbankcc


class ApiGateway:
    """
    BitBankのAPIをたたいて情報を取り出すクラス
    """

    def __init__(self, api_key=None, api_secret=None):
        self.__pub = python_bitbankcc.public()
        self.__pri = None
        if api_key is not None and api_secret is not None:
            self.__pri = python_bitbankcc.private(
                api_key=api_key, api_secret=api_secret
            )

    def use_depth(self, pair):
        """
        BitBankの板情報
        :param pair:
        :return: dict
        {
            asks: [
                [価格, 数量],
            ],

            bids: [
                [価格, 数量],
            ],
        }
        """
        return self.__pub.get_depth(pair)

    def use_ticker(self, pair):
        """
        BitBankのティッカー
        :return: dict ティッカー
        {
            "sell": "string",
            "buy": "string",
            "high": "string",
            "low": "string",
            "last": "string",
            "vol": "string",
            "timestamp": 0
          }
        """
        return self.__pub.get_ticker(pair)

    def use_candlestick(self, pair, candle_type, time):
        """
        BitBankのロウソク足
        :param pair:        string
        :param time:        string ex) 20180901
        :param candle_type: string
        :return:
        {
            "transactions": [
              {
                "transaction_id": 0,
                "side": "string",
                "price": "string",
                "amount": "string",
                "executed_at": 0
              }
            ]
          }
        """
        return self.__pub.get_candlestick(pair, candle_type, time)

    def new_order(self, pair, price, amount, side, order_type):
        """
        BitBankの新規注文
        :param pair:        string  ペア ex)btc_jpy
        :param price:       number  価格
        :param amount:      number  枚数
        :param side:        string  サイド ex)buy, sell
        :param order_type:  string  指値注文 or 成行注文
        :return: dict 注文内容
        {
            "order_id": integer,
            "pair": "string",
            "side": "string",
            "type": "string",
            "start_amount": "string",
            "remaining_amount": "string",
            "executed_amount": "string",
            "price": "string",
            "average_price": "string",
            "ordered_at": 0,
            "status": "string"
          }
        """
        if self.__pri is None:
            raise Exception('Private API is closed.')
        return self.__pri.order(
            pair=pair,
            price=str(price),
            amount=str(amount),
            side=side,
            order_type=order_type
        )

    def cancel_order(self, pair, order_id):
        """
        BitBankの注文取消
        :param pair:     string
        :param order_id: string
        :return: dict 取り消し注文内容
        {
            "order_id": 0,
            "pair": "string",
            "side": "string",
            "type": "string",
            "start_amount": "string",
            "remaining_amount": "string",
            "executed_amount": "string",
            "price": "string",
            "average_price": "string",
            "ordered_at": 0,
            "status": "string"
          }
        """
        if self.__pri is None:
            raise Exception('Private API is closed.')
        return self.__pri.cancel_order(
            pair=pair,
            order_id=order_id
        )

    def use_order(self, pair, order_id):
        """
        :param pair:
        :param order_id:
        :return:
        {
            "order_id": 0,
            "pair": "string",
            "side": "string",
            "type": "string",
            "start_amount": "string",
            "remaining_amount": "string",
            "executed_amount": "string",
            "price": "string",
            "average_price": "string",
            "ordered_at": 0,
            "status": "string"
          }
        """
        if self.__pri is None:
            raise Exception('Private API is closed')
        return self.__pri.get_order(
            pair=pair,
            order_id=order_id
        )

    def use_orders_info(self, pair, order_ids):
        """
        BitBankの注文情報
        :param pair:      string ペア
        :param order_ids: list   注文IDのリスト
        :return: dict 注文情報のリスト
        {
            "orders": [
              {
                "order_id": 0,
                "pair": "string",
                "side": "string",
                "type": "string",
                "start_amount": "string",
                "remaining_amount": "string",
                "executed_amount": "string",
                "price": "string",
                "average_price": "string",
                "ordered_at": 0,
                "status": "string"
              },
            ]
          }
        """
        if self.__pri is None:
            raise Exception('Private API is closed.')
        return self.__pri.get_orders_info(
            pair=pair,
            order_ids=order_ids
        )

    def use_asset(self):
        """
        BitBankのアセット
        :return: dict アセットの一覧
        {
            "assets": [
              {
                "asset": "string",
                "amount_precision": 0,
                "onhand_amount": "string",
                "locked_amount": "string",
                "free_amount": "string",
                "withdrawal_fee": "string"
              }
            ]
          }
        """
        if self.__pri is None:
            raise Exception('Private API is closed.')
        return self.__pri.get_asset()
