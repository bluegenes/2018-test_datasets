# Download Test Datasets from NCBI

Intended for downloading small testing datasets useful for assessing tool functionality, e.g. jaccard similarity over species at increasing evol. distances. 


usage:

`python download_genbank_datasets.py denticola.csv -o test --subfolders --genbank`


If you'd like to download RNA or Protein files as well, add the `--rna` or `--protein` flags.
