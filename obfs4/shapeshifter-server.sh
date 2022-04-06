#!/bin/sh
set -x
../../shapeshifter-dispatcher/shapeshifter-dispatcher \
    -transparent -server -state bridge \
    -orport $GW:443 \
    -transports obfs4 -bindaddr obfs4-127.0.0.1:1194 \
    -logLevel DEBUG -enableLogging

