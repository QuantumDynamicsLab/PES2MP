#!/usr/bin/env bash

conda create -y -n pes2mp --no-default-packages
eval "$(conda shell.bash hook)"
conda activate pes2mp

echo -n "Installing pyshtools ---: "
conda install -y -c conda-forge pyshtools

echo -n "Installing tqdm ---: "
conda install -y -c conda-forge tqdm

echo -n "Installing other dependies ---: "
conda install -y -c conda-forge numpy pandas scipy sympy matplotlib

echo -n "Installing Jupyter-Notebook ---: "
python -m pip install --upgrade pip
python -m pip install jupyter


