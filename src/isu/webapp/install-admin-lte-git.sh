#!/bin/bash
echo To install AdminLTE we need nasm package
# FIXME: This is VERY stupid.
mkdir -p node_modules
git clone https://github.com/almasaeed2010/AdminLTE.git node_modules/admin-lte
cd node_modules/admin-lte
npm install --save 
