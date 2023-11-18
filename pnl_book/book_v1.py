class pnl_book:
    def __init__(self, type) -> None:
        self.trades = []
        self.holding = 0    # 0 for none, 1 for long, -1 for buy
        self.price = 0
        self.no_of_trades = 0
        self.last_buy_price = 0
        self.net_pl = 0
        self.type = type

    def update_price(self, price):
        self.price = price

    def update_profit(self, order, order2 = None):
        order1 = order
        if(order2==None):
            result = {}
            if(order=="buy" and self.holding==0):
                self.last_buy_price = self.price
                self.holding = 1
                self.no_of_trades += 1
                # result["trig"] = self.trig
                result["order"]='buy'
                result["price"]= self.price
                result["current holding"]= self.holding
            elif((order=="sell" or order=="exit") and self.holding==1):
                self.net_pl += self.price - self.last_buy_price
                self.holding = 0
                self.no_of_trades += 1
                # result["trig"] = self.trig
                result["order"]= 'sell'
                result["price"]= self.price
                result["current holding"]= self.holding
                result["current profit"] = self.net_pl
            else:
                # result["trig"] = self.trig
                result["order"]= 'none'
                result["price"]= self.price
                result["current holding"]= self.holding
                return 0
            self.trades.append(result)

            return 1

        else:
            result = {}
            if((order1=="buy" and (order2=="sell" or order2=="exit")) and self.holding==0):
                self.last_buy_price = self.price
                self.holding = 1
                self.no_of_trades += 1
                # result["trig"] = self.trig
                result["order"]='buy'
                result["price"]= self.price
                result["current holding"]= self.holding
            elif((order1=="sell" or order1=="exit") and order2=="buy" and self.holding==1):
                self.net_pl += self.price - self.last_buy_price
                self.holding = 0
                self.no_of_trades += 1
                self.last_buy_price = self.price
                # result["trig"] = self.trig
                result["order"]= 'sell'
                result["price"]= self.price
                result["current holding"]= self.holding
                result["current profit"] = self.net_pl
            else:
                # result["trig"] = self.trig
                result["order"]= 'none'
                result["price"]= self.price
                result["current holding"]= self.holding
                return 0
            self.trades.append(result)

            return 1

    def get_current_status(self):
        return [self.net_pl, self.no_of_trades, self.holding, self.price - self.last_buy_price]
