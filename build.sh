#!/bin/bash

source versions.sh
./update.sh

for version in ${versions}
do
	pushd ${version}
		echo "Building for PG version: ${version}"
		./build.sh
	popd
done
