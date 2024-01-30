def counter(value):
    def inc():
        nonlocal value
        value += 1
        return value
    def dec():
        nonlocal value
        value -= 1
        return value
    return inc,dec

from typedproperty import typedproperty,String,Integer,Float

class Stock():
    name = String('name')
    shares = Integer('shares')
    price =  Float('price')
    
    def __init__ (self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price  
        