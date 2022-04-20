#!/bin/sh
# Script to launch obfs4proxy to listen on a local socks5 proxy.
# Your openvpn client needs to add:

# --socks-proxy localhost $SOCKS5_PORT socks5_auth_file

# where the socks5 auth file has been written by obfs4proxy
# the port you have to parse from the obfs4proxy logs

echo "[+] Remember to set CLIENT_REMOTE_CERT!"
sudo -u obfs4-ovpn -g obfs4-ovpn /usr/bin/env \
    TOR_PT_MANAGED_TRANSPORT_VER=1 \
    TOR_PT_STATE_LOCATION=/var/lib/obfs4proxy-openvpn/obfs4/ \
    TOR_PT_CLIENT_TRANSPORTS=obfs4 \
    CLIENT_OBFS4_SOCKS5_PORT=3000 \
    /usr/bin/obfs4proxy \
    -enableLogging -logLevel ERROR

