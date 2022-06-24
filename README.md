# In silico optimization of RNA-protein interactions for CRISPR-Cas13-based antimicrobials

In prokaryotes, RNA-protein interactions enable adaptive immunity through CRISPR-Cas systems. These defense systems utilize crRNA templates acquired from past infections to destroy invading genetic elements through crRNA-mediated nuclease activities of Cas proteins. Due to the programmability and specificity of CRISPR-Cas systems, CRISPR-based antimicrobials have the potential to be repurposed as novel antibiotics. Unlike traditional antibiotics, these CRISPR-based antimicrobials can target specific bacteria and minimize negative effects on the human microbiome during antibacterial therapy. Here, we explore the potential of CRISPR-based antimicrobials by optimizing the RNA-protein interactions of crRNAs and Cas13 proteins. First, we curate the validation dataset of Cas13 protein and CRISPR repeat pairs that are experimentally validated to interact. Second, we build the candidate dataset of CRISPR repeats that reside on the same genome as the currently known Cas13 proteins. To find optimal CRISPR-Cas13 interactions, we validate the 3-D structure prediction of crRNAs based on their experimental structures. Next, we test a number of in silico docking programs to optimize the RNA-protein interaction of crRNAs with the Cas13 proteins. From this optimized pipeline, we find a number of candidate crRNAs that have better in silico docking with the Cas13 proteins of the current studies. 


### Our GitHub largely has the following structure:

#### 1. [`crRNA_prediction`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/crRNA_prediction)
- The details on 2-D and 3-D RNA prediction, specifically on 3-D structure prediction using Rosetta can be found. Other structure prediction programs are explained in our paper.

#### 2. [`GT PDBs`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/GT_PDBs)
- The GT PDBs taken from the Protein Data Bank and have been cleaned (removed unwanted residues eg. water) can be found here.

#### 3. [`GT_FASTA`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/GT_FASTA)
- The fasta files of the GT from the Protein Data Bank can be found here, along with the shortened RNA sequences used in our experiments.

#### 4. [`Docking`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/Docking)
- The details on the pre-processing and post-processing for in silico docking can be found here, along with the codes for automatizing the use of the webservers.

#### 4. [`Validation_docking_results`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/Validation_docking_results)
- As the name entails, the results of docking the validation dataset and evaluations can be found here in the form of tables and images.

#### 5. [`Candidates_FASTA`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/Candidates_FASTA)
- The candidate crRNA sequences are stored here.

#### 6. [`Candidate_docking_result(3-D_interactive)`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/Candidate_docking_result(3-D_interactive))
- The results of docking the candidate crRNAs to the Cas proteins can be found here.

## For citation

Readers may use the following information to cite our research and dataset.

```
citation
```

```
bibtex citation
```

**Contributors**:
 - [Ho-min Park](https://github.com/powersimmani)
 - [Yunseol Park](https://github.com/YunseolPark)
 - [Urta Berani](https://github.com/urtaberani)
 - [Eunkyu Bang]()
 - [Joris Vankerschaver](https://github.com/jvkersch)
 - [Arnout Van Messem](https://github.com/avmessem)
 - [Wesley De Neve](https://github.com/wmdeneve)
 - [Hyunjin Shim](https://github.com/hjshim)

## Acknowledgement

The research and development activities described in this paper were funded by Ghent University Global Campus (GUGC).
