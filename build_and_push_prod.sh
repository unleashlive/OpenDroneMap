#!/usr/bin/env bash
set -e
git pull
docker build -t odm:stable .
eval $(aws ecr get-login --no-include-email --region ap-southeast-2 | sed 's|https://||')
docker tag odm:stable 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/odm:stable
docker push 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/odm:stable
