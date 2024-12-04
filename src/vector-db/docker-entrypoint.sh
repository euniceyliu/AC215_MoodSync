#!/bin/bash

echo "Container is running!!!"

args="$@"
echo $args

if [[ -z ${args} ]];
then
    pipenv shell
else
  pipenv run python llm_rag.py --load
fi
