#!/usr/bin/env python

"""
This script is used to extract api-tester-radio log from /var/log/syslog.

Usage::

    extractApiTesterRadioLog.py -h
    extractApiTesterRadioLog.py [-o <outfile>] [-s <starttime>] [-e <endtime>]

Options::

    -h or --help
        Display this help message.

    -o <file> or --output <file>
        output to the given file, If this option is not specified
        default test.log will be used

    -s <starttime> or --starttime <starttime>
        start time stamp h:m:s for extracting log, If this option is not specified
        default 00:00:00 will be used

    -e <endtime> or --endtime <endtime>
        end timestamp h:m:s for extracting log, If this option is not specified
        current time stamp will be used
"""

import os
import re
import sys
import getopt

from datetime import datetime



def withinTimeDelta(inputTime, startTimeDt, endTimeDt):
    inputTimeDt = datetime.strptime(inputTime, "%H:%M:%S")
    if (inputTimeDt >= startTimeDt) and (inputTimeDt < endTimeDt):
        return True
    return False

def parseFile(outputFileName, startTimeDt, endTimeDt):
    
    apiTesterRadioPattern = re.compile(r'.*api-tester-radio: (.*)')       

    logfilename ="/var/log/syslog"
    with open(outputFileName, 'w') as outputfile:
        with open(logfilename, 'r') as tracefile:
            for line in tracefile:           
                apiTesterRadioStringMatchResult = apiTesterRadioPattern.match(line)
                if apiTesterRadioStringMatchResult:
                    apiTesterRadioString = apiTesterRadioStringMatchResult.group(1)
                    timeStampPattern = re.compile(r'(\d+:\d+:\d+)\..*')                   
                    
                    timeStampMatchResult = timeStampPattern.match(apiTesterRadioString)
                    if timeStampMatchResult:
                        timeStamp = timeStampMatchResult.group(1)

                        if withinTimeDelta(timeStamp, startTimeDt, endTimeDt):
                            outputfile.write(apiTesterRadioString)
                            outputfile.write("\n")

def usage():
    print(__doc__)

if __name__ == "__main__":
    try:
        # Parse and interpret options.
        opts, args = getopt.getopt(sys.argv[1:], "ho:s:e:", ["help", "output=", "starttime=", "endtime=",])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    outputFileName = "test.log" #default output file name
    startTimeDt = datetime.strptime("00:00:00", "%H:%M:%S") #default start time stamp
    endTimeDt = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S") # default end time stamp

    for (opt, value) in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-o", "--output"):
            outputFileName = value
        elif opt in ("-s", "--starttime"):
            startTimeDt = datetime.strptime(value, "%H:%M:%S")
        elif opt in ("-e", "--endtime"):
            endTimeDt = datetime.strptime(value, "%H:%M:%S")
        else:
            assert False, "unhandled option"
    
    parseFile(outputFileName, startTimeDt, endTimeDt)
