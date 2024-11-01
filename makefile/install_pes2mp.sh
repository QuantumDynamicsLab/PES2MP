##################################################################################

printf " \n ----**** CREATING PES2MP ENVIRONMENT **** ---:  \n "

conda create -y -n pes2mp python=3.11 --no-default-packages
eval "$(conda shell.bash hook)"
conda activate pes2mp

printf " \n Installing psi4 ---:  \n "
conda install -y psi4 python=3.11 -c conda-forge/label/libint_dev -c conda-forge 
printf " \n Updating psi4 ---:  \n "
conda update -y psi4 -c conda-forge

printf " \n Installing Other Dependies ---:  \n "
conda install -y keras-tuner pyshtools tensorflow tqdm numpy pandas scipy sympy matplotlib tqdm scikit-learn jupyter spyder lmfit pydot python-graphviz -c conda-forge 
#conda install -y -c anaconda pydot 
printf " \n ----**** PES2MP ENVIRONMENT CREATED **** ---:  \n "

##################################################################################
