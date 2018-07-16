# Plot RuuviTag measurements

```
docker build . -t ruuviplot
touch out.tar
docker run --rm -it -v $PWD/out.tar:/out.tar --link influxdb.service:influx ruuviplot 48h
```
