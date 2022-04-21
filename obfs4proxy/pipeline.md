client
======

```
[UDP] -> [TCP] -> [TCP]
```

## source: openvpn (udp)

```
#!/bin/sh
set -x
sudo openvpn \
    --verb 3 \
    --tls-cipher DHE-RSA-AES128-SHA \
    --cipher AES-128-CBC \
    --dev tun --client --tls-client \
    --remote-cert-tls server --tls-version-min 1.2 \
    --ca /tmp/ca.crt --cert /tmp/cert.pem --key /tmp/cert.pem \
    --proto udp4 \
    --pull-filter ignore ifconfig-ipv6 \
    --pull-filter ignore route-ipv6 \
    --remote 127.0.0.1 4430 \
    --route $OBFS4_ENDPOINT 255.255.255.255 net_gateway
```

## udp2tcp

using [vpnproxy](https://github.com/ainghazal/vpnproxy)

```
[UDP] -> [TCP]
./udp-proxy-client --source 127.0.0.1:4430 --target 127.0.0.1:1443
```

## shapeshifter dispatcher (transparent proxy)

* want to get rid of this piece.

```
[TCP] -> [TCP]

#!/bin/sh
REMOTE=$OBFS4_ENDPOINT:443

set -x
shapeshifter-dispatcher \
    -transparent -client \
    -state bridge -target $REMOTE \
    -transports obfs4 -proxylistenaddr 127.0.0.1:1443 \
    -optionsFile bridge/obfs4.json -logLevel DEBUG -enableLogging
```

server
======

```
[TCP] -> [TCP] -> [UDP]
obfs4 proxy (tcp) -> local (tcp) -> VPN gateway (udp)
```

## source: obfsproxy (obfs4 PT, ORPORT as sink)

```
[TCP] -> [TCP]
./obfsproxy -addr ${LHOST} -vpn ${RHOST} -state test_data -c test_data/obfs4.json
```

## tcp2udp

* using [vpnproxy](https://github.com/ainghazal/vpnproxy)
* want to get rid of this piece.

```
[TCP] -> [UDP]
./udp-proxy-server --source 10.0.0.209:4431 --target 212.129.62.247:443  # VPN GATEWAY SINK (UDP)
```

