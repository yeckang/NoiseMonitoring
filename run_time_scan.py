import subprocess
import time
import ROOT as r

def read_threshold_file(dirName) :
    f = open('data/%s/threshold.txt'%dirName, 'r')
    threshold = []
    for l in f :
        threshold.append(float(l))
    return threshold

def run_time_scan(args, dirName, threshold) :
    script = 'scan_script/sbit_time_scan.py'
    arg = '%d -time %d -interval %d -total %d'%(args.nOH, args.timeWindow, args.interval, args.totalTime)

    arg += ' -thr'
    for thr in thresholds : arg += ' %d'%thr
    
    cmd = 'bash -c -l "python -u - %s"'%arg
    
    host = 'lxplus'
    log = file('%s/sbit_time_scan.log'%(dirName), 'w')
    err = file('%s/sbit_time_scan.err'%(dirName), 'w')
    infile = file(script, 'r')
    subprocess.call(['ssh', host, cmd], stdin=infile, stdout=log, stderr=err)
    
    log.close()
    err.close()
    infile.close()

def process_scan(dirName) :
    log = file('%s/sbit_time_scan.log'%dirName, 'r')
    histInfo = {}
    for l in log :
        source = l.replace(' ', '').rstrip().split(';')
        if source[0] == 'time' :
            t = float(source[1])
            histInfo[t] = [0 for i in range(24)]
        elif source[0] == 'vfatN' :
            vfatN = int(source[1])
            rate = float(source[2])
            histInfo[t][vfatN] = rate
    
    h = [ r.TH1D('sbit_time_vfat_%d'%i, 'vfat %d;Time;Rate [Hz]'%i, len(histInfo.keys()), 0, len(histInfo.keys())) for i in range(24) ]
    sortedKey = sorted(histInfo.keys())
    for i, t in enumerate(sortedKey) :
        rates = histInfo[t]
        loctime = time.localtime(t)
        label = '%02d:%02d:%02d'%(loctime.tm_hour, loctime.tm_min, loctime.tm_sec)
        xBin = h[0].GetXaxis().FindBin(i)
        for i in range(24) :
            h[i].GetXaxis().SetBinLabel(xBin, label)
            h[i].SetBinContent(xBin, rates[i])
    
    fOut = r.TFile('%s/sbit_time_scan.root'%dirName, 'recreate')
    for i in range(24) :
        h[i].Write()
    fOut.Close()

if __name__ == '__main__' :
    import argparse
    current = time.localtime()
    dirName = 'data/%d.%02d.%02d.%02d.%02d'%(current.tm_year, current.tm_mon, current.tm_mday, current.tm_hour, current.tm_min)
    subprocess.call(['mkdir', '-p', dirName])
    
    parser = argparse.ArgumentParser(description='SBit Rate Scans as Function of THR_ARM_DAC value')
    parser.add_argument('nOH', type=int, default = 0, help='number of OH to scan')
    parser.add_argument('--timeWindow', '-time', type=int, help='Time window for SBit counting(seconds)')
    parser.add_argument('--interval', '-interval', type=int, default = 10, help='Time interval for next data taking (second)')
    parser.add_argument('--totalTime', '-total', type=int, default = 60, help='Total data taking time (miniute)')
    parser.add_argument('--thresholds', '-thr', default = None, help='Date for threshold setup')
    args = parser.parse_args()

    read_threshold_file(dirName)
    run_time_scan(args, dirName)
    process_scan(dirName)
    exit()
