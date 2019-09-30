import tps
import time
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, help="directory of a node")
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("-n", "--number", type=int, help="number of rounds", default=100)
parser.add_argument("-p", "--period", type=int, help="time between each report (sec)", default=600)
parser.add_argument("-r", "--repeat", type=int, help="number of repeat.", default=1)

def main():
    args = parser.parse_args()
    data_folder = Path(args.dir)
    net_file = data_folder / "algod.net"
    token_file = data_folder / "algod.token"
    with open(net_file) as f:
        url = f.readline()
    
    with open(token_file) as f:
        token = f.readline()

    for _ in range(args.repeat):
        if args.repeat != 1:
            time.sleep(args.period)
        tps.tps(args.number, url, token, args.verbose)
        print("----------------------------------")
    
    return

if __name__ == "__main__":
    main()