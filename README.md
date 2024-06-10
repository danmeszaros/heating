running systemm filesystem structure

```
/bin/        # binaries
/dev/        # live values from sensors/relays etc
/cache/      # persistent data from apps 
/conf/       # configs
/cron/       # cron should link here
```

apps:

* relay_sync.py      # synchronize hw relays to desired value from dev
* dev_reporter.py    # report values from /dev/ to remote grafana
* sensor_reader.py   # reads value from hw sensors and updates /dev/ values
* controller.py      # read sensor values and decides relay states
