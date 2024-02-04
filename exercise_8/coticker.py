from structure import Structure
from validate import Integer, Float, String

class Ticker(Structure):
    name = String()
    price =Float()
    date = String()
    time = String()
    change = Float()
    open = Float()
    high = Float()
    low = Float()
    volume = Integer()

from cofollow import consumer, follow,recieve
from tableformat import create_formatter
import csv

# This one is tricky. See solution for notes about it
@consumer
def to_csv(target):
    def producer():
        while True:
            yield line

    reader = csv.reader(producer())
    while True:
        line = yield from recieve(str)
        target.send(next(reader))

@consumer
def create_ticker(target):
    while True:
        row = yield from recieve(list)
        target.send(Ticker.from_row(row))

@consumer
def negchange(target):
    while True:
        record = yield from recieve(Ticker)
        if record.change < 0:
            target.send(record)

@consumer
def ticker(fmt, fields):
    formatter = create_formatter(fmt)
    formatter.headings(fields)
    while True:
        rec = yield from recieve(Ticker)
        row = [getattr(rec, name) for name in fields]
        formatter.row(row)
        
if __name__ == '__main__':
    follow('../Data/stocklog.csv', to_csv(create_ticker(negchange(ticker('text', ['name', 'price', 'change'])))))