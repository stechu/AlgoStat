import tps
import time
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, help="directory of a node")
parser.add_argument("-v", "--silence", action="count", default=0)
parser.add_argument("-n", "--number", type=int, help="number of rounds", default=100)
parser.add_argument("-p", "--period", type=int, help="time between each report (sec)", default=600)

def main():
    args = parser.parse_args()
    data_folder = Path(args.dir)
    net_file = data_folder / "algod.net"
    token_file = data_folder / "algod.token"
    with open(net_file) as f:
        url = f.readline()
    
    with open(token_file) as f:
        token = f.readline()

    for i in range(1000): # essentially forever
        time.sleep(args.period)
        tps.tps(args.number, url, token)
        print("--------------------------------")
    
    return

if __name__ == "__main__":
    main()