#!/bin/bash

echo "Container is running!!!"

args="$@"
echo $args

gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS_data
mkdir -p /mnt/gcs_bucket
gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS_data $GCS_BUCKET_NAME /mnt/gcs_data
echo 'GCS bucket mounted at /mnt/gcs_data'
mkdir -p /app/output
mount --bind /mnt/gcs_data/output /app/output


if [[ -z ${args} ]]; 
then
    pipenv shell
else
  pipenv run python $args
fi