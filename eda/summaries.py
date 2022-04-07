#!/usr/bin/env python3

import glob
import json
import sys

BASE = "base"
VANILLA = "vanilla"
VANILLA_UDP = "vanilla-udp"
OBFS4 = "obfs4"
TYPES = (BASE, VANILLA, VANILLA_UDP, OBFS4)

#HEADER = '''exp,down_mbit_s,up_mbit_s,down_retrasn_mb_s,min_rtt_ms'''
HEADER = '''exp,down,up,retr,minrtt'''

def parseDataFiles(exp_type):
    if exp_type not in TYPES:
        raise TypeError("unknown experiment type")
    files = glob.glob(f"data/{exp_type}/*/*")
    for f in files:
        with open(f, 'r') as filep:
            try:
                m = [json.loads(jline) for jline in filep.readlines()]
                s = m[-1]
                down = s['Download']['Value']
                up = s['Upload']['Value']
                retr = s['DownloadRetrans']['Value']
                minrtt = s['MinRTT']['Value']
                print(f"{exp_type},{down},{up},{retr},{minrtt}")
            except KeyError:
                continue


if __name__ == "__main__":
    print(HEADER)
    parseDataFiles(BASE)
    parseDataFiles(VANILLA)
    parseDataFiles(VANILLA_UDP)
    parseDataFiles(OBFS4)
