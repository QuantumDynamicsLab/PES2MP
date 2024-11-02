# PES2MP
The program can generate Pis4 based Potential energy surface internally (with capabilities to create input files for Gaussian, Molpro and Psi4 for external calculations) for atom-atom (1D), rigid rotor(RR)-atom (2D) and RR-RR (4D) collision. A TensorFlow (keras) based neural networks model can be created to augment the surface with a high degree of accuracy (at both minima and high energy regions) OR (if angular augmentation is not necessary) radial terms for each angle(s) can be analytically fitted to get missing R values. Finally, the PES is fitted into Legendre (2D) and Bispherical Harmonics (4D) to get radial terms which can be used to study rotational transitions induced by the collider. The codes are useful while studying collisional :boom: dynamics of one or both species at cold :snowflake: and ultracold :snowman: temperatures. 


To be updated:
- (a) Full programmer's guide 
- (b) Example files
- :mailbox_with_mail: dhilip@iitrpr.ac.in

## PES Generation :: 1D/2D/4D rigid rotor PES.
The Python-based program automatically creates PES for various collisional pairs e.g. atom-atom (1D), rigid rotor-atom (2D) and rigid rotor-rigid rotor (4D). The program calculates and moves respective Rigid Rotor(s) (RR) to COM and generates PES using Psi4 (for rough estimation). The program also generates input files for external calculations using Molpro/Gaussian/Psi4 along with publication-ready plots with customization (title, axis, etc.) in pdf/eps formats. Simple templates (input_files.py) are provided for Psi4, Gaussian and Molpro which automatically creates required input files (for each individual coordinate in XYZ format) for respective ab initio software packages. Sample input files are provided for Single point, BSSE-corrected and CBS-extrapolation schemes for Molpro. Gaussian template defaults to BSSE corrected PES, while Psi4 can be used both internally (using pes2mp) or externally (recommended for large calculations).

## NN Model :: NN model to augment and/or get missing data points.
The program can be utilized to separately fit minima and high energy region for a good fit. The underlying package for the NN model is TensorFlow, which can learn multiple outputs simultaneously and is not restricted by dimensionality (i.e. data can have N inputs and M output columns). The program also keeps boundary elements (of input features) in the training dataset to prevent boundary errors. There are two models: PES-specific (default) and Generic. The PES-specific model uses Gaussian activation functions (custom-made) and a modified Slater function for high-energy and long-range extrapolation. In the generic model, GELU is the default activation function. For finding the most suitable model (layers/nodes/activation function), keras-tuner’s (package) Bayesian Optimization tuning is used which utilises the Gaussian process to find optimum parameters within a reasonably defined search space.

## Multipole Expansion
The radial terms ($V_\Lambda$) are obtained by expanding the interaction potential (i.e. 2D/4D PES) in a set of orthogonal functions (Legendre [2D] and two Spherical harmonics [4D]) of the internal coordinates ([R, $\theta$] and [R, $\phi, \theta_2, \theta_1$]). The current implementation takes PES (must not have any coordinate missing) and multiples it with the pseudo-inverse matrix containing Legendre/Spherical harmonics coefficients to get radial terms. Warning: The number of angles must not be less than λ as it will result in poor fit which can be visualized by recreating the PES.
2D and 4D multipole expansion code (using [Legendre polynomials](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.legendre.html) and [Spherical Harmonics](https://shtools.github.io/SHTOOLS/) respectively) for fitting Potential Energy Surface (PES) into radial coefficients ($V_\lambda$ / $V_{\lambda1}V_{\lambda2}V_{\lambda}$) are provided as user-friendly jupyter-notebook files.<br>
Both codes (2D/4D) use least squares fit, achieved by taking the pseudo-inverse of Legendre/Spherical-Harmonics coefficients, which are saved as a 2D numpy matrix for future use. 
The code is currently limited to rigid rotor - atom (2D) and rigid rotor - rigid rotor (4D) collision. For theoretical details please follow the paper ```N. Sathyamurthy, “Computational fitting of ab initio potential energy surfaces,” _Comput. Phys. Rep._ 3, 1–69 (1985).``` [link :monocle_face:](https://doi.org/10.1016/0167-7977(85)90007-3)

## Curve fit :: Fit 1D PES and/or radial terms into analytical expression.
The radial terms ($V_\Lambda$) can be fitted into a series of power/exponential functions provided with the pes2mp package or user-defined function for complex fit. Extrapolation schemes ($R^{−6}/R^{−4}/R^{−3}/R^{−x}$ etc.) are also available with plots (optional). After fitting the PES into MOLSCAT readable functions, the PES can be recreated (with a residual plot) to verify whether a good fit is obtained or not.

## MOLSCAT readable output :: Available for general-purpose version of POTENL subroutine
The curve fit produces an output which is MOLSCAT readable for direct utilization in &potl block. The feature is available in a general-purpose version of the subroutine POTENL of MOLSCAT 2020. The same can be utilized to calculate cross- sections for rotational (de-)excitation of two colliding species at cold and ultracold temperatures.

## Plots :: Plot PES, residual and curve fits.
PES plots are available as 1D (R vs E) and polar (R,θ vs E). For 2D/4D PES, certain angle combinations can be chosen for plots to prevent cluttering. Residual (error) plots can be automatically generated for NN/radial-terms generated PES. The curve fit with various functions can also be visualized along with any extrapolation function (if used). Apart from these, many other relevant plots are also provided for NN module.

For any queries :envelope: [Dr. T. J. Dhilip Kumar](mailto:dhilip@iitrpr.ac.in) cc: [Apoorv Kushwaha](mailto:kushwaha.apoorv@gmail.com)<br />  <br />

<details><summary>Installation Instructions:</summary>

The makefiles (inside `make_scripts folder`) are tested on Linux and MacOS. The quick install files do not use `conda install` (where solving environments can take hours), instead, it uses `python -m pip`. However, all 4 files create separate environments and can be run without clashing with each other. To understand more [read :snake:](https://www.anaconda.com/blog/understanding-and-improving-condas-performance)

##### Install Anaconda 
- Install anaconda
- Open conda promot<br />
 The command prompt will show `base' meaning base conda environment. 
##### For conda install (recommended), enter:
- run ``chmod +x install_pes2mp.sh``
- run ``./install_pes2mp.sh``
##### For quick install (uses python -m pip: can cause error due to conflicting packages):
 - run ``chmod +x install_pes2mp_quick.sh`` (recommended) or ``chmod +x install_pes2mp_quick.sh`` {See manual for more information}
- run ``./install_pes2mp_quick.sh``<br />
  </details>

<details><summary>Running PES2MP: </summary>
	
### Running PES2MP
The program can be run by keeping the input file (e.g. pesgen1D.py) 

#### Direct execution:
- run ``conda activate pes2mp`` or `conda activate pes2mp_quick` depending on installation
- run ``python3 pes2mp.py pesgen1D ``
#### Shorter execution (requires one-time update of bashrc): 
- open bashrc in Ubuntu (or bash_profile in MacOS) and add  ``pes2mp ()
{python3 pes2mp.py $1
}`` at end of file. Save and exit.
- The command for running PES2MP will now be ``pes2mp pesgen1D ``


