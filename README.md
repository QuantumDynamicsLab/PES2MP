[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8232313.svg)](https://doi.org/10.5281/zenodo.8232313) <br>
:mailbox_with_mail: dhilip@iitrpr.ac.in

# PES2MP (Potential Energy Surface Mapping to Multipole Expansion Series)
2D and 4D multipole expansion code (using [Legendre polynomials](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.legendre.html) and [Spherical Harmonics](https://shtools.github.io/SHTOOLS/) respectively) for fitting Potential Energy Surface (PES) into radial coefficients ($V_\lambda$ / $V_{\lambda1}V_{\lambda2}V_{\lambda}$) are provided as user-friendly jupyter-notebook files.<br>
Both codes (2D/4D) use least squares fit, achieved by taking the pseudo-inverse of Legendre/Spherical-Harmonics coefficients, which are saved as a 2D numpy matrix for future use. The codes are useful while studying collisional :boom: dynamics of one or both species at cold :snowflake: and ultracold :snowman: temperatures. 


The code is currently limited to rigid rotor - atom (2D) and rigid rotor - rigid rotor (4D) collision. For theoretical details please follow the paper ```N. Sathyamurthy, “Computational fitting of ab initio potential energy surfaces,” _Comput. Phys. Rep._ 3, 1–69 (1985).``` [link :monocle_face:](https://doi.org/10.1016/0167-7977(85)90007-3)


For any queries :envelope: [Dr. T. J. Dhilip Kumar](mailto:dhilip@iitrpr.ac.in) cc: [Apoorv Kushwaha](mailto:kushwaha.apoorv@gmail.com)<br />  <br />

### Update V2
-  Code 0-1 are for augmenting PES data using ML package [PESLearn](https://github.com/CCQC/PES-Learn),
-  Code 2 and 3 are for fitting PES to radial coefficients and vice-versa (to calculate fitting error),
-  Code 4 is a template to fit radial coefficients into molscat readable functions.

### V1
* The original code has been broken into 5 parts (Code_0-5),
* The old codes published in Supplementary Information *(links to articles are provided below)* can be accessed via following [link](https://github.com/apoorv-kushwaha/PES2MP/).


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


Manual: :book: [Upcoming !]() 
```diff
- Under Preparation
```

