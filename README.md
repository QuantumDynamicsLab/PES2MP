# PES2MP
The program can generate Pis4 based Potential energy surface internally (with capabilities to create input files for Gaussian, Molpro and Psi4 for external calculations) for atom-atom (1D), rigid rotor(RR)-atom (2D) and RR-RR (4D) collision. A TensorFlow (keras) based neural networks model can be created to augment the surface with a high degree of accuracy (at both minima and high energy regions) OR (if angular augmentation is not necessary) radial terms for each angle(s) can be analytically fitted to get missing R values. Finally, the PES is fitted into Legendre (2D) and Bispherical Harmonics (4D) to get radial terms which can be used to study rotational transitions induced by the collider. 


To be updated:
- (a) Full programmer's guide 
- (b) Example files
- :mailbox_with_mail: dhilip@iitrpr.ac.in



## Multipole Expansion
2D and 4D multipole expansion code (using [Legendre polynomials](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.legendre.html) and [Spherical Harmonics](https://shtools.github.io/SHTOOLS/) respectively) for fitting Potential Energy Surface (PES) into radial coefficients ($V_\lambda$ / $V_{\lambda1}V_{\lambda2}V_{\lambda}$) are provided as user-friendly jupyter-notebook files.<br>
Both codes (2D/4D) use least squares fit, achieved by taking the pseudo-inverse of Legendre/Spherical-Harmonics coefficients, which are saved as a 2D numpy matrix for future use. The codes are useful while studying collisional :boom: dynamics of one or both species at cold :snowflake: and ultracold :snowman: temperatures. 


The code is currently limited to rigid rotor - atom (2D) and rigid rotor - rigid rotor (4D) collision. For theoretical details please follow the paper ```N. Sathyamurthy, “Computational fitting of ab initio potential energy surfaces,” _Comput. Phys. Rep._ 3, 1–69 (1985).``` [link :monocle_face:](https://doi.org/10.1016/0167-7977(85)90007-3)


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


