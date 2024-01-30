import importlib
readport = importlib.import_module("2_1")
from collections import Counter
from collections import defaultdict
from pprint import pprint

rows = readport.read_rides("../Data/ctabus.csv",readport.read_line_as_dict)

# how many bus routes exist in Chicago?
routes_count = len(set([row['route'] for row in rows]))
print(routes_count)

# How many people rode the number 22 bus on February 2, 2011?  What about any route on any date of your choosing?
date = '02/02/2011'
route_num = '22'
date_rides = Counter()
for row in rows:
        if row['date'] == date:
            date_rides[row['route']] += row['rides']
print(f"ride on {date}, on {route_num}, total rides:",date_rides['22'])


# What is the total number of rides taken on each bus route?
route_rides = Counter()
for row in rows:
    route_rides[row['route']] += row['rides']
for route, count in route_rides.most_common():
    print('%5s %10d' % (route, count))
print('________________________________________')
    

# What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?
year_rides = defaultdict(Counter)
for row in rows:
    year_rides[row['date'][6:]][row['route']] += row['rides']
ten_year_increase = Counter()
ten_year_increase = year_rides['2011'] - year_rides['2001']
print("most changed routes:")
for route, count in ten_year_increase.most_common(5):
    print('%5s %10d' % (route, count))
