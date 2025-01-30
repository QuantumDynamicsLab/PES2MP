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
conda install -y keras-tuner pyshtools tensorflow tqdm numpy pandas scipy sympy matplotlib scikit-learn jupyter spyder lmfit pydot python-graphviz -c conda-forge 

# optional d3/d4 dispersion correction for Psi4 (works with psithon)
# Refer https://github.com/dftd4/dftd4 and https://psicode.org/psi4manual/master/dftd3.html
#conda install dftd3  -y -c psi4   # or conda install dftd3-python  -y -c conda-forge 
#conda install dftd4 dftd4-python -y -c conda-forge
printf " \n ----**** PES2MP ENVIRONMENT CREATED **** ---:  \n "

##################################################################################
