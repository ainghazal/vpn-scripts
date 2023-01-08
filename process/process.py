"""
Process RAW OONI data (from a report.jsonl file).
Perform basic series manipulation, and write some intermediary representations on disk.

"""
import glob
import json
import os
import sys

from datetime import datetime

from dateutil import relativedelta

import pandas as pd
import numpy as np
import feather

FEATHER_DATA_BASE = "ftr"

# feather RAW files are a first feather representation of the series contained
# in the concatenation of several reports. Raw files are appended when new
# source files (in json format) are found.
FEATHER_RAW = os.path.join(FEATHER_DATA_BASE, "raw")

# feather CUR are curated files. the idea is that these files contain less
# fields, and are flatenned to easy data analysis. Currently we will be changing the data
# included in this.
# This format is a good summary to share and publish (more portable and more compact).
FEATHER_CUR = os.path.join(FEATHER_DATA_BASE, "cur")

OONIDATA_DEFAULT = "/var/log/oonidata"
OONIDATA = os.getenv('OONIDATA', OONIDATA_DEFAULT)

def parseJSONReport(location, skip_old=True):
    """
    Parse loads OONI report files (report.jsonl) from a given location folder.
    If no feather file exist, it will create one.
    If the first timestamp in a new measurement file is older than the last timestamp in the feather file,
    it will be skipped.
    """
    ff = getRawFeatherFile(location)
    last_feather_ts = None
    if os.path.isfile(ff):
        fs = readSummarySeries(ff)
        last_feather_ts = getLastTimestamp(fs)

    allJsonFiles = glob.glob(f"/{OONIDATA}/{location}/*.jsonl")
    allJsonFiles.sort()
    dfs = []

    for i in allJsonFiles:
        # TODO skip all, in an smarter way (check TS from file perhaps)
        # TODO can also check first and last in series (if we do month)
        msm = loadJsonFile(i)
        # TODO a better thing, if we have more measurements, would be to filter
        # out all the ts in this dataframe that are older than our last known ts
        # we'll be missing only a few msm, so not urgent for now.
        msm_ts = getFirstTimestampInMeasurement(msm)

        if last_feather_ts is None or not skip_old:
            print("appending:", i)
            dfs.append(msm)

        elif skip_old and msm_ts > last_feather_ts:
            print("appending:", i)
            dfs.append(msm)

    if len(dfs) == 0:
        return

    df = pd.concat(dfs)
    df.reset_index()

    if last_feather_ts is not None:
        orig_f = loadRawFeatherFileForLocation(location)
        merged = pd.concat([orig_f, df])
        merged.reset_index()
        merged.reset_index(drop=False).to_feather(ff)
    else:
        df.reset_index(drop=False).to_feather(ff)


def loadJsonFile(jf):
    return pd.read_json(jf, lines=True)

def loadFeatherFile(ff):
    return pd.read_feather(ff, columns=None, use_threads=True);

def loadRawFeatherFileForLocation(location):
    ff = getRawFeatherFile(location)
    return pd.read_feather(ff, columns=None, use_threads=True);

def getRawFeatherFile(location):
    return os.path.join(FEATHER_RAW, location + '.ftr')

def getFirstTimestampInMeasurement(msm):
    """
    msm is a pandas dateframe from a single measurement json
    """
    first = msm['test_start_time'][0]
    return first.to_pydatetime()


def getLastTimestamp(ts):
    return max(ts.index).to_pydatetime()

