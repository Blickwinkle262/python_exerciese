# reader.py

import csv
from stock import Stock
from typing import Iterable,List,Dict,Any,Type,Optional

def read_csv_as_dicts(filename:str,types:List[Type]):
    with open(filename) as file:
        return csv_as_dicts(file,types)

def read_csv_as_instance(filename:str,cls:Stock):
    with open(filename) as file:
        return csv_as_instances(file,cls)


def csv_as_dicts(lines: Iterable, types: List[Type], *, headers: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    records = []
    rows = csv.reader(lines)

    if headers is None:
        headers = next(rows)

    for row in rows:
        record = {
            name: func(val) for name, func, val in zip(headers, types, row)
        }
        records.append(record)
    return records


def csv_as_instances(lines: Iterable, cls: Stock, *, headers: Optional[List[str]] = None) -> List[Stock]:
    records = []
    rows = csv.reader(lines)

    if headers is None:
        headers = next(rows)

    for row in rows:
        record = cls.from_row(row)
        records.append(record)
    return records