# PES2MP
The program can generate Pis4 based Potential energy surface internally (with capabilities to create input files for Gaussian, Molpro and Psi4 for external calculations) for atom-atom (1D), rigid rotor(RR)-atom (2D) and RR-RR (4D) collision. A TensorFlow (keras) based neural networks model can be created to augment the surface with a high degree of accuracy (at both minima and high energy regions) OR (if angular augmentation is not necessary) radial terms for each angle(s) can be analytically fitted to get missing R values. Finally, the PES is fitted into Legendre (2D) and Bispherical Harmonics (4D) to get radial terms which can be used to study rotational transitions induced by the collider. 


To be updated:
(a) Full programmer's guide 
(b) Debugging files
