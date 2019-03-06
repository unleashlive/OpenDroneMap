#!/usr/bin/env bash
set -e
eval $(aws ecr get-login --no-include-email --region ap-southeast-2 | sed 's|https://||')
docker build --no-cache -t odm .
docker tag odm:latest 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/imhotep:odm
docker push 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/imhotep:odm
