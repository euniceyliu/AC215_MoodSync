#!/bin/bash

echo "Container is running!!!"

args="$@"
echo $args

if [[ -z ${args} ]];
then
    pipenv run python llm_rag.py --load
else
  pipenv run python llm_rag.py --load
fi
