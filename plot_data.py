import sys

if len(sys.argv) < 2:
    print("Usage: plot_data.py <conf-file>", file=sys.stderr)
    sys.exit(1)

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time
import iso8601
import matplotlib.patches as mpatches
import json

conf = json.load(open(sys.argv[1]))
for plot in conf['plots']:
    data = pd.read_csv(plot['datafile'])
    data['time'] = data['time'].map(iso8601.parse_date)
    data = data.set_index('time')

    plt.figure()

    legend_patches = []

    for coloridx, location in enumerate(data.location.unique()):
        color = "C" + str(coloridx)
        for column in data.columns.values:
            if column not in ('time', 'location'):
                rows = data[data['location'] == location]
                style = '-'
                legend_patch = mpatches.Patch(color = color, label = location)
                if 'min' in column or 'max' in column:
                    style = ':'
                    legend_patch = None

                line = rows[column].plot.line(color = color, linestyle = style, label = location)
                if legend_patch:
                    legend_patches.append(legend_patch)
    plt.xlabel('Time')
    plt.ylabel(plot['ylabel'])
    plt.title(plot['title'])
    plt.legend(handles=legend_patches)
    plt.savefig(plot['plotfile'])

