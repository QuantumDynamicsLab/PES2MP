# PES2MP (Potential Energy Surface Mapping to Multipole Expansion Series)
## Multipole expansion
2D and 4D multipole expansion code (using Legendre polynomials and Spherical Harmonics respectively) 
for fitting PES into radial coefficients is provided as jupyter-notebook files. <br />

Both codes use least square fit (achieved by taking the pseudo-inverse of Legendre/Spherical-Harmonics coefficients stored in a 2D matrix).<br />
Currently limited to rigid rotor - atom (2D) and rigid rotor - rigid rotor (4D) collision

For any queries contact [Dr. T. J. Dhilip Kumar](mailto:dhilip@iitrpr.ac.in) cc: (mailto:kushwaha.apoorv@gmail.com)<br />

### File 1: 2D_multipole_inv.ipynb
_Uses scipy.special for Legendre coefficient_

2D PES (Atom - Rigid Rotor collision)<br />
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

### File 2: Use 4D_SF_expansion.ipynb

_Uses pyshtools for calculating spherical harmonics_
**(need separate installation: Instructions are provided in jupyter-notebook file)<br />**

4D PES (Two Rigid Rotors)<br />
<img src="https://github.com/apoorv-kushwaha/Multipole/blob/main/jac_final.png" width="500">

Link: [Upcoming Link]() 

```diff
# Article citation for 4D code: multipole expansion of 4D Potential Energy Surface

! bibliography: Upcoming.bib
```
