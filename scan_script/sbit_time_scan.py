import sys, time
sys.path.append("lib/gem/")

import gempy
gempy.initialize()

def run_scan(ohN, seconds, interval, totalTime, thresholds) :
    timeWindow= 40079000 * seconds # conversion in BX units                                                                                                                                              
    waitTime = interval # minuite to second
    nData = totalTime / interval
    
    gempy.writeReg("GEM_AMC.OH.OH{}.FPGA.TRIG.CNT.SBIT_CNT_TIME_MAX".format(ohN), timeWindow)

    for vfatN in range(24):
        gempy.writeReg("GEM_AMC.OH.OH{}.GEB.VFAT{}.CFG_THR_ARM_DAC".format(ohN, vfatN), int(thresholds[vfatN]))

    for i in range(nData) :
        start = time.time()
        print "time;", time.time()

        time.sleep(seconds+1)

        for vfatN in range(24):
            print "vfatN;", vfatN, ";", (gempy.readReg("GEM_AMC.OH.OH{}.FPGA.TRIG.CNT.VFAT{}_SBITS".format(ohN, vfatN))/seconds*1.0)

        end = time.time()
        time.sleep(waitTime - (end - start))

if __name__ == '__main__' :
    import argparse
    parser = argparse.ArgumentParser(description='SBit Rate Scans as Function of THR_ARM_DAC value')
    parser.add_argument('nOH', help='number of OH to scan')
    parser.add_argument('--timeWindow', '-time', type=int, help='Time window for SBit counting(seconds)')
    parser.add_argument('--interval', '-interval', type=int, default = 10, help='Time interval for next data taking (second)')
    parser.add_argument('--totalTime', '-total', type=int, default = 60, help='Total data taking time (miniute)')
    parser.add_argument('--thresholds', '-thr', type=int, nargs='+', help='threshold for each vfat as list format')
    args = parser.parse_args()
    run_scan(args.nOH, args.timeWindow, args.interval, args.totalTime, args.thresholds)
    exit()
