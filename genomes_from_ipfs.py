import pandas as pd
import os
import argparse
import ipfsapi
import requests
import shutil



#def download_genbank(genome_path, outF):
#    genbank_url = 'https://ftp.ncbi.nih.gov/genomes'
#    url = os.path.join(genbank_url,genome_path)
#    print(url)
#    with requests.get(url, stream=True) as r:
#        with open(outF, 'wb') as f:
#            shutil.copyfileobj(r.raw, f)

def download_ipfs(genome_path, outF, ipfs_api, failed):
    ipfs_url = "/ipfs/zDMZof1m4BD9VvDjPqguMrAoiY2gspmSAyyNLNYxNxRntLdXK3wj"
    url = os.path.join(ipfs_url, genome_path)
    print(url)
    with open(outF, 'wb') as f:
        try:
            f.write(ipfs_api.cat(url))
        except:
            failed.write(url + '\n')
            pass


def download_genomes(csv, outdir, ipfs=False, genbank=False):
    genomeInfo = pd.read_csv(csv)
    csv_name = args.csv.split('.')[0]#assuming good csv naming
    outD = os.path.join(outdir,csv_name)
    failedF = os.path.join(outD, 'failed.txt')
    os.makedirs(outD, exist_ok=True)
    genomes = genomeInfo.iloc[:,2]
    #if ipfs:
    api = ipfsapi.connect()
    with open (failedF, 'w') as failed:
        for g in genomes:
            out_name = g.split('/')[-1]
            out = os.path.join(outD, out_name)
            #if ipfs:
            download_ipfs(g, out, api, failed)
#           elif genbank:
#           download_genbank(g, out)

if __name__ == '__main__':
    """
    """
    psr = argparse.ArgumentParser()
    psr.add_argument('--csv')
    psr.add_argument('-o', '--outdir', default=os.getcwd())
    psr.add_argument('--ipfs', action='store_true')
    psr.add_argument('--genbank', action='store_true')
    args = psr.parse_args()
    download_genomes(args.csv, args.outdir, args.ipfs, args.genbank)
