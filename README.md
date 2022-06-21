# In silico optimization of RNA-protein interactions for CRISPR-Cas13-based antimicrobials

RNA-protein interactions are crucial for diverse biological processes. In prokaryotes, RNA-protein interactions enable adaptive immunity through CRISPR-Cas systems. These defense systems utilize CRISPR RNA (crRNA) templates acquired from past infections to destroy foreign genetic elements through crRNA-mediated nuclease activities of Cas proteins. Thanks to the programmability and specificity of CRISPR-Cas systems, CRISPR-based antimicrobials have the potential to be repurposed as new types of antibiotics. Unlike traditional antibiotics, these CRISPR-based antimicrobials can be designed to target specific bacteria and minimize detrimental effects on the human microbiome during antibacterial therapy. Here, we explore the potential of CRISPR-based antimicrobials by optimizing the RNA-protein interactions of crRNAs and Cas13 proteins. CRISPR-Cas13 systems are unique as they degrade specific foreign RNAs using the crRNA template, which leads to non-specific RNase activities and cell cycle arrest. We show that a high proportion of the Cas13 systems have no colocalized CRISPR arrays, and the lack of direct association between crRNAs and Cas proteins may result in suboptimal RNA-protein interactions in the current tools. Here, we investigate the RNA-protein interactions of the Cas13-based systems by curating the validation dataset of Cas13 protein and CRISPR repeat pairs that are experimentally validated to interact, and the candidate dataset of CRISPR repeats that reside on the same genome as the currently known Cas13 proteins. To find optimal CRISPR-Cas13 interactions, we first validate the 3-D structure prediction of crRNAs based on their experimental structures. Next, we test a number of RNA-protein interaction programs to optimize the in silico docking of crRNAs with the Cas13 proteins. From this optimized pipeline, we find a number of candidate crRNAs that have comparable or better in silico docking with the Cas13 proteins of the current tools. This study fully automatizes the in silico optimization of RNA-protein interactions as an efficient preliminary step for designing effective CRISPR-Cas13-based antimicrobials. --> **To be paraphrased**

### Our GitHub largely has the following structure:

#### 1. [`crRNA_prediction`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/crRNA_prediction)
- The details on 2-D and 3-D RNA prediction, specifically on 3-D structure prediction using Rosetta can be found. Other structure prediction programs are explained in our paper.

#### 2. [`GT PDBs`](https://github.com/hshimlab/CRISPR-Cas-interaction/tree/main/GT_PDBs)
- The GT PDBs from the Protein Data Bank can be found here.

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
