#!/bin/bash

source versions.sh

template_dir=template
cp -p ${template_dir}/README.md .

pushd template
	files=$(find . -type f | xargs grep -l '$POSTGRES_VERSION')
popd

for version in ${versions}
do
	echo "Copy files into ${version}"
	cp -rp ${template_dir}/* ${version}

	echo "Expanding ${version}"
	for file in ${files}
	do
		source=${template_dir}/${file}
		target=${version}/${file}
		echo "Expanding ${source} to ${target}"
		export POSTGRES_VERSION=${version}
        envsubst < ${source} > ${target}
	done
done
