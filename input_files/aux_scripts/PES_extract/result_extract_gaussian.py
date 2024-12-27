#python file to collect data from each subfolder
import re
import os
# loop for each angle subdirectory

path = os.getcwd()

##############################################################
PES_folder = path + '/Molpro_CP/'

f1 = open(os.path.join(path, "PES.dat"), "w+")
f2 = open(os.path.join(path, "PES_err.dat"), "w+")

num_files = 6371
##############################################################

# Change to the user-specified directory
if os.path.isdir(PES_folder):
    os.chdir(PES_folder)


ct = 1
pattern1=re.compile("R = ")
pattern2 = re.compile("sum of fragments =")

for i in range (1,num_files+1,1):
    if (os.path.isfile("%d.out" %(i))):
        f= open("%d.out" %(i),"r")
        print("first file opened!")
        for line in f:
            for match in re.finditer(pattern1,line):
                print("first pattern found!")
                f1.write(line)
        for line in f:
            for match in re.finditer(pattern2,line):
                f1.write(line)
        f.close()
    else:
        f2.write("%d.out does not exist" %(i) )
f1.close()
f2.close()
