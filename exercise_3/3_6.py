import csv

class Stock():
    __slots__ = ['name','_shares','_price']  # Fix: Change 'name', 'shares', 'price' to '_name', '_shares', '_price'
    _type =(str,int,float)
    def __init__ (self,name,shares,price):
        self.name = name  # Fix: Change 'name' to '_name'
        self.shares = shares  # Fix: Change 'shares' to '_shares'
        self.price = price  # Fix: Change 'price' to '_price'
    
    @property
    def shares(self):
        return self._shares
    
    @shares.setter
    def shares(self,value):
        if not isinstance(value,self._type[1]):
            raise TypeError('Expected int')
        self._shares = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self,value):
        if not isinstance(value,self._type[2]):
            raise TypeError('Expected float')
        elif value < 0:
            raise ValueError('Must be >= 0')
        else:
            self._price = value
    
    @property
    def cost(self):
        return self.shares * self.price
    
    def sell(self,amount):
        self.shares -= amount
    
    @classmethod
    def from_row(cls,row):
        values = [func(val) for func,val in zip(cls._type,row)]
        return cls(*values)
    
    def __eq__(self,other):
        if isinstance(other,Stock):
            return self.name == other.name and self.shares == other.shares and self.price == other.price
        else:
            return False
    
    def __repr__(self) -> str:
        return f'Stock({self.name!r},{self.shares},{self.price})'
    


def read_csv_as_instances(filename,cls):
    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records
    