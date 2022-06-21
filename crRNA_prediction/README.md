# crRNA Structure Prediction

## 2-D Prediction
All 2-D predictions were made via their respective webservers.

## 3-D Prediction

### RNAComposer
3-D RNA structure prediction with RNAComposwer was done through webserver.

### Rosetta

The Rosetta version 2021.16 was used.

For more information on 3-D RNA structure prediction with Rosetta, read their paper ["FARFAR2: Improved De Novo Rosetta Prediction of Complex Global RNA Folds"](https://www.cell.com/structure/fulltext/S0969-2126(20)30180-5?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0969212620301805%3Fshowall%3Dtrue)

#### RNA de novo
The RNA de novo function (linuxgccrelease) in the FARFAR2 protocol was used in the path ```main/source/bin``` inside the Rosetta package.

``./rna_denovo.static.linuxgccrelease -sequence "[in vitro Cas13-interacting CRISPR RNA sequence]" -secstruct "[predicted 2-D structure]" -minimize_rna true -out:file:silent [output file name].out``

The RNA sequence is given in place of the **[in vitro Cas13-interacting CRISPR RNA sequence]** box and the dot-bracket notation of the predicted 2-D structure in place of the **[predicted 2-D structure]** box. We did not implement Rosetta with RNA 2-D structure prediction software, so the dot-bracket prediction was obtained separately. With the ``minimize_rna`` function, the predicted RNA 3-D models were subjected to minimization in an all-atom scoring function used by the FARFAR2 protocol. The Rosetta output was given through the filename, which is given in place of the **[output file name]** box.

#### grep

Then, the grep function of the FARFAR2 protocol selects the best model (in terms of MFE and RMSD) of the ensemble of predicted CRISPR RNA 3-D structure models.

``grep "ˆSCORE:" [rnadenovo output file name].out | grep -v description | sort -nk2 | head -n 500 | sort -nk24 | head -n 1 | awk '{print $NF}'``

The name of the output file, obtained from the RNA de novo function, is provided in place of the ``[rnadenovo output file name]``.

``grep -v description`` prints the scores of the predicted models without description. ``sort -nk2`` sorts the models by total energy. ``Head -n 500`` picks the top 500 models, which are then sorted by RMSD value with ``sort -nk24``. Then the best RNA 3-D structure is selected with ``head -n 1``. With ``awk ‘{print $NF}’``, the tag of this structure is printed.

#### Extract PDBs

The extract PDBs function (linuxgccrelease) was used in the path ```main/source/bin``` inside the Rosetta package.

```./extract_pdbs.static.linuxgccrelease -in::file::silent [rnadenovo output file name].out -tags $TAG```

The best-RMSD and -MFE 3-D model was extracted and saved with a filename of format ``S_000001`` by ``-tags $TAG``.

#### Example

Example on 3-D structure precition of crRNA 6IV9 (chain B).

```
./rna_denovo.static.linuxgccrelease -sequence "cacuggugcaaauuugcacuagucuaaaacuccucgauuacauacacaaa" -secstruct ".(((((((((....)))))))))..........................." -minimize_rna true -out:file:silent 6iv9_rnashapes.out

grep "ˆSCORE:" 6iv9_rnashapes.out | grep -v description | sort -nk2 | head -n 500 | sort -nk24 | head -n 1 | awk '{print $NF}'

./extract_pdbs.static.linuxgccrelease -in::file::silent 6iv9_rnashapes.out -tags $TAG
```
