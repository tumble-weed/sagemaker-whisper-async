
## To build an image and push it to ecr

```bash build_and_push.sh dummy-whisper-async true```

## To build an image locally

```bash build_and_push.sh dummy-whisper-async false```

## To build an image and deploy as sagemaker async endpoint

```bash build_push_deploy.sh```

This file includes options for selecting the instance type, currently it is set to __g4dn.2xlarge__