def readSummarySeries(ffile):
    rf = pd.read_feather(ffile, columns=None, use_threads=True);
    ts = rf.test_start_time
    tk = rf.test_keys

    provider = [x['provider'] for x in tk]
    remote = [x['remote'] for x in tk]
    vpn_proto = [x['vpn_protocol'] for x in tk]
    transport = [x['transport'] for x in tk]
    obfuscation = [x['obfuscation'] for x in tk]

    remote_pairs =  [x.split(':') for x in [x['remote' ] for x in tk]]
    ipaddr, port = zip(*remote_pairs)

    icmp1_min_rtt = [x['icmp_pings'][0]['min_rtt'] if x['icmp_pings'] is not None and len(x['icmp_pings']) != 0 else np.nan for x in tk]
    icmp1_rcv = [x['icmp_pings'][0]['pkt_rcv'] if x['icmp_pings'] is not None and len(x['icmp_pings']) != 0 else np.nan for x in tk]
    icmp1_snt = [x['icmp_pings'][0]['pkt_snt'] if x['icmp_pings'] is not None and len(x['icmp_pings']) != 0 else np.nan for x in tk]

    success = [x['success'] for x in tk]
    success_handshake = [x['success_handshake'] for x in tk]
    success_icmp = [x['success_icmp'] for x in tk]
    success_urlgrab = [x['success_urlgrab'] for x in tk]

    failures = [x['failure'] for x in tk]
    stage = [x['last_handshake_transaction_id'] for x in tk]
    bstr_t = [x['bootstrap_time'] for x in tk]

    dfc = pd.DataFrame({
        'ts': rf.measurement_start_time,
        'report_id': rf.report_id,
        'test_name': rf.test_name,
        'test_ver': rf.test_version,
        'obfuscation': obfuscation,
        'provider': provider,
        'remote': remote,
        'ipaddr': ipaddr,
        'port': port,
        'vpn_proto': vpn_proto,
        'transport': transport,
        'probe_asn': rf.probe_asn,
        'probe_cc': rf.probe_cc,
        'probe_network': rf.probe_network_name,
        'icmp1_min_rtt': icmp1_min_rtt,
        'icmp1_rcv': icmp1_rcv,
        'icmp1_snt': icmp1_snt,
        'ok': success,
        'ok_hnd': success_handshake,
        'ok_icmp': success_icmp,
        'ok_url': success_urlgrab,
        'btime': bstr_t,
        'runtime': rf.test_runtime,
        'stage': stage
        },
        columns=[
            'ts', 'report_id',
            'test_name', 'test_ver',
            'vpn_proto', 'transport', 'obfuscation',
            'provider', 'remote', 'ipaddr', 'port',
            'probe_asn', 'probe_cc', 'probe_network',
            'icmp1_min_rtt', 'icmp1_rcv', 'icmp1_snt',
            'ok', 'ok_hnd', 'ok_icmp', 'ok_url',
            'btime', 'runtime',
            'stage'
        ]
    )
    dfc["ts"] = dfc["ts"].astype("datetime64")
    # TODO: probably need to construct one random id for missing 
    # dfc = dfc.set_index("report_id")
    return dfc

def dumpMonthySummary(location, df):
    for monthTS in monthsInRange(df):
        year, month = monthTS.split('-')
        dest = os.path.join(FEATHER_CUR, f'{location}-{monthTS}.ftr')
        filtered = filterByMonth(df, monthTS)
        filtered.reset_index().to_feather(dest)


# TODO user filter functions

def filterByDay(df, day):
    # f.query('"2023-01-07 00:00:00" <= test_start_time <  "2023-01-08 00:00:00"')
    pass

def filterByMonth(df, month_ts):
    fmt = '%Y-%m-%d %H:%M:%S'
    # TODO use strptime
    year, month = month_ts.split('-')
    _begin = f'{year}-{month}-01 00:00:00'
    begin = datetime.strptime(_begin, fmt)
    # add 1 month and set to the fist day of the month
    _end = begin + relativedelta.relativedelta(months=1, day=1)
    end = datetime.strftime(_end, fmt)
    return df.query(f'"{begin}" <= ts < "{end}"')


def monthsInRange(df):
    """
    Return a list of all months included in the range of a series.
    It will pick the "ts" column.
    Return a list in the format ["%Y-%m"]
    """
    min_ts = min(df.ts).to_pydatetime().strftime('%Y-%m')
    max_ts = max(df.ts).to_pydatetime().strftime('%Y-%m')
    return pd.date_range(min_ts, max_ts, freq="MS").strftime("%Y-%m").tolist()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: process <cmd> <args>")
        sys.exit(1)

    cmd = sys.argv[1]
    loc = sys.argv[2]

    if loc == "":
        print("pass valid location")
        sys.exit(1)


    if cmd == "raw":
        parseJSONReport(loc)
        sys.exit(0)

    elif cmd == "monthly":
        ss = readSummarySeries(getRawFeatherFile(loc))
        dumpMonthySummary(loc, ss)
        sys.exit(0)

    else:
        print("unknown command")
        sys.exit(1)





