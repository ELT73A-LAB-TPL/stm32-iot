
```bash
docker ps
docker exec -it influxdb2 bash

influx org ls
influx org create --name Node-RED --description Node-RED
influx user create --org Node-RED --name Node-RED --password noderedpass
for group in A B C D E F; do
  influx bucket create --name bucket-${group} --org Node-RED
done

influx auth create --org Node-RED --user Node-RED --all-access

```
