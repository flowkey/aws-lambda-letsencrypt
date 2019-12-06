#!/bin/bash

OUTFILE=package.zip
VENV=package

cd $(dirname $0)

OUTABS=$(cd $(dirname ${OUTFILE}) && pwd)/$(basename ${OUTFILE})

[ -f ${VENV}/bin/activate ] || python3 -m venv ${VENV}
source ${VENV}/bin/activate

pip3 install -r requirements.txt

rm -f ${OUTABS}
zip -9 ${OUTABS} $(git ls-files | grep -F .py)
pushd ${VENV}/lib/python3.7/site-packages && zip -r9 ${OUTABS} * && popd
pushd ${VENV}/lib64/python3.7/site-packages && zip -r9 ${OUTABS} * && popd

# workaround for libffi
pushd ${VENV}/lib/python3.7/site-packages/.libs_cffi_backend && zip -r9 ${OUTABS} * && popd
pushd ${VENV}/lib64/python3.7/site-packages/.libs_cffi_backend && zip -r9 ${OUTABS} * && popd
