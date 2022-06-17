# Docking
In order to dock Cas13 proteins and crRNAs, the ground truth (GT) validation datasets were randomly rotated. Furthermore, the docking runs were automated via python.

## Random Rotations of Receptors and Ligands
GT validation datasets were taken and randomly rotated via the python script `make_rotationPDB.py`. 

## Docking Runs
The docking programs used in this section are HADDOCK, HDOCK, and PyDockDNA. For each, only the webserver was used. In ordr to automate the docking runs, we made use of Selenium and ChromeDriver. These automations are found in each of the python files named after the respective docking programs: `haddock.py`, `hdock.py`, and `pyockdna.py`.

The functions `haddock_web`, `hdock_web`, and `pyockdna_web` in the respective python scripts are used to submit the receptor and ligands, and any other parameters. Then the 
