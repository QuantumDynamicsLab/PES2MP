[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8232313.svg)](https://doi.org/10.5281/zenodo.8232313) <br>
Contact: dhilip@iitrpr.ac.in

# PES2MP (Potential Energy Surface Mapping to Multipole Expansion Series)
2D and 4D multipole expansion code (using [Legendre polynomials](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.legendre.html) and [Spherical Harmonics](https://shtools.github.io/SHTOOLS/) respectively) 
for fitting PES into radial coefficients is provided as jupyter-notebook files. <br />

### Update V2
-  Code 0-1 are for splining/augmenting data using ML package [PESLearn](https://github.com/CCQC/PES-Learn)
-  Code 2 and 3 are for fitting PES to radial coefficients and vice-versa (to calculate fitting error.)
-  Code 4 is a template to fit radial coefficients into molscat readable functions.

### V1
* The original code has been broken into 4 parts.
* The old codes published in Supplementary Information can be accessed via following [link](https://github.com/apoorv-kushwaha/PES2MP/)

Both codes use least square fit (achieved by taking the pseudo-inverse of Legendre/Spherical-Harmonics coefficients stored in a 2D matrix).<br />
Currently limited to rigid rotor - atom (2D) and rigid rotor - rigid rotor (4D) collision

For any queries contact [Dr. T. J. Dhilip Kumar](mailto:dhilip@iitrpr.ac.in) cc: (mailto:kushwaha.apoorv@gmail.com)<br />

### 2D PES (Atom - Rigid Rotor collision)
File 2: CODE_2_PES2MP_2D.ipynb <br />
_Uses [[scipy.special]](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.legendre.html) for Legendre coefficient_


<img src="https://github.com/apoorv-kushwaha/Multipole/blob/main/jacobi22.png" width="250">

Link: [[Link to paper: See Supplementary Information]](https://doi.org/10.1002/qua.27007) 

```diff 
# Bibtex citation for 2D code: multipole expansion of 2D Potential Energy Surface
@article{Kushwaha2023Jan,
	author = {Kushwaha, Apoorv and Kumar, Thogluva Janardhanan Dhilip},
	title = {{Benchmarking PES-Learn's machine learning models predicting accurate potential energy surface for quantum scattering}},
	journal = {Int. J. Quantum Chem.},
	volume = {123},
	number = {1},
	pages = {e27007},
	year = {2023},
	month = jan,
	issn = {0020-7608},
	publisher = {John Wiley {\&} Sons, Ltd},
	doi = {10.1002/qua.27007}
}
```

### 4D PES (Two Rigid Rotors) 

_Uses [[pyshtools]](https://shtools.github.io/SHTOOLS/) for calculating spherical harmonics_
**(need separate installation: Instructions are provided in jupyter-notebook file)<br />**

File 2: CODE_2_PES2MP_4D.ipynb <br />
<img src="https://github.com/apoorv-kushwaha/Multipole/blob/main/jac_final.png" width="500">

Link: [[Link to paper: See Supplementary Information]](https://doi.org/10.1063/5.0161335) 

```diff
# Article citation for 4D code: multipole expansion of 4D Potential Energy Surface
@article{Kushwaha2023Aug,
	author = {Kushwaha, Apoorv and Dhilip Kumar, T. J.},
	title = {{4D potential energy surface of NCCN{\textendash}H2 collision: Rotational dynamics by p-H2 and o-H2 at interstellar temperatures}},
	journal = {J. Chem. Phys.},
	volume = {159},
	number = {7},
	year = {2023},
	month = aug,
	issn = {0021-9606},
	publisher = {AIP Publishing},
	doi = {10.1063/5.0161335}
}
```

Manual: [Upcoming !]() 
```diff
- Under Preparation
```

```diff
# Software citation
@software{kushwaha_apoorv_2023_8232313,
  author       = {Kushwaha, Apoorv and
                  Dhilip Kumar, T. J.},
  title        = {QuantumDynamicsLab/PES2MP},
  month        = aug,
  year         = 2023,
  note         = {If you use this software, please cite it as below.},
  publisher    = {Zenodo},
  version      = {v1.0.3},
  doi          = {10.5281/zenodo.8232313},
  url          = {https://doi.org/10.5281/zenodo.8232313}
}
```

