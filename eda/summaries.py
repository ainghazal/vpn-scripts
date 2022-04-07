#!/usr/bin/env python3

import glob
import json
import sys

BASE = "base"
VANILLA = "vanilla"
VANILLA_UDP = "vanilla-udp"
OBFS4 = "obfs4"
TYPES = (BASE, VANILLA, VANILLA_UDP, OBFS4)
HEADER = '''down_mbit_s,up_mbit_s,down_retrasn_mb_s,min_rtt_ms'''

def parseDataFiles(exp_type):
    if exp_type not in TYPES:
        raise TypeError("unknown experiment type")

    print(HEADER)
    files = glob.glob(f"data/{exp_type}/*/*")
    for f in files:
        with open(f, 'r') as filep:
            try:
                measurements = [json.loads(jline) for jline in filep.readlines()]
                s = measurements[-1]
                down = s['Download']['Value']
                up = s['Upload']['Value']
                down_retrans = s['DownloadRetrans']['Value']
                rtt = s['MinRTT']['Value']
                print(f"{exp_type},{down},{up},{down_retrans},{rtt}")
            except KeyError:
                continue


if __name__ == "__main__":
    parseDataFiles(BASE)
    parseDataFiles(VANILLA)
    parseDataFiles(VANILLA_UDP)
    parseDataFiles(OBFS4)
