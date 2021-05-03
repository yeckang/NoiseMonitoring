# Noise monitoring script for the integration set up in B904

## Set the threshold value
```
python run_threshold_scan.py 0 -minThr 0 -maxThr 255 -step 1 -rate 10
```
This script make a sbit rate scan as a function of THR\_ARM\_DAC value.

And it also find the specific THR\_ARM\_DAC value that sbit rate is around 10Hz based on the result

The result will be located in `data/thresh_scan/<Scan date>'.

## Run the monitoring script
```
python run_time_scan.py 0 -time 1 -interval 10 -total 30 -thr <Scan date of run_thrshold_scan>
```
This script make a sbit rate scan as a function of time.

Before run the script, you should run the threshold scan to feed the threshold to the script.
