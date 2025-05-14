#python file to collect data from each subfolder
import re
import os
# loop for each angle subdirectory

path = os.getcwd()

##############################################################
PES_folder = path + '/Gaussian_CP/'

f1 = open(os.path.join(path, "PES_raw.dat"), "w+")
f2 = open(os.path.join(path, "PES_err.dat"), "w+")

num_files = 1424
##############################################################

# Change to the user-specified directory
if os.path.isdir(PES_folder):
    os.chdir(PES_folder)


ct = 1
pattern1=re.compile(" R = ")
pattern2 = re.compile("Counterpoise corrected energy")

for i in range (0,num_files+1,1):
    if (os.path.isfile("%d.log" %(i))):
        f= open("%d.log" %(i),"r")
        #print("first file opened!")
        for line in f:
            for match in re.finditer(pattern1,line):
                #print("first pattern found!")
                f1.write(line)
        f.close()
        f= open("%d.log" %(i),"r")
        for line in f:
            for match in re.finditer(pattern2,line):
                f1.write(line)
        f.close()
    else:
        f2.write("%d.out does not exist" %(i) )
f1.close()
f2.close()
if os.path.isdir(path):
    os.chdir(path)

with open("PES_raw.dat") as f1, open("PES.dat", "w") as f3:
    buffer = ""
    for line in f1:
        line = line.strip()
        if line.startswith("R ="):
            parts = line.replace("R =", "").replace("Theta=", "").split(",")
            buffer = f"{parts[0].strip()}, {parts[1].strip()}"
        elif "Counterpoise corrected energy" in line:
            energy = line.split("=")[-1].strip()
            f3.write(f"{buffer}, {energy}\n")
f3.close()

