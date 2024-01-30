from typing import Iterable
import time
import threading
from concurrent.futures import Future

def parse_line(line:str)-> Iterable:
    if line.find('=') == -1:
        return None
    else:
        return tuple(line.split('='))

def work(x,y):
    print("about to work")
    time.sleep(3)
    print("Done")
    return x+y

def do_work(x,y,fut):
    fut.set_result(work(x,y))

t = threading.Thread(target=work,args=(1,2))
t.start()

fut = Future()
f = threading.Thread(target=do_work,args=(2,3,fut))
f.start()
