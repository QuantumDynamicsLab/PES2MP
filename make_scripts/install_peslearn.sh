#!/usr/bin/env bash

conda create -y -n peslearn python=3.6 --no-default-packages
eval "$(conda shell.bash hook)"
conda activate peslearn

echo -n "Installing other dependies ---: "
conda install -y -c conda-forge -c pytorch -c omnia gpy pytorch scikit-learn pandas hyperopt cclib

echo -n "Installing tqdm ---: "
conda install -y -c conda-forge tqdm


conda activate peslearn_pes2mp
echo -n "Installing PES-Learn ---: "
git clone https://github.com/adabbott/PES-Learn.git
cd PES-Learn
python setup.py install
pip install -e .
