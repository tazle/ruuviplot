#! /bin/sh
set -e
LENGTH=${1:-24h}

python3 data_for_plot.py $LENGTH temperature humidity pressure
echo "Download complete"

plotconf=$(mktemp)
cat plot-template.json > "$plotconf"
sed -i -es/__LENGTH__/$LENGTH/ "$plotconf"

python3 plot_data.py "$plotconf"

