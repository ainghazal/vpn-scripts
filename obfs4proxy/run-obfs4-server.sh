#!/bin/sh
GW=212.129.62.247 # paris
BIND_ADDR=1.1.1.1 # set to your proxy public ip
BIND_PORT=3000
sudo -u obfs4-ovpn -g obfs4-ovpn /usr/bin/env \
        TOR_PT_MANAGED_TRANSPORT_VER=1 \
        TOR_PT_STATE_LOCATION=/var/lib/obfs4proxy-openvpn/obfs4/ \
        TOR_PT_SERVER_TRANSPORTS=obfs4 \
        TOR_PT_SERVER_BINDADDR=obfs4-$BIND_ADDR:$BIND_PORT \
        TOR_PT_ORPORT=$GW:443 \
        /usr/bin/obfs4proxy \
        -enableLogging -logLevel ERROR
