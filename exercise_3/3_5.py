import importlib
stock = importlib.import_module("3_4")
from abc import ABC, abstractmethod


def print_table(portfolio, attribute_names,formatter):
    # 3_7 question a 
    if not isinstance(formatter, TableFormatter):
        raise TypeError('Expected a TableFormatter')
    formatter.headings(attribute_names)
    for stock in portfolio:
        rowdata = [getattr(stock, fieldname) for fieldname in attribute_names]
        formatter.row(rowdata)

class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()
    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))

    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))

class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join(headers))

    def row(self, rowdata):
        print(','.join( str(d) for d in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print('<tr> ' + ' '.join(f'<th>{header}</th>' for header in headers) + ' </tr>')

    def row(self, rowdata):
        print('<tr> ' + ' '.join(f'<td>{data}</td>' for data in rowdata) +' </tr>')

import sys
class redirect_stdout():
    def __init__(self, new_target):
        self.new_target = new_target

    def __enter__(self):
        self.old_target = sys.stdout
        sys.stdout = self.new_target
        return self.new_target

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.old_target
        

class ColumnFormatterMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeaderFormatterMixin:
    def headings(self, headers):
        headers = [header.upper() for header in headers]
        super().headings(headers)

# class TextColumnFormatter(UpperHeaderFormatterMixin,ColumnFormatterMixin,TextTableFormatter):
#     pass

# class HTMLColumnFormatter(ColumnFormatterMixin, HTMLTableFormatter):
#     pass

# class CSVColumnFormatter(ColumnFormatterMixin, CSVTableFormatter):
#     pass

def create_formatter(name, column_formats=None, upper_headers=False):
    if name == 'text':
        formatter_cls = TextTableFormatter
    elif name == 'csv':
        formatter_cls = CSVTableFormatter
    elif name == 'html':
        formatter_cls = HTMLTableFormatter
    else:
        raise RuntimeError('Unknown format %s' % name)

    if column_formats:
        class formatter_cls(ColumnFormatterMixin, formatter_cls):
              formats = column_formats

    if upper_headers:
        class formatter_cls(UpperHeaderFormatterMixin, formatter_cls):
            pass

    return formatter_cls()

    
portfolio = stock.read_csv_as_instances('../Data/portfolio.csv', stock.Stock)
formatter = create_formatter('csv',['%10s','%10d','%10.2f'],True)
with redirect_stdout(open('portfolio.csv','w')) as file:  
    print_table(portfolio, ['name','shares','price'], formatter)
    file.close()
