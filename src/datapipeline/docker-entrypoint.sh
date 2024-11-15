#!/bin/bash

echo "Container is running!!!"

args="$@"
echo $args

gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS_data
mkdir -p /mnt/gcs_bucket
gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS_data $GCS_BUCKET_NAME /mnt/gcs_data
echo 'GCS bucket mounted at /mnt/gcs_data'
rm -r /app/output
mkdir /app/output
#mount --bind /mnt/gcs_data/output /app/output
#gsutil ls gs://rag_data_song/  #this works BUT mount --bind doesn't with gcs FOR WHAETEVER REASON, let's work around it then
gsutil -m cp gs://rag_data_song/output/* /app/output/


if [[ -z ${args} ]]; 
then
    pipenv shell
else
  pipenv run python $args
fi