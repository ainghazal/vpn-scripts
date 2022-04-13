#!/usr/bin/env python3

import glob
import json
import sys

from types import SimpleNamespace

BASE = "base"
VANILLA = "vanilla"
VANILLA_UDP = "vanilla-udp"
OBFS4 = "obfs4"
TYPES = (BASE, VANILLA, VANILLA_UDP, OBFS4)
DOWNLOAD = "download"

HEADER = "exp,time,bw,speed,delivery_rate,pacing_rate"

bps = lambda x: x * 8 / 1e6

def parseDataFiles(exp_type, direction):
    if exp_type not in TYPES:
        raise TypeError("unknown experiment type")
    files = glob.glob(f"data/{exp_type}/*/*")
    for f in files:
        with open(f, 'r') as filep:
            mm = [json.loads(jline, object_hook=lambda d:SimpleNamespace(**d)) for jline in filep.readlines()]
            for m in mm:
                if hasattr(m, "Key") and m.Key == "measurement":
                    test = m.Value.Test
                    if test == direction:
                        v = m.Value
                        try:
                            tcp = v.TCPInfo
                            bbr = v.BBRInfo
                            #print(tcp)
                            #print(bbr)
                            bw = bps(bbr.BW)
                            et = float(tcp.ElapsedTime) / 1e06
                            bytes_acked = bps(tcp.BytesAcked)
                            speed = bytes_acked / et
                            delivery_rate = bps(tcp.DeliveryRate)
                            pacing_rate = bps(tcp.PacingRate)
                            print(f"{exp_type},{et},{bw},{speed},{delivery_rate},{pacing_rate}")
                        except AttributeError:
                            pass


if __name__ == "__main__":
   print(HEADER)
   d = DOWNLOAD
   parseDataFiles(BASE, d)
   parseDataFiles(VANILLA, d)
   parseDataFiles(VANILLA_UDP, d)
   parseDataFiles(OBFS4, d)
