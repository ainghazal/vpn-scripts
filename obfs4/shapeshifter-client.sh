#!/bin/sh
set -x
../../shapeshifter-dispatcher/shapeshifter-dispatcher \
    -transparent -client \
    -state bridge -target $REMOTE:443 \
    -transports obfs4 -proxylistenaddr 127.0.0.1:1443 \
    -optionsFile bridge/obfs4.json -logLevel DEBUG -enableLogging
