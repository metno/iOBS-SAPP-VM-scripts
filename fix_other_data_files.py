#!/usr/bin/python

import re
import os
from datetime import datetime
import os.path as path
import argparse

from shutil import move,Error
from glob import glob

def main():
        
    nowTime = datetime.utcnow() #date and time now
    
    print('----------------------\nProgram start at {}'.format(nowTime.strftime('%Y-%m-%d %H:%M:%S')))
    
    
    #Parse input options
    parser = argparse.ArgumentParser(description='Change file names of bufr data files to include 14 datetime digits, then move to SAPP input dir')
    parser.add_argument('-d','--datadir',help='Absolute path to input data directory', required=True)
    parser.add_argument('-o','--outdir',help='Absolute path to output directory', required=True)
     
    parser.add_argument('-y','--dryrun',action='store_true', default=False, \
                        help='Provide flag if you do not want to actually make changes', required=False)
     
     
    args = parser.parse_args()
    datadir = args.datadir
    outdir = args.outdir
    dryrun = args.dryrun     

    test1Regex = re.compile("(.+?_)(\d{8})_(\d{4})(_.+)", re.IGNORECASE) #Define regex pattern to match file names        
    test2Regex = re.compile("(.+?_)(\d{8})_(\d{6})(_.+)", re.IGNORECASE) #Define regex pattern to match file names        
    
    inputfiles = glob(path.join(datadir,'*'))
    
    for file_ in inputfiles:
#         print('File: {}'.format(file_))
        if not re.search('_\d{14}_', os.path.basename(file_)): 
#             print('  Not 14 digits!!!!!!!')
            m = test1Regex.search(os.path.basename(file_)) #Match file name to get information
            if m: newname = '{}{}{}00{}'.format(m.group(1),m.group(2),m.group(3),m.group(4))
            else: 
                m = test2Regex.search(os.path.basename(file_)) #Match file name to get information
                if m: newname = '{}{}{}{}'.format(m.group(1),m.group(2),m.group(3),m.group(4))
                else:
                    print('  File {} without 14 digits also does not match!!!'.format(file_))
                    continue
        else: newname = os.path.basename(file_)
            
        newfile = path.join(outdir,newname)
        
        print('Moving file {} to {}'.format(file_,newfile))
        if dryrun: continue
        
        try:
#             print('  Move file!')
            move(file_, newfile)
        except Error: print('Error in moving file {} to {}!!!'.format(file_,newfile))
        
        
    
    
                
if __name__ == '__main__':
    main()
