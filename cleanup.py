# Cleanup file for making selected SNIa FITRES files pandas-compatible
import numpy as np

def fitresCleanup(fname):

    with open(fname, 'r') as f:
        dat = f.readlines()

    varlabels = dat[12]
    dat[12] = varlabels # add variable labels right on top of data

    fname = fname[:-7] + "_selected" + '.FITRES' 
    
    with open(fname, 'w') as newf:       # create new file
        newf.write("%s" % dat[12])
        
        for line in dat[13:]:
            if 'SN' in line:             # remove blank lines
                newf.write("%s" % line)  # write output

def clean_chains(fname):
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        dat = f.readlines()  

    #with open(path, 'rb') as f:
        #dat = f.read()

    newfname = 'mod' + fname

    with open(newfname, 'w') as newf:

        for line in dat[10:]:        # keep only data (no blank lines or sim headers)
            if line.startswith('0'):
                newf.write("%s" % line)  # write data output


# for cleaning up bulk SN file
def simgenFileCleanup(fname):
    with open(fname, 'r') as f:
        dat = f.readlines()

    varlabels = dat[1]
    dat[9] = varlabels               # add variable labels right on top of data

    
    fname = fname[:-4] + "_bulk" + '.DAT' # create processed bulk file
    with open(fname, 'w') as newf:

        newf.write("%s" % dat[9])    # write in the varname header 

        for line in dat[10:]:        # keep only data (no blank lines or sim headers)
            if 'SN' in line:
                newf.write("%s" % line)  # write data output


def createSNeFiles(fname, path, filenewname, nfiles):
    with open(fname, 'r') as f:
        dat = f.readlines()

    varlabels = dat[0]

    nfiles = nfiles      # how many times we want to sample the FITOPT data

    samplespace = len(dat)
    numobs = 511    # 511 SNe per sample

    #start_indx = 1   # start from the first line of data
    
    for i in range(nfiles):
        # select 511 random SNe from a sample space len(FITOPT_FILE) long.
        randomindx = np.random.choice(a=np.arange(samplespace), size=numobs, replace=False)
        #index = np.arange(start = start_indx, stop = start_indx + numobs)
        sampled = np.asarray(dat)[randomindx]

        #start_indx += numobs

        newfname = path + '{}_{}.txt'.format(filenewname, i+1)  # label each new sample
        with open(newfname, 'w') as newf:

            newf.write("%s" % dat[0])    # write in the varname header 

            for line in sampled:        # keep only data (no blank lines or sim headers)
                #if 'SN' in line:
                newf.write("%s" % line)  # write data output

     

def selectBootstrap(fname, path):
    with open(fname, 'r') as f:
        dat = f.readlines()

    varlabels = dat[0]

    nfiles = 9    # how many times we want to resample the data
    numlines = len(dat)

    for i in range(nfiles):
        randomindx = np.random.choice(a=np.arange(numlines)[1:], size=numlines, replace=True)
        resampled = np.asarray(dat)[randomindx]


        newfname = path + 'selected_{}.txt'.format(i+2)  # already have a selected_1 file
        with open(newfname, 'w') as newf:

            newf.write("%s" % dat[0])    # write in the varname header 

            for line in resampled:        # keep only data (no blank lines or sim headers)
                #if 'SN' in line:
                newf.write("%s" % line)  # write data output
        

            
