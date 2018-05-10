import time
import sys
from collections import defaultdict
import csv
import re

from influxdb import InfluxDBClient

if len(sys.argv) < 2:
    print("Usage: data_for_plot.py <period> <parameter>...", file=sys.stderr)
    sys.exit(1)

period = "24h"
window = "15m"

period = sys.argv[1]
if not re.match("^[0-9]+h$", period):
    print("Invalid period", period, file=sys.stderr)
    sys.exit(3)
window_min = max(1, int(int(period[:-1])*60 / 96))
window = str(window_min) + "m"    

client = InfluxDBClient(host="influx", port=8086, database="tag_data")

for parameter in sys.argv[2:]:
    if not re.match("^[a-z]+$", parameter):
        print("Invalid parameter", parameter, file=sys.stderr)
        sys.exit(2)

for parameter in sys.argv[2:]:
    results = client.query('SELECT mean(%(param)s) as mean_t, min(%(param)s) as min_t, max(%(param)s) as max_t FROM ruuvitag WHERE time > now() - %(period)s GROUP BY "name", time(%(window)s)' %{"param":parameter, "period":period, "window":window}, database="tag_data")


    rows = []

    columns = [k for k in next(iter(results[next(iter(results.keys()))])).keys() if k != 'time']

    for key in results.keys():
        location = key[1]['name']
        for point in results[key]:
            t = point['time']
            row = [t, location]
            for col in columns:
                row.append(point[col])
            rows.append(row)

    header = ['time', 'location'] + columns

    output = csv.writer(open(parameter + ".csv", "w"))
    output.writerow(header)
    output.writerows(rows)
