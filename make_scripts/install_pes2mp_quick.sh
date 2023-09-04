#!/usr/bin/env bash

conda create -y -n pes2mp_quick --no-default-packages
eval "$(conda shell.bash hook)"
conda activate pes2mp_quick

echo -n "Installing Jupyter-Notebook ---: "
conda install -y -c anaconda python
python -m pip install --upgrade pip
python -m pip install jupyter

echo -n "Installing pyshtools/tqdm/otherdependies ---: "
python -m pip install pyshtools tqdm numpy pandas scipy sympy matplotlib




