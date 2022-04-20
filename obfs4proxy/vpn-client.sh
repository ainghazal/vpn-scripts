#!/bin/sh
set -x
GW=212.129.62.247 # paris
PROXY=1.1.1.1     # setup to your obfs4 remote proxy
LOCAL=127.0.0.1
OBFS4_PORT=3000
sudo openvpn \
    --verb 4 \
    --tls-cipher DHE-RSA-AES128-SHA \
    --cipher AES-128-CBC \
    --dev tun --client --tls-client \
    --remote-cert-tls server --tls-version-min 1.2 \
    --ca /dev/shm/ca.crt --cert /dev/shm/cert.pem --key /dev/shm/cert.pem \
    --pull-filter ignore ifconfig-ipv6 \
    --pull-filter ignore route-ipv6 \
    --remote $PROXY $OBFS4_PORT \
    --socks-proxy $LOCAL $SOCKS5_PORT /var/lib/obfs4proxy-openvpn/socks5_auth \
    --proto tcp \
    --route $PROXY 255.255.255.255 net_gateway \
    --auth-nocache
