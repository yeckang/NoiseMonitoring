# Noise monitoring script for the integration set up in B904

## Set the threshold value
```
python run_threshold_scan.py 0 -minThr 0 -maxThr 255 -step 1 -rate 10
```

## Run the monitoring script
```
python run_time_scan.py 0 -time 1 -interval 10 -total 30 -thr <Date that you set threshold value>
```
