##################################################################################

printf " \n ----**** CREATING PES2MP Quick ENVIRONMENT **** ---:  \n "

conda create -y -n pes2mp_q python=3.11 --no-default-packages
eval "$(conda shell.bash hook)"
conda activate pes2mp_q

printf " \n Installing psi4 ---:  \n "
conda install -y psi4 python=3.11 -c conda-forge/label/libint_dev -c conda-forge 
printf " \n Updating psi4 ---:  \n "
conda update -y psi4 -c conda-forge

printf " \n Installing Other Dependies ---:  \n "
conda install -y -c anaconda python
python -m pip install --upgrade pip
python -m pip install tensorflow keras-tuner pyshtools numpy pandas pyarrow scipy sympy matplotlib tqdm scikit-learn jupyter spyder #lmfit pydot python-graphviz
conda install -y lmfit pydot python-graphviz -c conda-forge 

# To use GPU acceleration in MacOS, uncomment the lines below
#python -m pip uninstall tensorflow
#python -m pip install tensorflow-macos
#python -m pip install tensorflow-metal


# optional d3/d4 dispersion correction for Psi4 (works with psithon)
# Refer https://github.com/dftd4/dftd4 and https://psicode.org/psi4manual/master/dftd3.html
conda install dftd3-python  -y -c conda-forge   # or conda install dftd3-python  -y -c conda-forge 
conda install dftd4 dftd4-python -y -c conda-forge
printf " \n ----**** PES2MP Quick ENVIRONMENT CREATED **** ---:  \n "

##################################################################################
