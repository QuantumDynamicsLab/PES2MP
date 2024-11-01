#python file to collect data from each subfolder
import re
import os
# loop for each angle subdirectory

path = os.getcwd()
os.chdir(path+'/cross_sections_CC__para')

START_PATTERN = re.compile('JTOTL')
END_PATTERN = re.compile('TOTAL INELASTIC')
END_PATTERN2 = re.compile('---- MOLSCAT')
newfile = open(path+"/sigma.dat" ,"w+")

ct=1
for i in range (1,5000,1):
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
os.system("sed -i \'/^$/d\' sigma.dat")










