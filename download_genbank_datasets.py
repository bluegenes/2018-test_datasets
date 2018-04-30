import pandas as pd
import os
import re
import argparse
import ipfsapi
import requests
import shutil

# see README for genbank's "all" folder: https://ftp.ncbi.nih.gov/genomes/all/README.txt

def download_genbank(name, genome_path, outF, protein, rna, quiet):
    genbank_url = 'https://ftp.ncbi.nih.gov/genomes/all'
    alpha,first,second,third = re.match("([A-Z]+)_(\d{3})(\d{3})(\d{3})", name).groups()
    folder_name = name.split('_genomic.fna.gz')[0]
    genbank_path =os.path.join(genbank_url,alpha,first,second,third,folder_name)
    genome_url = os.path.join(genbank_path,name)
    if not quiet:
        print('genome: ' + genome_url)
    get_genbank_file(genome_url, outF)

    if protein:
        protein_name = folder_name + '_protein.faa.gz'
        protein_url = os.path.join(genbank_path,protein_name)
        if not quiet:
            print('protein: ' + protein_url)
        outP = outF.split('_genomic.fna.gz')[0] + '_protein.faa.gz'
        get_genbank_file(protein_url, outP)

    if rna:
        rna_name = folder_name + '_rna_from_genomic.fna.gz'
        #rna_name = folder_name + '_cds_from_genomic.fna.gz'
        rna_url = os.path.join(genbank_path,rna_name)
        if not quiet:
            print('rna: ' + rna_url)
        outR = outF.split('_genomic.fna.gz')[0] + '_rna_from_genomic.fna.gz'
        #outP = outF.split('_genomic.fna.gz')[0] + '_cds_from_genomic.fna.gz'
        get_genbank_file(rna_url, outR)


def get_genbank_file(url, outFile):
    # note that this will create an empty local file if the file does not exist on the server (some protein/rna files)
    r =requests.get(url, stream=True)
    with open(outFile, 'wb') as f:
        #with requests.get(url, stream=True) as r: # currently not working
        shutil.copyfileobj(r.raw, f)
    r.close()

def download_ipfs(genome_path, outF, ipfs_api, failed):
    ipfs_url = "/ipns/genbank.oxli.org"
    url = os.path.join(ipfs_url, genome_path)
    print(url)
    with open(outF, 'wb') as f:
        try:
            f.write(ipfs_api.cat(url))
        except:
            failed.write(url + '\n')
            pass


def download_genomes(csv, outdir, ipfs=False, genbank=False, protein=False, rna=False, quiet=False):
    genomeInfo = pd.read_csv(csv)
    csv_name = args.csv.split('.')[0]#assuming good csv naming
    outD = os.path.join(outdir,csv_name)
    failedF = os.path.join(outD, 'failed.txt')
    os.makedirs(outD, exist_ok=True)
    genomes = genomeInfo.iloc[:,2]
    if ipfs:
        api = ipfsapi.connect()
    with open (failedF, 'w') as failed:
        for g in genomes:
            out_name = g.split('/')[-1]
            out = os.path.join(outD, out_name)
            if ipfs:
                download_ipfs(g, out, api, failed)
            elif genbank:
                download_genbank(out_name, g, out, protein, rna, quiet)

if __name__ == '__main__':
    """
    """
    psr = argparse.ArgumentParser()
    psr.add_argument('csv')
    psr.add_argument('-o', '--outdir', default=os.getcwd())
    psr.add_argument('--ipfs', action='store_true')
    psr.add_argument('--genbank', action='store_true')
    psr.add_argument('--protein', action='store_true')
    psr.add_argument('--rna', action='store_true')
    psr.add_argument('--quiet', action='store_true', help='suppress stdout printing')
    args = psr.parse_args()
    download_genomes(args.csv, args.outdir, args.ipfs, args.genbank, args.protein, args.rna, args.quiet)
