import csv
from abc import ABC, abstractmethod

class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass
    

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def read_csv_as_dicts(filename, types):
    parser = DictCSVParser(types)
    return parser.parse(filename)

def read_csv_as_instances(filename, cls):
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)

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
    
    def __repr__(self) -> str:
        return f'Stock({self.name!r},{self.shares},{self.price})'
        
print(read_csv_as_instances('../Data/portfolio.csv', Stock))