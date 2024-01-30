import csv

def read_line_as_tuple(row):
    route = row[0]
    date = row[1]
    daytype = row[2]
    rides = int(row[3])
    record = (route, date, daytype, rides)
    return record

class RowRecord:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

    def __str__(self):
        return f'{self.route}, {self.date}, {self.daytype}, {self.rides}'

def read_line_as_dict(row):
    record = {
        'route': row[0],
        'date': row[1],
        'daytype': row[2],
        'rides': int(row[3])
    }
    return record

from collections import namedtuple
RideRow = namedtuple('RideRow', ['route', 'date', 'daytype', 'rides'])
import tracemalloc
import csv
import time

class RowRecordSlots:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides
    def __str__(self):
        return f'{self.route}, {self.date}, {self.daytype}, {self.rides}'

def read_line_as_class(row):
    record = RowRecord(row[0], row[1], row[2], int(row[3]))
    return record

def read_line_as_slot_class(row):
    record = RowRecordSlots(row[0], row[1], row[2], int(row[3]))
    return record

def read_line_as_namedtuple(row):
    record = RideRow(row[0], row[1], row[2], int(row[3]))
    return record

def memory_usage_decorator(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        print(f'Memory Use: Current {current_memory}, Peak {peak_memory}')
        print(f'Execution Time: {end_time - start_time} seconds')
        return result
    return wrapper



@memory_usage_decorator
def read_rides(file_name, method):
    records = []
    with open(file_name, "r") as file:
        rows = csv.reader(file)
        headers = next(rows)
        for row in rows:
            record = method(row)
            records.append(record)
    return records

if __name__ == '__main__':
    tracemalloc.start()
    tuple_rows = read_rides('../Data/ctabus.csv', read_line_as_tuple)
    print("-----------------------------------------------------")
    
    dict_rows = read_rides('../Data/ctabus.csv', read_line_as_dict)
    print("-----------------------------------------------------")  
    
    class_rows = read_rides('../Data/ctabus.csv', read_line_as_class)
    print("-----------------------------------------------------")
    
    slot_class_rows = read_rides('../Data/ctabus.csv', read_line_as_slot_class)
    print("-----------------------------------------------------") 
    
    namedtuple_rows = read_rides('../Data/ctabus.csv', read_line_as_namedtuple)
    print("-----------------------------------------------------")