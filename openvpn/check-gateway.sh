#!/bin/bash

# these are gateways for riseupvpn
TCP_GW=10.41.0.1
UDP_GW=10.42.0.1

FIRSTHOP=$(traceroute -m 1 8.8.8.8 | awk -F"[()]" '{print $2}' | tail -n 1)
echo "first hop:" $FIRSTHOP
echo "experiment type:" $TYPE

# vanilla is vanilla-tcp
if [[ "$TYPE" == "vanilla" ]];
then
    if [ "$FIRSTHOP" == $TCP_GW ]
    then
        echo "ok"
        exit 0
    else
        echo "error!"
        exit 1
    fi;
fi;

# plain openvpn over udp
if [[ "$TYPE" == "vanilla-udp" ]];
then
    if [[ "$FIRSTHOP" == $UDP_GW ]]
    then
        echo "ok"
        exit 0
    else
        echo "error!"
        exit 1
    fi;
fi;

# obfs4 uses an openvpn/tcp tunnel over the tpc-based obfs4
if [[ "$TYPE" == "obfs4" ]];
then
    if [[ "$FIRSTHOP" == $TCP_GW ]]
    then
        echo "ok"
        exit 0
    else
        echo "error!"
        exit 1
    fi;
fi;

# base is the non-tunneled measurement
if [[ "$TYPE" == "base" ]];
then
    if [[ "$FIRSTHOP" == $TCP_GW ]]
    then
        echo "error!"
        exit 1
    fi;
    if [[ "$FIRSTHOP" == $UDP_GW ]]
    then
        echo "error!"
        exit 1
    fi;
fi;
