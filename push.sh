#!/usr/bin/env bash

# This script shows how to build the Docker image and push it to ECR to be ready for use
# by SageMaker.

# The argument to this script is the image name. This will be used as the image on the local
# machine and combined with the account and region to form the repository name for ECR.
image=$1

if [ "$image" == "" ]
then
    echo "Usage: $0 <image-name>"
    exit 1
fi

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi


# Get the region defined in the current configuration (default to us-west-2 if none defined)
region=$(aws configure get region)
region=${region:-us-west-2}


fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"
# echo "$fullname"
# exit
# If the repository doesn't exist in ECR, create it.

aws ecr describe-repositories --repository-names "${image}"
#========================================================================
# Get the login command from ECR and execute it directly
# $(aws ecr get-login --region ${region} --no-include-email)
#========================================================================
echo "$region"
echo "$account"
# $(aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com)
# $(aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 268945887964.dkr.ecr.ap-northeast-1.amazonaws.com)
# $(aws ecr get-login-password --region ap-northeast-1|docker login --username AWS --password-stdin 268945887964.dkr.ecr.ap-northeast-1.amazonaws.com)
docker login --username AWS --password eyJwYXlsb2FkIjoiNVlaZERNb1JCZXl3UnVUdEtBU3RxdE1zY3hmQjVINnV2QnREcjFHa1IyYXd5WlJMdUlVdnlPUm9jVmdIU2hMZkxqVzdhTVd6Z2FFWEh3c0VNT0dnaUdSN05aLzlCSjhrQk5nVkhLVGFTbUEyV2hybWpNa3kyUC9nNzYrVjRLcE5MTktXSFpiZUtiY29WNFhMejNha3JFRzFGei96cWtTSjUrc1dPZWFnR0RCTUNqR3dxeEJwcFVvOWNra0xLU0VML1pEaE9HekQwMXczeG5GcHQzSWhjbFE3WndhNkpsVWZzeU9wR1dQVVdRSjlQTFk1NkhZQXRPc2hGODNLbmsyeUs1V3lJQ1JwRG42aXA4dG12Rjc3bk9DL1o2cjVnS3VqMGI3MnpQRG9nUW5oMzBKSDVlSWxOaHdhVzNRRWpIUWp6d0wwb0M3cHJNZ1Z1aExEQzNPYlhNeEtudFFQYjJSMjVMdkJ1TVdyNm1FZVVYcmJjamU5Z1cxZytyTVM1bXlWZ1VGeEZ2dStmSmtKMEpSRUxaM1BLSG5TVkVTSm1zVm1ZSU5OVFlydkNpZWhqakxGNlFWUUpLVlJrbWV2RWkzUXBEN3ZoSzhVWnI5WkRqc2hNcktVM3lER2JkOVVKckxadlJuQWQyYzFLQkptRnJ6WUttREZXdWtwd3d0YWVwbHpJTGE1YzlyblFFb1VhSHd1YzBmZlo3RWd3ak5jMmh0S1cvZXoxSHNVYjNobWEyYWxPcGdLTlErY3BhMFp5U29IRllWbWJoRHh1MzhDbEJ4VzBic0VTOUdxNDJHWnB4Wmp1YTA3Lytqa2RSVkVVQ2kvZHgxR0xrVlBQb3g1ZkQ1VmUwdXpGcHlYeWVLY2RyWFdkMHFNZ1NZWlVDRmwyK0I2a01LSVBaOG14NGIyMlBna2dhYWdaMTBHeHpPODdzNXZQa2JaNFhPcXFIMWl1MmZMenZPQXNybFdoRy84YjZRQjRaY1RHbUlNTDdlYnBkZHRRWlV6SDl6WEd5VTd4U1ozSVMxZGR4VS9sYWN1WlAzWU0yT0s1SWhRdXhtVmZBem93bmZweDYrelBlTTErSXRhOTJHZ0VGUWdUc1QvOU91YzJWSjdSV1hick1QZXdPSGppS25RaGN2VnBlTXFXamY3VzRNN0FZaEl4SDhwR2VBZFRKVkRhWnRjZ2NxWHVhTGJuMVd2TEo5NmxWOGdLVkNmaGtpMCsyeUtxdjgrOCtFeWdRZ2plOXJNdFZqdDM5OW5PSUxGSW1MeDd4RlpVRE9QMjdacE5tVThUaTBRQmlYZkZDd0Y1aTE2NThvSWVxcFpiVTdwSkNrOUVyTitmd0djMEF0TTV1OVRTY2NsRzRJdkZudFVaRVhyNUF5aGtRSVo3MUN3M3Z5bjFHVy91bUxnRGllMDBMOG5xMnBJelhWempaWmJFaVBDQXdGcFFEM0lWSVZCaC82RENYMWNReVVVQ1R6OFE5VUxmalpmUTV5WTZ4R3dtRC94QmJkUkNqSjhYc1NYOU1uNlhxTks5aWJ5Zy9wc2I0dlpQUi9zb0MxeWwycXBTV2J0cng0UzVFZXVRd0k4YldGdGlrL0hjOTZ1K0E5RlpiOEJBbnBjVUNzSWVSNFJnN3gxWDlIcDlpUUZxdmdFeXIrYTFzb0pjdzZiNWtuRU9aUlkwbmlPMytpTG9oSVdWTWpicEIwbjl6ZHdPYzdtRThDTXIrd0FuUWV5YkNDYVAwSjFsY2lPWlU0aVZSUzJYYmo4TlVnUStoUmwwQUd4TEpWTWhDNE0iLCJkYXRha2V5IjoiQVFFQkFIZ0FNZktEbElvcEM2enMwYk1kUnJZU0hhL0MzOWtDcmNQOGtWcHJFOWYra1FBQUFINHdmQVlKS29aSWh2Y05BUWNHb0c4d2JRSUJBREJvQmdrcWhraUc5dzBCQndFd0hnWUpZSVpJQVdVREJBRXVNQkVFREM2VjNVVVZTbWFrMGE0WVZnSUJFSUE3UnFIN2h0bVF2N3l6NXhlSkdNRTJGdEFWb2dta3hJb2NyZVFiaHoxMWxQRTRod0RBbTJTTHhjV3REbmtTVUM1dWx0YU5FVllOTC9KcDBBTT0iLCJ2ZXJzaW9uIjoiMiIsInR5cGUiOiJEQVRBX0tFWSIsImV4cGlyYXRpb24iOjE2NjkzOTU4NDJ9 268945887964.dkr.ecr.ap-northeast-1.amazonaws.com
docker push 268945887964.dkr.ecr.ap-northeast-1.amazonaws.com/dummy-whisper:latest
#========================================================================
# push it to ECR
# with the full name.
echo "$fullname"
docker push ${fullname}

docker save --output image_class.tar ${image}  

# docker login --username AWS --password-stdin 268945887964.dkr.ecr.ap-northeast-1.amazonaws.com

