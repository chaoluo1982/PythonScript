import os
import re
from datetime import datetime

def withinTimeDelta(inputtime):
    inputtimedt = datetime.strptime(inputtime, "%Y-%m-%d %H:%M:%S")
    if (inputtimedt >= starttimedt) and (inputtimedt < endtimedt):
        return True
    return False


def parsefile(fullfilename):
    
    blockPattern = re.compile(r'(^\[.*)')   #indicate new block, if we have time stamp
    continuePrint = False

    # match this one: file = "bbiEqmhDumpHandler.cc"
    #searchPattern = re.compile(r'^\[.*file = \"bbiEqmhDumpHandler\.cc\".*')
    #fileAndLine = "iesa.c
    #searchPattern = re.compile(r'^\[.*fileAndLine = \"iesa.c.*')
    #find the content inside {}
    #searchPattern = re.compile(r'\{([^}]+) = ([^}]+)\}')
    #find the content =
    #searchPattern = re.compile(r'([^{}=,]+) = ([^{}=,]+)')
    #searchPattern = re.compile(r"^(\[[^]]+\]).*(msg = [^}]+)")
    # we have 2 pattern here!!
    searchPatternList = []

    #search pattern regex list                              
    regRuleTime = r"^(\[[^]]+\]).*"                    #group, match trace time, [^]] means match anything except ]
    regRuleKeyWord1 = r"(" + re.escape(keyword1) + r")"+ r".*"      #match this keywords
    regRuleMsg = r"(msg\s{1}=.*\n)"                    #group, match msg = ...., \s{1} means we must have 1 space here if we use VERBOSE, [^}] means match anything except }, space will be ignored so it must be stated and escaped.
    searchPattern1 = re.compile(regRuleTime + regRuleKeyWord1 + regRuleMsg)
    searchPatternList.append(searchPattern1)


    regRuleKeyWord2 = r"(" + re.escape(keyword2) + r".*\n)"               #group 1, match trace time, [^]] means match anything except ]
    searchPattern2 = re.compile(regRuleTime + regRuleKeyWord2 )
    searchPatternList.append(searchPattern2)


    
    (pathname, filename) = os.path.split(fullfilename)  # split to paht and filename
    newfilename = "new_" + filename                     # new file name 
    newfilename = os.path.join(pathname, newfilename)
    
    with open(newfilename, 'w') as outputfile:
        with open(fullfilename, 'r') as tracefile:
            for line in tracefile:              
                if blockPattern.match(line):
                    # find new block
                    continuePrint = False
                    # find the line with keywords, print the captured groups in the matching result
                    for searchPattern in searchPatternList:                                            
                        searchresult = searchPattern.search(line)
                        if searchresult:
                            newline = " ".join(searchresult.groups())

                            #time stamp handling
                            timestamp = searchresult.group(1)
                            timestampstr = timestamp.replace("[", "").replace("]", "")
                            timestampstr = timestampstr.split(".")[0]   #remove milliseconds
                            
                            if withinTimeDelta(timestampstr):
                                outputfile.write(newline)
                                continuePrint = True

                            break
                else:
                    # still old block, then print everyting within this block
                    if continuePrint:
                        outputfile.write(line)

filename = "C:\\Users\\eluchao\\Desktop\\D\\python\\example\\traceeaxmple.txt"

starttimedt = datetime.strptime("2016-09-08 11:06:58", "%Y-%m-%d %H:%M:%S")
endtimedt = datetime.strptime("2016-09-08 11:40:14", "%Y-%m-%d %H:%M:%S")

keyword1 = "iesa.c:331"
keyword2 = "ELIB_BC"

parsefile(filename)


        