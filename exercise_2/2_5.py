import csv
from collections.abc import Sequence


class RideData(Sequence):
    def __init__(self):
        self.routes = []
        self.dates = []
        self.daytype = []
        self.num_rides = []
    
    def __len__(self):
        return len(self.routes)
    
    def __getitem__(self, i):
        if isinstance(i, slice):
            new_record = RideData()
            for index in range(*i.indices(len(self))):
                new_record.append(self.routes[index], self.dates[index], self.daytype[index], self.num_rides[index])
            return new_record
        else:
            return {'routes':self.routes[i],'dates': self.dates[i], 'daytype':self.daytype[i], 'rides':self.num_rides[i]}
    
    def append(self, route, date, daytype, rides):
        self.routes.append(route)
        self.dates.append(date)
        self.daytype.append(daytype)
        self.num_rides.append(rides)

def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = RideData()      # <--- CHANGE THIS
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            # record = {
            #     'route': route, 
            #     'date': date, 
            #     'daytype': daytype, 
            #     'rides' : rides
            #     }
            records.append(route, date, daytype, rides)
    return records