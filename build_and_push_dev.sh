#!/usr/bin/env bash
set -e
docker build -t odm:latest .
eval $(aws ecr get-login --no-include-email --region ap-southeast-2 | sed 's|https://||')
docker tag odm:latest 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/odm:latest
docker push 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/odm:latest
