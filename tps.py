from typing import Dict

import json
import requests
import time

def get_block(n: int, node_info: Dict[str, str], verbose):
    if verbose == 1:
        print("getting block {}.".format(n))
    url = 'http://{}/v1/block/{}'.format(node_info["url"], n)
    headers = {"X-Algo-API-Token": node_info["token"]}
    r = requests.get(url, headers=headers)
     
    if r.status_code != 200:
        print("ERROR: status code: {}".format(r.status_code))
        return (0, False)

    bj = r.json()  
    if 'transactions' in bj["txns"]:
        return (len(bj["txns"]["transactions"]), True)
    else:
        return (0, True)

def get_lastround(node_info: Dict[str, str]):
    url = 'http://{}/v1/status'.format(node_info["url"])
    headers = {"X-Algo-API-Token": node_info["token"]}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("ERROR: status code: {}".format(r.status_code))
        return 0

    j = r.json()
    return j['lastRound']

def tps(max_round, url, token, silence):
    node_info = {"url": url, "token": token}
    last_round = 0
    first_round = 0
    data = []
    i = 0
    while i < max_round:
        current_round = get_lastround(node_info)
        if last_round == 0: 
            first_round = current_round
        if current_round == last_round :
           time.sleep(0.300)
        else: 
            (nt, success) = get_block(current_round, node_info, silence) 
            if not success:
                print("ERROR in round {}".format(i))
            btime = time.time()
            data.append((nt, btime))
            last_round = current_round
            i = i + 1
    
    total_txn = sum([x for (x, y) in data])
    total_time = data[-1][1] - data[0][1]
    num_round = last_round - first_round + 1
    avg_time = total_time/(num_round -1)
    print("txn stats (round {} - {})".format(first_round, last_round))
    print("number of non-empty block: {}".format(len(list(filter(lambda x: x[0] > 0, data)))))
    print("avg. txn per block: {}".format(
        total_txn/num_round))
    print("avg. time per block: {}".format(avg_time))
    print("txn per second: {}".format(total_txn/(total_time+avg_time)))