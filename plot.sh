#! /bin/sh
set -e
LENGTH=${1:-24h}

python3 data_for_plot.py $LENGTH temperature humidity pressure
echo "Download complete"

plotconf=$(mktemp)
cat plot-template.json > "$plotconf"
sed -i -es/__LENGTH__/$LENGTH/ "$plotconf"

python3 plot_data.py "$plotconf"

files=$(jq -r .plots[].plotfile "$plotconf")
tar cf _out.tar $files
truncate -s 0 out.tar
cat _out.tar >> out.tar

