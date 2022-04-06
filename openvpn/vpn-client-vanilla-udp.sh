#!/bin/sh
set -x
sudo openvpn \
    --verb 3 \
    --tls-cipher DHE-RSA-AES128-SHA \
    --cipher AES-128-CBC \
    --dev tun --client --tls-client \
    --remote-cert-tls server --tls-version-min 1.2 \
    --ca /tmp/ca.crt --cert /tmp/cert.pem --key /tmp/cert.pem \
    --pull-filter ignore ifconfig-ipv6 \
    --pull-filter ignore route-ipv6 \
    --proto udp4 \
    --remote $GW 443 udp4
