class Uniform:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def F(self, x):
        return (x - self.low) / (self.high - self.low)

    def f(self):
        return 1 / (self.high - self.low)

    def r(self, x):
        return x - (1 - self.F(x)) / self.f()

    def r_inv(self, x):
        return (x + self.high) / 2
