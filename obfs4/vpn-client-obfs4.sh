#!/bin/sh
set -x

sudo openvpn \
    --verb 3 \
    --tls-cipher DHE-RSA-AES128-SHA \
    --cipher AES-128-CBC \
    --dev tun --client --tls-client \
    --remote-cert-tls server --tls-version-min 1.2 \
    --ca /dev/shm/ca.crt --cert /dev/shm/cert.pem --key /dev/shm/cert.pem \
    --proto tcp4 \
    --pull-filter ignore ifconfig-ipv6 \
    --pull-filter ignore route-ipv6 \
    --remote 127.0.0.1 1443 tcp4 \
    --route $REMOTE 255.255.255.255 net_gateway
