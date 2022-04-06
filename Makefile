RHOST?=
NDT_SERVER?=
TYPE?=base
TIME=$(shell date +'%Y-%j-%T%z')
PATH=data/${TYPE}/${TIME}
NDT7=$(shell which nd7-client)

perf:
	/usr/bin/mkdir -p "${PATH}"
	${NDT7} -server ${NDT_SERVER}:4443 -no-verify -format=json | /usr/bin/tee ${PATH}/result.json

certs:
	curl -k https://black.riseup.net/ca.crt > /dev/shm/ca.crt
	curl -k https://api.black.riseup.net/3/cert > /dev/shm/cert.pem

connect-obfs4:
	./obfs4/vpn-client-obfs4.sh

connect-vanilla-tcp:
	./openvpn/vpn-client-vanilla-tcp.sh

connect-vanilla-tcp:
	./openvpn/vpn-client-vanilla-udp.sh

check:
	curl https://wtfismyip.com/json
