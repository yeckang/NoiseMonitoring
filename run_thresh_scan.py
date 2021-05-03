import subprocess
import time
import ROOT as r

def run_threshold_scan(args, dirName) :
    script = 'scan_script/sbit_threshold.py'
    arg = '%d -minThr %d -maxThr %d -step %d'%(args.nOH, args.minTHR_ARM_DAC, args.maxTHR_ARM_DAC, args.stepTHR_ARM_DAC)
    
    cmd = 'bash -c -l "python -u - %s"'%arg
    
    host = 'gempro@gem-shelf01-amc02'
    log = file('%s/sbit_threshold_scan.log'%(dirName), 'w')
    err = file('%s/sbit_threshold_scan.err'%(dirName), 'w')
    infile = file(script, 'r')
    subprocess.call(['ssh', host, cmd], stdin=infile, stdout=log, stderr=err)
    
    log.close()
    err.close()
    infile.close()

def process_threshold_scan(dirName, minThr, maxThr, step, timeWindow) :
    log = file('%s/sbit_threshold_scan.log'%dirName, 'r')
    histInfo = {}
    for l in log :
        source = l.rstrip().split(';')
        if source[0] == 'threshold' :
            t = float(source[1])
            histInfo[t] = [0 for i in range(24)]
        elif source[0] == 'vfatN' :
            vfatN = int(source[1])
            rate = float(source[2])
            histInfo[t][vfatN] = rate

    nBins = (maxThr - minThr)/2
    
    h = [ r.TH1D('sbit_threshold_vfat_%d'%i, 'vfat %d;THR_ARM_DAC;Rate [Hz]'%i, nBins, minThr, maxThr) for i in range(24) ]
    sortedKey = sorted(histInfo.keys())
    for i, t in enumerate(sortedKey) :
        rates = histInfo[t]
        xBin = h[0].GetXaxis().FindBin(i)
        for i in range(24) :
            h[i].SetBinContent(xBin, rates[i])
            h[i].SetBinError(xBin, 1./timeWindow)
    
    fOut = r.TFile('%s/sbit_threshold_scan.root'%dirName, 'recreate')
    for i in range(24) :
        h[i].Write()
    fOut.Close()

def make_threshold_file(dirName, rate) :
    fIn = r.TFile('%s/sbit_threshold_scan.root'%dirName, 'read')
    threshold = []
    for i in range(24) :
        h = fIn.Get('sbit_thrdshold_vfat_%d'%i)
        nBins = h.GetXaxis().GetNBins()
        for ix in range(1, nBins+1) :
            if h.GetBinContent(ix) < rate :
                threshold.append(int(h.GetXaxis().GetLowEdge(ix)))
                break

    fOut = open('%s/threshold.txt'%dirName, 'w')
    for value in threshold :
        print >>fOut,value
    fOut.close()

if __name__ == '__main__' :
    import argparse
    current = time.localtime()
    dirName = 'data/thresh_scan/%d.%02d.%02d.%02d.%02d'%(current.tm_year, current.tm_mon, current.tm_mday, current.tm_hour, current.tm_min)
    subprocess.call(['mkdir', '-p', dirName])

    parser = argparse.ArgumentParser(description='SBit Rate Scans as Function of THR_ARM_DAC value')
    parser.add_argument('nOH', help='number of OH to scan')
    parser.add_argument('--timeWindow', '-time', type=int, help='Time window for SBit counting')
    parser.add_argument('--minTHR_ARM_DAC', '-minThr', type=int, default = 0, help='Minimum value of THR_ARM_DAC')
    parser.add_argument('--maxTHR_ARM_DAC', '-maxThr', type=int, default = 255, help='Maximum value of THR_ARM_DAC')
    parser.add_argument('--stepTHR_ARM_DAC', '-step', type=int, default = 1, help='Step size of THR_ARM_DAC')
    parser.add_argument('--rate_value', '-rate', type=float, default = 10, help='rate to set as threshold')
    args = parser.parse_args()

    run_threshold_scan(args, dirName)
    process_threshold_scan(dirName, args.minTHR_ARM_DAC, args.maxTHR_ARM_DAC, args.stepTHR_ARM_DAC, args.timeWindow)
    make_threshold_file(dirName, args.rate_value)
    exit()
