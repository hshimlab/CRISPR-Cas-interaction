# crRNA Structure Prediction

%

```./rna_denovo.static.linuxgccrelease -sequence "[in vitro Cas13-interacting CRISPR RNA sequence]" -secstruct "[predicted 2-D structure]" -minimize_rna true -out:file:silent [5WLH_RNAfold+Rosetta].out```

```grep "ˆSCORE:" [5WLH_RNAfold+Rosetta].out | grep -v description | sort -nk2 | head -n 500 | sort -nk24 | head -n 1 | awk '{print $NF}'```

```./extract_pdbs.static.linuxgccrelease -in::file::silent[5WLH_RNAfold+Rosetta]```

```./rna_denovo.static.linuxgccrelease -sequence "cacuggugcaaauuugcacuagucuaaaacuccucgauuacauacacaaa" -secstruct ".(((((((((....)))))))))..........................." -minimize_rna true -out:file:silent 6iv9_rnashapes.out

grep "ˆSCORE:" 6iv9_rnashapes.out | grep -v description | sort -nk2 | head -n 500 | sort -nk24 | head -n 1 | awk '{print $NF}'

./extract_pdbs.static.linuxgccrelease -in::file::silent 6iv9_rnashapes.out -tags $TAG```
