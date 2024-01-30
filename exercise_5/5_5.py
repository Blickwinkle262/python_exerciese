import csv
from typing import Iterable,List,Dict,Any,Type,Optional
import logging

log = logging.getLogger(__name__)

def convert_csv(lines: Iterable, func: callable, *, headers: Optional[List[str]] = None) -> List:
    rows = csv.reader(lines)
    records = []

    if headers is None:
        headers = next(rows)

    for idx, row in enumerate(rows):
        try:
            current = func(headers, row)
            records.append(current)
        except Exception as e:
            log.warning(f'Row {idx+1} bad row: {row}')
            log.debug(f'Exception: {e}')
            continue
    return records

def make_dict(headers:List[str], rows:List[str]) -> Dict[str,str]:
    return dict(zip(headers,rows))

def csv_as_dicts(lines:Iterable,types:List[Type],*,headers:Optional[List[str]]=None)->List[Dict[str,Any]]:
    convert_func = lambda headers,row: {name: func(val) for name, func, val in zip(headers, types, row)}
    return convert_csv(lines,convert_func,headers=headers)