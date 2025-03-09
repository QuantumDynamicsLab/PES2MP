''' Python script to extract cross sections and pair energy from molscat output files ''' 

# importing libraries
import re
import os
from tqdm import tqdm
import platform

# saving current directory to path
path = os.getcwd()

##################################################################################
#################### Input parameters (make changes here) ########################
##################################################################################

# enter folder name (keep this file outside the folder containing molscat files)
sig_folder = 'sigma'  # eample folder name: 'cross_sections_CC'  

filename = 'sigma.dat'    # output file name  (cross sec)
filename_PE = 'pair_E.dat'   # output file name (pair Energy)

ini   = 1           # initial file number
final = 1700        # final file number 

# the final file number will be used for extracting pair Energy

##################################################################################
######################### Extracting cross-sections ##############################
##################################################################################

os.chdir(path + '/' + sig_folder)  

START_PATTERN = re.compile('JTOTL')
END_PATTERN = re.compile('TOTAL INELASTIC')
END_PATTERN2 = re.compile('---- MOLSCAT')
newfile = open(path+"/"+filename ,"w+")

ct=1
for i in tqdm(range (ini,final+1,1)):
    if (os.path.isfile("%d.out" %(i))):
        f = open("%d.out" %(i),"r")
        match = False
        for line in f:
            if re.search(START_PATTERN, line):
                if ct == 1:
                    newfile.write(line)
                    ct+=1
                match = True
                continue
            elif re.search(END_PATTERN, line) or re.search(END_PATTERN2, line):
                if match:
                    match = False
                continue
            elif match:
                newfile.write(line)
                newfile.write('\n')
        f.close()
newfile.close() 

os.chdir(path)
sed_cmd = "sed -i '' '/^$/d' {}" if platform.system() == "Darwin" else "sed -i '/^$/d' {}"
os.system(sed_cmd.format(filename))

################################################################
################# Extracting pair energy from last file ########
################################################################

os.chdir(path + '/' + sig_folder)  

START_PATTERN_PE = re.compile('STATE-TO-STATE INTEGRAL CROSS SECTIONS')
END_PATTERN_PE = re.compile('JTOTL')

newfile_PE = open(path+"/"+filename_PE ,"w+")

if (os.path.isfile("%d.out" %(final))):
    fpe = open("%d.out" %(final),"r")
    match = False
    for line in fpe:
        if re.search(START_PATTERN_PE, line):
            match = True
            continue
        elif re.search(END_PATTERN_PE, line):
            if match:
                match = False
            continue
        elif match:
            newfile_PE.write(line)
    fpe.close()
else:
    print('file %d.out not found!'%(final))
    print('Cannot create Pair E file. Try different final file' )

newfile_PE.close() 

os.chdir(path)
os.system(sed_cmd.format(filename_PE))

##################################################################################






