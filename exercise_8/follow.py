class FRange:
    def __init__(self,start,end,step):
        self.start = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        n = self.start
        while n < self.end:
            yield n
            n += self.step

import os
import time

# while True:
#     line = f.readline()
#     if line == '':
#         time.sleep(0.1)
#         continue
#     fields = line.split(',')
#     name = fields[0].strip('"')
#     price = float(fields[1])
#     change = float(fields[4])
    
#     if change < 0:
#         print('%10s %10.2f %10.2f' % (name,price,change))

def follow(filepath):
    try:
        with open(filepath,'r') as f:
            f.seek(0,os.SEEK_END)
            while True:
                line = f.readline()
                if line == '':
                    time.sleep(0.1)
                    continue
                yield line
    except GeneratorExit:
        print('Goodbye')

