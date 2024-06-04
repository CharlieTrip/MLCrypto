class SmallPRG(object):

    def __init__(self, seed):
        self.random_seed = [0xf1ea5eed, int(seed), int(seed), int(seed)]
        for _ in range(20):
            self.value()

    def rot(self, x, k):
        return ((x << k) & 0xffffffff) | (x >> (32 - k))

    def value(self):
        extra = self.random_seed[0] - self.rot(self.random_seed[1], 27)
        self.random_seed[0] = self.random_seed[1] ^ self.rot(self.random_seed[2], 17)
        self.random_seed[1] = (self.random_seed[2] + self.random_seed[3]) & 0xffffffff
        self.random_seed[2] = (self.random_seed[3] + extra) & 0xffffffff
        self.random_seed[3] = (extra + self.random_seed[0]) & 0xffffffff
        return self.random_seed[3]

    def rand1d(self):
        return abs(self.value()) % 6

    def rand2d(self):
        seed = abs(self.value())
        result = (seed % 6, (seed / 6) % 6)
        return result

    def flux(self):
        seed = abs(self.value())
        return (seed % 6) - ((seed / 6) % 6)