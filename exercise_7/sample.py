from logcall import logged,logformat
from validate import Integer, PositiveInteger,validated, enforce


# @validated
# def add(x:Integer,y:Integer) -> Integer:
#     return x+y

@validated
def pow(x:Integer,y:Integer) -> Integer:
    return x**y  

@logged
def test_add(x,y):
    'add x and y together'
    return x + y

@logformat('{func.__code__.co_filename}:{func.__name__}')
def mul(x,y):
    return x * y

@enforce(x=Integer,y=Integer)
def add(x,y):
    return x+y


class Stock:
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price
    
    @property
    def cost(self):
        return self.shares * self.price
    
    @validated
    def sell(self,nshares:PositiveInteger):
        self.shares -= nshares