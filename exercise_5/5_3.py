import csv
from typing import Iterable,List,Dict,Any,Type,Optional


def convert_csv(lines:Iterable,func:callable,*,headers:Optional[List[str]]=None)->List:
    rows = csv.reader(lines)

    if headers is None:
        headers = next(rows)

    records = map(lambda row: func(headers,row), rows)
    return records



def make_dict(headers:List[str], rows:List[str]) -> Dict[str,str]:
    return dict(zip(headers,rows))

def csv_as_dicts(lines:Iterable,types:List[Type],*,headers:Optional[List[str]]=None)->List[Dict[str,Any]]:
    convert_func = lambda headers,row: {name: func(val) for name, func, val in zip(headers, types, row)}
    return convert_csv(lines,convert_func,headers=headers)

def csv_as_instances(lines:Iterable,cls:Type,*,headers:Optional[List[str]]=None)->List:
    convert_func = lambda headers,row: cls.from_row(row)
    return convert_csv(lines,convert_func,headers=headers)
