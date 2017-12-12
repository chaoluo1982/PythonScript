import os
import re
import sys

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



    

    searchPattern1 = re.compile(r"""^(\[[^]]+\]).*          #group, match trace time, [^]] means match anything except ]
                                (boardCtrl[.]cc)            #match this keywords
                                .*                          #anything in between
                               (msg\s{1}=.*\n)              #group, match msg = ...., \s{1} means we must have 1 space here, [^}] means match anything except }, space will be ignored so it must be stated and escaped.
                               """, re.X)
    searchPatternList.append(searchPattern1)
#
#    
#    searchPattern2 = re.compile(r"""^(\[[^]]+\]).*           #group 1, match trace time, [^]] means match anything except ]
#                               (ELIB_BC.*\n)              #group 2, match msg = ...., \s{1} means we must have 1 space here, [^}] means match anything except }, space will be ignored so it must be stated and escaped.
#                               """, re.X)
#   searchPatternList.append(searchPattern2)

    
    (pathname, filename) = os.path.split(fullfilename)  # split to paht and filename
    pathname = os.path.abspath(pathname)
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
                            #newline = " ".join(searchresult.groups())
                            #outputfile.write(newline)
		            outputfile.write(line)
                            continuePrint = True
                            break
                else:
                    # still old block, then print everyting within this block
                    if continuePrint:
                        outputfile.write(line)

def main(filename):
    parsefile(filename)

if __name__ == "__main__":
    main(sys.argv[1])

        
