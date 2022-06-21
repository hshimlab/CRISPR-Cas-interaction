# Docking
In order to dock Cas13 proteins and crRNAs, the ground truth (GT) validation datasets were randomly rotated. Furthermore, the docking runs were automated via python.

Python 3.8.3, Selenium v.3.141.0, ChromeDriver v. 100.0.4896.60, urllib.request v.3.8, PyVirtualDisplay v.3.0, pandas v.1.0.5, and PyMOL v.2.4.1 were used.

## Random Rotations of Receptors and Ligands
GT validation datasets were taken and randomly rotated via the python script `make_rotationPDB.py`.

## Pre-processing of GT PDBs
The GT PDBs had to be pre-processed for HADDOCK to separate ensembles.

## Docking Runs
The docking programs used in this section are HADDOCK, HDOCK, and PyDockDNA. For each, only the webserver was used. In ordr to automate the docking runs, we made use of Selenium and ChromeDriver. These automations are found in each of the python files named after the respective docking programs: `haddock.py`, `hdock.py`, and `pyockdna.py`.

The functions `haddock_web`, `hdock_web`, and `pyockdna_web` in the respective python scripts are used to submit the receptor and ligands with the necessary parameters. Then the results of the docking are downloaded and their docking scores are written.


## Post-processing
The resultant PDBs given by each docking program had different formats. Therefore, they had to be made into one single format.
