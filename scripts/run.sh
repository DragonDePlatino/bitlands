#!/usr/bin/env bash

if [[ ! -d objects ]]; then
    echo "Objects folder missing..."
    exit -1
fi

./creature_graphics.py
./creature_raws.py
./grass_raws.py
./overrides.py
./plant_raws.py
./stone_raws.py
