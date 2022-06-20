# crRNA Structure Prediction

## 3-D Prediction

### Rosetta

rosetta_bin_linux_2021.16.61629_bundle

For RNA software combinations with Rosetta, the FARFAR2 protocol was applied. In the code for the RNA de novo function, Linuxgccrelease made it possible for Linux to read the given CRISPR RNA sequence.

```./rna_denovo.static.linuxgccrelease -sequence "[in vitro Cas13-interacting CRISPR RNA sequence]" -secstruct "[predicted 2-D structure]" -minimize_rna true -out:file:silent [5WLH_RNAfold+Rosetta].out```

The CRISPR RNA sequences of the experimentally validated dataset were given in place of the [in vitro Cas13-interacting CRISPR RNA sequence] box and the dot-bracket notation of the predicted 2-D structure in place of the [predicted 2-D structure] box. Rosetta is not implemented with RNA 2-D structure prediction software, so the dot-bracket prediction was obtained separately. With the minimize_rna function, the predicted RNA 3-D models were subjected to minimization in an all-atom scoring function used by the FARFAR2 protocol. The Rosetta file was given the desired name by out:file:silent (e.g. 5WLH_RNAfold+Rosetta).


```grep "ˆSCORE:" [5WLH_RNAfold+Rosetta].out | grep -v description | sort -nk2 | head -n 500 | sort -nk24 | head -n 1 | awk '{print $NF}'```

The grep function of the FARFAR2 protocol selected the best model (in terms of MFE and RMSD) of the ensemble of predicted CRISPR RNA 3-D structure models. In this code, grep -v description printed the scores of the predicted models without description. The sort -nk2 function sorted the models by total energy. Head -n 500 picked the top 500 models. This top 500 was then sorted by RMSD value with sort -nk24 and the best RNA 3-D structure was selected with head -n 1. With awk ‘{print $NF}’ the tag of this structure was printed.

```./extract_pdbs.static.linuxgccrelease -in::file::silent[5WLH_RNAfold+Rosetta]```

The best-RMSD and -MFE 3-D model was extracted with the extract_pdbs.static.linuxgccrelease function and saved with a filename of format S_000001 by -tags $TAG.

``` ./rna_denovo.static.linuxgccrelease -sequence "cacuggugcaaauuugcacuagucuaaaacuccucgauuacauacacaaa" -secstruct ".(((((((((....)))))))))..........................." -minimize_rna true -out:file:silent 6iv9_rnashapes.out

grep "ˆSCORE:" 6iv9_rnashapes.out | grep -v description | sort -nk2 | head -n 500 | sort -nk24 | head -n 1 | awk '{print $NF}'

./extract_pdbs.static.linuxgccrelease -in::file::silent 6iv9_rnashapes.out -tags $TAG ```

