import json
import argparse
import pandas as pd
import upload
import processing

def run_Network(mode):
    processing.main(mode)
    upload.main(mode)

def run_FQDN(mode):
    processing.main(mode)
    upload.main(mode)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload')
    parser.add_argument('-m','--mode', type=str, default='NetWork', choices=['NetWork', 'FQDN'], help='The mode to run: NetWork or FQDN.')
    args = parser.parse_args()

    if args.mode == 'NetWork':
        run_Network(args.mode)
    elif args.mode == 'FQDN':
        run_FQDN(args.mode)
