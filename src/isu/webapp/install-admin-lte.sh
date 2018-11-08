#!/bin/bash
echo To install AdminLTE we need nasm package
rm -rf package*.json admin-lte node_modules
npm install --save admin-lte
#cd node_modules/admin-lte
#npm install --save
set -e
#pushd node_modules
#shopt -s extglob
#shopt -s dotglob
#echo rm -rf ./!(admin-lte)
mv node_modules/admin-lte ./
rm -rf node_modules
rm -rf admin-lte/build
#popd
