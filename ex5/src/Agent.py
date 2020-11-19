class Agent:
    def __init__(self, item_values):
        self.item_values = item_values
        self.value = 0

    def item_value(self, idx):
        return self.item_values[idx]

    def __str__(self):
        return "Items: {}, Value: {}".format(self.item_values,self.value)
