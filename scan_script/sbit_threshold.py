import sys, time
sys.path.append("lib/gem/")

import gempy
gempy.initialize()

def run_scan(ohN, seconds, minThr, maxThr, step) :
    timeWindow= 40079000 * seconds # conversion in BX units                                                                                                                                              
    gempy.writeReg("GEM_AMC.OH.OH{}.FPGA.TRIG.CNT.SBIT_CNT_TIME_MAX".format(ohN), timeWindow)
    
    print 'second;', seconds
    for threshold in range(minThr, maxThr+1, step) :
        for vfatN in range(24):
            gempy.writeReg("GEM_AMC.OH.OH{}.GEB.VFAT{}.CFG_THR_ARM_DAC".format(ohN, vfatN), threshold)
        
        time.sleep(seconds+1)
        
        print 'threshold;', threshold
        for vfatN in range(24):
            print  'vfat;', vfatN, ';', gempy.readReg("GEM_AMC.OH.OH{}.FPGA.TRIG.CNT.VFAT{}_SBITS".format(ohN, vfatN))/seconds*1.0

if __name__ == '__main__' :
    import argparse
    parser = argparse.ArgumentParser(description='SBit Rate Scans as Function of THR_ARM_DAC value')
    parser.add_argument('nOH', help='number of OH to scan')
    parser.add_argument('--timeWindow', '-time', type=int, help='Time window for SBit counting')
    parser.add_argument('--minTHR_ARM_DAC', '-minThr', type=int, default = 0, help='Minimum value of THR_ARM_DAC')
    parser.add_argument('--maxTHR_ARM_DAC', '-maxThr', type=int, default = 255, help='Maximum value of THR_ARM_DAC')
    parser.add_argument('--stepTHR_ARM_DAC', '-step', type=int, default = 1, help='Step size of THR_ARM_DAC')
    args = parser.parse_args()
    run_scan(args.nOH, args.timeWindow, args.minTHR_ARM_DAC, args.maxTHR_ARM_DAC, args.stepTHR_ARM_DAC)
