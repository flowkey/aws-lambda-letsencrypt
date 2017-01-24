#!/bin/bash

BUILD_DIR=$HOME/build
OUTFILE=${BUILD_DIR}/package.zip
REMOTE_URL=https://github.com/kento1218/aws-lambda-letsencrypt.git

sudo yum -y groupinstall 'Development Tools'
sudo yum -y install libffi-devel openssl-devel

[ -d ${BUILD_DIR} ] || mkdir ${BUILD_DIR}
cd ${BUILD_DIR}

[ -d src ] || git clone ${REMOTE_URL} src

[ -f bin/activate ] || virtualenv .
source bin/activate

pip install certbot

pushd src && python certbot_s3website/setup.py develop && popd

rm -f ${OUTFILE}
pushd src && zip -r9 ${OUTFILE} * && popd
pushd $VIRTUAL_ENV/lib/python2.7/site-packages && zip -r9 ${OUTFILE} * && popd
pushd $VIRTUAL_ENV/lib64/python2.7/site-packages && zip -r9 ${OUTFILE} * && popd

GIT_VER=$(cd src && git describe --always)
DATE=$(date '+%Y%m%d%H%M%S')

aws s3 cp ${OUTFILE} s3://${BUCKET_NAME}/aws-lambda-letsencrypt-${GIT_VER}-${DATE}.zip
