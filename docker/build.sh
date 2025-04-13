#!/bin/sh

rm -rf stock
rsync -av --progress ../../stock . --exclude .git --exclude .idea --exclude *.md --exclude *.bat --exclude __pycache__ --exclude .gitignore --exclude stock/cron --exclude stock/img --exclude stock/docker --exclude instock/cache --exclude instock/log --exclude instock/test
rm -rf cron
cp -r ../../stock/cron .
rm ta-lib-0.6.4-src.tar.gz
wget https://github.com/TA-Lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz

DOCKER_NAME=atompi/stock
TAG=latest

echo " docker build -f Dockerfile -t ${DOCKER_NAME}:${TAG} ."
docker build -f Dockerfile -t ${DOCKER_NAME}:${TAG} .
echo "#################################################################"
echo " docker push ${DOCKER_NAME}:${TAG} "

#docker push ${DOCKER_NAME}:${TAG}
