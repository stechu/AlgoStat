import tps
import time
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, help="directory of a node", required=True)
parser.add_argument("-n", "--number", type=int, help="number of rounds", default=100)


def main():
    args = parser.parse_args()
    data_folder = Path(args.dir)
    net_file = data_folder / "algod.net"
    token_file = data_folder / "algod.token"
    with open(net_file) as f:
        url = f.readline()
    
    with open(token_file) as f:
        token = f.readline()

    node_info = {"url": url, "token": token}
    print(tps.get_block(args.number, node_info, 0))
    return

if __name__ == "__main__":
    main()