## Overview of DVC in the repo
### **Implementing DVC for the first time (if not implemented yet)**

1. Configure GCP service accounts on https://console.cloud.google.com/storage/browser and add secrets to your local folder.
2. Create folders inside google cloud buckets: ```dvc_store``` and any folders to contain data you wish to track
3. Change docker-entrypoint.sh and docker-shell.sh accordingly to reflect the folders and buckets.
4. Make sure the github repository has .git files in it, indicating it to be a git repo.
5. Make sure you have dvc and dvc_gs installed in your local environment (pip install dvc dvc_gs)
6. Run the container (sh docker-shell.sh)
7. Inside the container:
	  ```
	  #initialize dvc
	  dvc init
	  #add remote registry to GCS bucket
	  dvc remote add -d {folder_name} gs://{your-bucket-name}/dvc_store
	  #add the dataset to registry 
	  dvc add {folder_name}
	  #push to remote registry
	  dvc push
	  ```
8. Exit out of the container, then:
	```
	git status
	git add .
	git commit -m ‘some message…’
	git tag -a ‘{versionTag}’ -m ‘tag dataset’
	git push —atomic origin {gitBranch, e.g.HEAD:main} {versionTag}
	```

### **Updating DVC (if already implemented)**
1. Run the container (sh docker-shell.sh)
2. Inside the container:
	```
	#add the dataset to registry
	dvc add {folder_name}
	#push to remote registry
	Dvc push 
	```
3. Exit out of the container, the:
	```
	git status
	git add .
	git commit -m ‘some message…’
	git tag -a ‘{versionTag}’ -m ‘tag dataset’
	git push —atomic origin {gitBranch, e.g.HEAD:main} {versionTag}
	```
4. Lastly use goole colab to view the content of each version:
```
  import os
  import cv2
  import numpy as np
  import pandas as pd
  
  # Colab auth
  from google.colab import auth
  from google.cloud import storage
  
  # This step is required for DVC in colab to access your Bucket
  auth.authenticate_user()
  
  pat = {your_github_token}
  !dvc list -R https://{pat}@github.com/Singyuna/AC215_MoodSync
  !rm -rf {folder_name}
  !dvc get https://{pat}@github.com/singyuna/AC215_MoodSync {folder_name} --force --rev {versionTag}
  print("Number of items:”,len(os.listdir(“{folder_name}”)))
```
