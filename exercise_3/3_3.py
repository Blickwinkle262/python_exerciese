class Stock:
    type = (str, int,float)
    def __init__(self, name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price
    
    @classmethod
    def from_row(cls,row):
        values = [func(val) for func, val in zip(cls.type, row)]
        return cls(*values)
        
import csv      

def read_csv_as_instances(filename,cls):
    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records

