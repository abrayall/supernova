#!/bin/bash
source build.properties

echo Installing flight-computer [$version]...
./build.sh

mkdir -p /opt/supernova/flight-computer
rm -rf /opt/supernova/flight-computer/*

tar -xzf build/flight-computer-$version.tar.gz -C /opt/supernova/flight-computer/

/opt/supernova/flight-computer/resources/service/install.sh

echo Installing flight-computer complete.
