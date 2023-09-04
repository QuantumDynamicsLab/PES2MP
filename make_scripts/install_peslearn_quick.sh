#!/usr/bin/env bash

conda create -y -n peslearn_quick python=3.6 --no-default-packages
eval "$(conda shell.bash hook)"
conda activate peslearn_quick

echo -n "Installing Jupyter-Notebook ---: "
conda install -y -c anaconda python
python -m pip install --upgrade pip
python -m pip install jupyter

echo -n "Installing tqdm ---: "
python -m pip install tqdm

echo -n "Installing other dependies ---: "
python -m pip install numpy pandas scipy sympy matplotlib

echo -n "Installing peslearn dependies ---: "
python -m pip install gpy torch scikit-learn hyperopt cclib

echo -n "Installing PES-Learn ---: "
git clone https://github.com/adabbott/PES-Learn.git
cd PES-Learn
python setup.py install
pip install -e .
