import sys
import inspect


class Structure:
    _fields = ()

    @staticmethod
    def _init():
        locs = sys._getframe(1).f_locals
        self = locs.pop("self")
        for name, val in locs.items():
            setattr(self, name, val)

    # def __init__(self, *args):
    #     if len(args) != len(self._fields):
    #         raise TypeError(f"Expected {len(self._fields)} arguments")
    #     for key, values in zip(self._fields, args):
    #         setattr(self, key, values)
    @classmethod
    def set_fields(cls):
        sig = inspect.signature(cls)
        cls._fields = tuple(sig.parameters)

    @classmethod
    def set_init(cls):
        argstr = ",".join(cls._fields)
        code = f"def __init__(self, {argstr}):\n"
        for name in cls._fields:
            code += f"    self.{name} = {name}\n"
        locs = {}
        exec(code, locs)
        cls.__init__ = locs["__init__"]

    def __setattr__(self, key, value):
        if key not in self._fields and not key.startswith("_"):
            raise TypeError(f"no attribute {key}")
        super().__setattr__(key, value)

    def __repr__(self):
        values = ",".join(f"{getattr(self, key)!r}" for key in self._fields)
        return f"{type(self).__name__}({values})"


class Stock(Structure):
    _fields = ("name", "shares", "price")

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


Stock.set_init()
