#!/usr/bin/python

import re
import os
from datetime import datetime, timedelta
import os.path as path
import argparse
import mysql.connector
import subprocess
from time import gmtime


def main():
        
    nowTime = datetime.utcnow() #date and time now
    gtsRegex = re.compile("^data(\d{2})(\d{2})$", re.IGNORECASE) #Define regex pattern to match file names
    find_minutes = 8
    print('----------------------\nProgram start at {}'.format(nowTime.strftime('%Y-%m-%d %H:%M:%S')))
    
    
    #Parse input options
    parser = argparse.ArgumentParser(description='Translate newest GTS file to SAPP friendly bufr format')
    parser.add_argument('-d','--datadir',help='Absolute path to input data directory', required=True)
    parser.add_argument('-o','--outdir',help='Absolute path to output directory', required=True)
    parser.add_argument('-r','--minutes',help='Look for data arriving within X minutes', type=int, required=True)
     
    parser.add_argument('-y','--dryrun',action='store_true', default=False, \
                        help='Provide flag if you do not want to actually make changes', required=False)
     
     
    args = parser.parse_args()
    datadir = args.datadir
    outdir = args.outdir
    dryrun = args.dryrun     
    find_minutes = args.minutes
        
    starttime = nowTime - timedelta(minutes=find_minutes)
    print ('Start time: {}'.format(starttime.strftime('%Y-%m-%d %H:%M:%S')))
    if starttime.second < 31: starttime = starttime.replace(second=0,microsecond=0)
    else: starttime = (starttime + timedelta(minutes=1)).replace(second=0,microsecond=0)
    print ('Start time: {}'.format(starttime.strftime('%Y-%m-%d %H:%M:%S')))
    delta_time = 5
    if starttime.minute % delta_time != 0:
        starttime += timedelta(minutes=delta_time) #Add delta_time min
        starttime -= timedelta(minutes=starttime.minute % delta_time) #Subtract modulo of delta_time min    
    print ('Start time: {}'.format(starttime.strftime('%Y-%m-%d %H:%M:%S')))
    inc_time = starttime
    while inc_time < nowTime.replace(second=0,microsecond=0) - timedelta(minutes=5):
        print ('Time file: {}'.format(inc_time.strftime('%Y-%m-%d %H:%M:%S')))
        file_data = path.join(datadir,'data{}'.format(inc_time.strftime('%H%M')))
        if path.isfile(file_data):
            file_mtime = datetime.fromtimestamp(path.getmtime(file_data))
            print('  Found file {}: mtime {}'.format(file_data,file_mtime.strftime('%Y-%m-%d %H:%M:%S')))
            if nowTime - file_mtime > timedelta(hours=2): 
                inc_time += timedelta(minutes=5)
                continue #If file is old, assume it is from yesterday or older
                    
            with open(file_data, "rb") as binaryfile :
                mybinarydata = binaryfile.read()
                 
            new1 = '\001\r\r\n'
            new2 = '\r\r\n\003'
            mybinarydata=mybinarydata.replace(b'ZCZC ',bytes(new1))
            mybinarydata=mybinarydata.replace(b'\n\n\n\n\n\n\nNNNN\r\r\n',bytes(new2))
                        
            output_file = path.join(outdir,'gts_data_{}.bufr'.format(inc_time.strftime('%Y%m%d%H%M%S')))
 
            if not dryrun:
                with open(output_file, "wb") as newFile:
                    newFile.write(mybinarydata)
                print('  Output: {}'.format(output_file))
                    
        inc_time += timedelta(minutes=5)
             

    
    
    
                
if __name__ == '__main__':
    main()
