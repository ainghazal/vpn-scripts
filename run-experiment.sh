#!/bin/bash

measure_run() {
    for i in {1..10}
    do 
        echo "run: $TYPE-$i"
        make perf
        sleep 30
    done
}

measure_run
