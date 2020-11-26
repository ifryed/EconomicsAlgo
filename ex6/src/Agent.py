class Agent:
    def __init__(self, item_values):
        self.values = item_values
        self.org_pay = -999
        self.pay = -999

    def value(self, option: int):
        return self.values[option]
