# test_datasets

Follow instructions in https://github.com/dib-lab/2018-ncbi-lineages to build a csv file containing a set of desired genomes, then use `download_genbank_datasets.py` to download these files from NCBI.


download small testing datasets useful for assessing tool functionality, e.g. jaccard similarity over species at increasing evol. distances


usage:

python download_genbank_datasets.py --csv denticola.csv --genbank
