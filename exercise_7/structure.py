import sys
import inspect
from validate import Validator
from collections import ChainMap

class StructureMeta(type):
    @classmethod
    def __prepare__(meta, clsname, bases):
        return ChainMap({}, Validator.validators)
        
    @staticmethod
    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)

class Structure(metaclass=StructureMeta):
    _fields = ()
    _types = ()

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
    def __init__subclass__(cls):
        validate_attributes(cls)

    @classmethod
    def set_init(cls):
        argstr = ",".join(cls._fields)
        code = f"def __init__(self, {argstr}):\n"
        for name in cls._fields:
            code += f"    self.{name} = {name}\n"
        locs = {}
        exec(code, locs)
        cls.__init__ = locs["__init__"]
    
    @classmethod
    def from_row(cls,row):
        row_data = [func(val) for func,val in zip(cls._types,row)]
        return cls(*row_data)
    
    def __setattr__(self, key, value):
        if key not in self._fields and not key.startswith("_"):
            raise TypeError(f"no attribute {key}")
        super().__setattr__(key, value)

    def __repr__(self):
        values = ",".join(f"{getattr(self, key)!r}" for key in self._fields)
        return f"{type(self).__name__}({values})"
    

from validate import Validator

def validate_attributes(cls):
    validators = []
    for name, val in vars(cls).items():
        if isinstance(val, Validator):
            validators.append(val)
    cls._fields = tuple([val.name for val in validators])
    cls._types = tuple( getattr(val, 'expected_type',lambda x: x) for val in validators)
    if cls._fields:
        cls.set_init()
    return cls

def typed_structures(clsname,**validators):
    cls = type(clsname,(Structure,),validators)
    return cls


# class Stock(Structure):
#     _fields = ("name", "shares", "price")

#     @property
#     def cost(self):
#         return self.shares * self.price

#     def sell(self, nshares):
#         self.shares -= nshares


# Stock.set_init()
