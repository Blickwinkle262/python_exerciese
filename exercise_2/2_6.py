from typing import List
import csv
from collections.abc import Sequence
import time


class Datacollection(Sequence):
    def __init__(self, types: List[type], header: List[str]):
        self.records = [[] for _ in types]
        self.types = types
        self.header = header
        if len(types) != len(header):
            raise ValueError("column types and file header are not match")
    
    def __len__(self):
        return len(self.records[0])
    
    def __getitem__(self, i):
        if isinstance(i, slice):
            new_record = Datacollection(self.types,self.header)
            for index in range(*i.indices(len(self))):
                current_record = [record[index] for record in self.records]
                new_record.append(current_record)
            return new_record
        else:
            selected = [record[i] for record in self.records]
            return {name: func(val) for name, func, val in zip(self.header, self.types, selected)}
    
    
    def append(self, new_record: list):
        if len(new_record) != len(self.types):
            raise ValueError("column types and record are not match")
        for sublist, value in zip(self.records, new_record):
            sublist.append(value)
            
#(111320895, 111351201）
#(34687332,  127305914

def time_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return result
    return wrapper

@time_wrapper
def read_csv_as_columns(filename: str, types: List[type]) -> Datacollection:
    '''
    Read the bus ride data as a list of dicts
    '''

    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows) 
        records = Datacollection(types, headers)
        for row in rows:
            records.append(row)        
    return records

@time_wrapper
def read_csv_as_dict(filename: str, types: List[type]) -> List[dict]:
    '''
    Read the bus ride data as a list of dicts
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)     # Skip headers
        for row in rows:
            record = {name: func(val) for name, func, val in zip(headers, types, row)}
            records.append(record)
    return records