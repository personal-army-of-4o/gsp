#!/bin/bash


nt="0"
ct="0"
if [ "$1" == "nmigen" ]; then
    nt="1"
fi
if [ "$1" == "cocotb" ]; then
    ct="1"
fi
if [ "$1" == "" ]; then
    nt="1"
    ct="1"
fi

if [ "$nt"  == "1" ]; then
    python3 tb.py
    if [ "$?" != "0" ]; then
        echo "nmigen test failed"
        exit 1
    fi
fi

if [ "$ct"  == "1" ]; then
    export PYTHONPATH=$PYTHONPATH:`pwd`
    cd cocotb_sim
    make
    if [ "$?" != "0" ]; then
        echo "cocotb test failed"
        exit 1
    fi
fi
