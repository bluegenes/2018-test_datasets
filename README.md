# Download Test Datasets from NCBI

Intended for downloading small testing datasets useful for assessing tool functionality, e.g. jaccard similarity over species at increasing evol. distances. 


Clone the Repo:
```
git clone https://github.com/bluegenes/2018-test_datasets
cd 2018-test_datasets
```

Install the required software. To do this in a new conda environment called `dl-test-datasets-env`, run the following:

```
conda env create -f environment.yml -n dl-test-datasets-env
# then enter into that environment:
conda activate dl-test-datasets-env
```

usage:

`python download_genbank_datasets.py denticola.csv -o test --subfolders --genbank`


If you'd like to download RNA or Protein files as well, add the `--rna` or `--protein` flags.
