#!/bin/bash

source build.properties

echo Building flight-computer [$version]...
rm -rf build > /dev/null
mkdir -p build/work

cp -R src/* build/work
cp -R resources build/work

tar -czf build/flight-computer-$version.tar.gz -C build/work .  

echo Build complete.
