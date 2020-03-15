from collections import namedtuple


_Interval = namedtuple("_Interval", ["lo", "hi"])


class Interval(_Interval):
    @property
    def width(self):
        return self.hi - self.lo

    def __repr__(self):
        return f"[{self.lo}, {self.hi}]"
