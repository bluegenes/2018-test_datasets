import pandas as pd
import sys
import os
import re
import argparse
import requests
import shutil
# import ipfsapi
# import ipfshttpclient

# see README for genbank's "all" folder: https://ftp.ncbi.nih.gov/genomes/all/README.txt

def download_genbank(name, genome_path, outD, protein, rna, quiet, subfolders, failed):
    if subfolders:
        genomic_outD = os.path.join(outD, "genomic")
        rna_outD = os.path.join(outD, "rna")
        protein_outD = os.path.join(outD, "protein")
    else:
        genomic_outD = os.path.join(outD)
        rna_outD = os.path.join(outD)
        protein_outD = os.path.join(outD)

    genbank_url = 'https://ftp.ncbi.nih.gov/genomes/all'
    alpha,first,second,third = re.match("([A-Z]+)_(\d{3})(\d{3})(\d{3})", name).groups()
    folder_name = name.split('_genomic.fna.gz')[0]
    genbank_path =os.path.join(genbank_url,alpha,first,second,third,folder_name)
    genome_url = os.path.join(genbank_path,name)
    if not quiet:
        print('genome: ' + genome_url)

    genomic_outF = os.path.join(genomic_outD, name)
    if not os.path.exists(genomic_outD):
        os.makedirs(genomic_outD, exist_ok=True)
    get_genbank_file(genome_url, genomic_outF)

    if protein:
        protein_name = folder_name + '_protein.faa.gz'
        protein_url = os.path.join(genbank_path,protein_name)
        if not quiet:
            print('protein: ' + protein_url)
        prot_name = name.split('_genomic.fna.gz')[0] + '_protein.faa.gz'
        protein_outF = os.path.join(protein_outD, prot_name)
        if not os.path.exists(protein_outD):
            os.makedirs(protein_outD, exist_ok=True)
        get_genbank_file(protein_url, protein_outF)

    if rna:
        rna_name = folder_name + '_rna_from_genomic.fna.gz'
        #rna_name = folder_name + '_cds_from_genomic.fna.gz'
        rna_url = os.path.join(genbank_path,rna_name)
        if not quiet:
            print('rna: ' + rna_url)
        rna_name = name.split('_genomic.fna.gz')[0] + '_rna_from_genomic.fna.gz'
        rna_outF = os.path.join(rna_outD, rna_name)
        if not os.path.exists(rna_outD):
            os.makedirs(rna_outD, exist_ok=True)
        #outP = outF.split('_genomic.fna.gz')[0] + '_cds_from_genomic.fna.gz'
        get_genbank_file(rna_url, rna_outF)


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


def download_genomes(csv, outdir, ipfs=False, genbank=False, protein=False, rna=False, quiet=False, subfolders=False):
    genomeInfo = pd.read_csv(csv)
    csv_name = args.csv.split('.')[0]#assuming good csv naming
    outD = os.path.join(outdir,csv_name)
    failedF = os.path.join(outD, 'failed.txt')
    genomes = genomeInfo.iloc[:,2]
    if not os.path.exists(outD):
        os.makedirs(outD, exist_ok=True)
    if ipfs:
        sys.stdout.write("please use genbank download with '--genbank'")
        sys.exit(0)
        #api = ipfsapi.connect()
    with open (failedF, 'w') as failed:
        for g in genomes:
            out_name = g.split('/')[-1]
            out = os.path.join(outD, out_name)
            if ipfs:
                download_ipfs(g, out, api, failed)
            elif genbank:
                download_genbank(out_name, g, outD, protein, rna, quiet, subfolders, failed)

if __name__ == '__main__':
    """
    """
    psr = argparse.ArgumentParser()
    psr.add_argument('csv')
    psr.add_argument('-o', '--outdir', default=os.getcwd())
    psr.add_argument('--ipfs', action='store_true', help = 'download files from ipfs. NOT functional at the moment')
    psr.add_argument('--genbank', action='store_true', default=True, help='download files from genbank')
    psr.add_argument('--protein', action='store_true', help='also download protein files')
    psr.add_argument('--rna', action='store_true', help='also download rna_from_genomic files')
    psr.add_argument('--quiet', action='store_true', help='suppress stdout printing')
    psr.add_argument('--subfolders', action='store_true', help='download genomic, rna, protein files to individual subfolders')
    args = psr.parse_args()
    download_genomes(args.csv, args.outdir, args.ipfs, args.genbank, args.protein, args.rna, args.quiet, args.subfolders)
