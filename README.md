# Noise monitoring script for the integration set up in B904

## Set the threshold value
```
python run_threshold_scan.py 0 -minThr 0 -maxThr 255 -step 1 -rate 10
```
This script make a sbit rate scan as a function of THR\_ARM\_DAC value.
And it also find the specific THR\_ARM\_DAC value that sbit rate is around 10Hz based on the result

## Run the monitoring script
```
python run_time_scan.py 0 -time 1 -interval 10 -total 30 -thr <Date that you set threshold value>
```
