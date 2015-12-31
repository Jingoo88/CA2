import sys, getopt

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:], "c:i:", ["coeffs=", "ids="])
 
for i, j in myopts:
    if i == "--ids" or i == "-i":
        print j
    else:
        print "kk"
