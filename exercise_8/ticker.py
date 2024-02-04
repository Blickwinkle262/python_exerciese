# ticker.py

from structure import Structure
from validate import Integer, Float, String

class Ticker(Structure):
    name = String()
    price = Float()
    date = String()
    time = String()
    change = Float()
    open = Float()
    high = Float()
    low = Float()
    volume = Integer()

class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares





if __name__ == '__main__':
    from follow import follow
    import csv
    from tableformat import create_formatter,print_table
    lines = follow('../Data/stocklog.csv')
    # s = Stock.from_row(["GOOG",100,490.1])
    # print(s)
    formatter = create_formatter('text')
    rows = csv.reader(lines)
    records = (Ticker.from_row(row) for row in rows)
    negative = (record for record in records if record.change < 0)
    print_table(negative,['name','price','change'],formatter)
    # records = (Ticker.from_row(row) for row in rows)
    # for record in records:
    #     print(record)