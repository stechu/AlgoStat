from typing import Dict

import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="url of the node. e.g. ,.algod.net")
parser.add_argument("token", type=str, help="API token.  e.g. ./algod.token")
parser.add_argument("-v", "--silence", action="count", default=0)

def get_block(n: int, node_info: Dict[str, str]):
    if not args.silence:
        print("getting block {}.".format(n))
    url = 'http://{}/v1/block/{}'.format(node_info["url"], n)
    headers = {"X-Algo-API-Token": node_info["token"]}
    r = requests.get(url, headers=headers)
     
    if r.status_code != 200:
        print("ERROR: status code: {}".format(r.status_code))
        return (0, False, 0)

    bj = r.json()  
    if 'transactions' in bj["txns"]:
        return (len(bj["txns"]["transactions"]), True, bj["timestamp"])
    else:
        return (0, True, bj["timestamp"])

def get_lastround(node_info: Dict[str, str]):
    url = 'http://{}/v1/status'.format(node_info["url"])
    headers = {"X-Algo-API-Token": node_info["token"]}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("ERROR: status code: {}".format(r.status_code))
        return 0

    j = r.json()
    return j['lastRound']

def tps():
    node_info = {"url": args.url, "token": args.token}
    last_round = get_lastround(node_info)
    first_round = last_round - 999 if last_round >=1000 else 0
    data = []
    for i in range(first_round, last_round + 1):
        (nt, success, time) = get_block(i, node_info) 
        if not success:
            print("ERROR in round {}".format(i))
        data.append((nt, time))
    total_txn = sum([x for (x, y) in data])
    total_time = data[-1][1] - data[0][1] 
    num_round = last_round - first_round + 1
    print("txn stats (round {} - {})".format(first_round, last_round))
    print("number of non-empty block: {}".format(len(list(filter(lambda x: x[0] > 0, data)))))
    print("avg. txn per block: {}".format(
        total_txn/num_round))
    print("avg. time per block: {}".format(total_time/(num_round -1)))
    print("txn per second: {}".format(total_txn/total_time))

args = parser.parse_args()
tps()