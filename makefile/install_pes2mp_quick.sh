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
python -m pip install tensorflow keras-tuner pyshtools tqdm numpy pandas scipy sympy matplotlib tqdm scikit-learn jupyter spyder #lmfit pydot python-graphviz
conda install -y -c lmfit pydot python-graphviz -c conda-forge 

printf " \n ----**** PES2MP Quick ENVIRONMENT CREATED **** ---:  \n "

##################################################################################
