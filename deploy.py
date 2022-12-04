import sagemaker
#===============================================================
# Imports
import io
import os
import sys
import time
import json
from IPython.display import display
from time import strftime, gmtime
import boto3
import re
import sagemaker
from sagemaker import get_execution_role
import argparse
def main(args):
    # Get the boto3 session and sagemaker client, as well as the current execution role
    sess = boto3.Session()
    sm = sess.client('sagemaker')
    role = sagemaker.get_execution_role()

    # Name of the docker image containing the model code
    # docker_image_name = '268945887964.dkr.ecr.ap-northeast-1.amazonaws.com/dummy-whisper'
    docker_image_name = f"268945887964.dkr.ecr.ap-northeast-1.amazonaws.com/{args.model_prefix}:latest"
    # docker_image_name = 'dummy-whisper'

    # Name and prefix for the S3 bucket storing the model output
    account_id = sess.client('sts', region_name=sess.region_name).get_caller_identity()["Account"]
    # bucket = 'sagemaker-studio-{}-{}'.format(sess.region_name, account_id)
    # prefix = 'dummy-whisper1'
    #===============================================================
    sess = sagemaker.session.Session()
    dummy_whisper = sagemaker.estimator.Estimator(docker_image_name,
                                        role=role,
                                        train_instance_count=1, 
                                        train_instance_type=args.train_instance_type,
    #                                     output_path='s3://{}/{}/output'.format(bucket, prefix),
    #                                       output_path='s3://sagemaker-ap-northeast-1-268945887964', 
    #                                       output_path='s3://sagemaker-ap-northeast-1-268945887964/custom_inference/',
                                          output_path=f's3://sagemaker-ap-northeast-1-268945887964/{args.model_prefix}',# this is for saving training results
                                        base_job_name=args.model_prefix,
                                        sagemaker_session=sess)
    #===============================================================
    dummy_whisper.fit()
    #===============================================================
    endpoint_name = f'{args.model_prefix}-endpoint'
    from sagemaker.async_inference.async_inference_config import AsyncInferenceConfig
    '''
    dummy_whisper.deploy(initial_instance_count=1, 
                                                 instance_type=args.instance_type, 
                                                 endpoint_name=endpoint_name,
                                                 async_inference_config=AsyncInferenceConfig
                         (
                             {
                            "OutputConfig": {
                                "S3OutputPath": f"s3://sagemaker-ap-northeast-1-268945887964/{args.instance_type}/response",
                                # Optionally specify Amazon SNS topics
                                # "NotificationConfig": {
                                # "SuccessTopic": "arn:aws:sns:::",
                                # "ErrorTopic": "arn:aws:sns:::",
                                # }
                            },
                            "ClientConfig": {"MaxConcurrentInvocationsPerInstance": 4},
                        }),)
    '''
    print(f'deploying to {args.instance_type}')
    dummy_whisper.deploy(initial_instance_count=1, 
                                                 instance_type=args.instance_type, 
                                                 endpoint_name=endpoint_name,
                                                 async_inference_config=AsyncInferenceConfig(output_path = f"s3://sagemaker-ap-northeast-1-268945887964/{args.model_prefix}/response",max_concurrent_invocations_per_instance=1)
                        )
    #############################################################################
    # autoscaling
    client = boto3.client(
        "application-autoscaling"
    )  # Common class representing Application Auto Scaling for SageMaker amongst other services

    resource_id = (
        "endpoint/" + endpoint_name + "/variant/" + "AllTraffic"
    )  # This is the format in which application autoscaling references the endpoint

    # Configure Autoscaling on asynchronous endpoint down to zero instances
    response = client.register_scalable_target(
        ServiceNamespace="sagemaker",
        ResourceId=resource_id,
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        MinCapacity=0,
        MaxCapacity=5,
    )

    response = client.put_scaling_policy(
        PolicyName="Invocations-ScalingPolicy",
        ServiceNamespace="sagemaker",  # The namespace of the AWS service that provides the resource.
        ResourceId=resource_id,  # Endpoint name
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",  # SageMaker supports only Instance Count
        PolicyType="TargetTrackingScaling",  # 'StepScaling'|'TargetTrackingScaling'
        TargetTrackingScalingPolicyConfiguration={
            "TargetValue": 5.0,  # The target value for the metric. - here the metric is - SageMakerVariantInvocationsPerInstance
            "CustomizedMetricSpecification": {
                "MetricName": "ApproximateBacklogSizePerInstance",
                "Namespace": "AWS/SageMaker",
                "Dimensions": [{"Name": "EndpointName", "Value": endpoint_name}],
                "Statistic": "Average",
            },
            "ScaleInCooldown": 600,  # The cooldown period helps you prevent your Auto Scaling group from launching or terminating
            # additional instances before the effects of previous activities are visible.
            # You can configure the length of time based on your instance startup time or other application needs.
            # ScaleInCooldown - The amount of time, in seconds, after a scale in activity completes before another scale in activity can start.
            "ScaleOutCooldown": 300  # ScaleOutCooldown - The amount of time, in seconds, after a scale out activity completes before another scale out activity can start.
            # 'DisableScaleIn': True|False - ndicates whether scale in by the target tracking policy is disabled.
            # If the value is true , scale in is disabled and the target tracking policy won't remove capacity from the scalable resource.
        },
    )

    #############################################################################

    # Delete endpoint when you don't need your model deployed
    if False:
        sm.delete_endpoint(EndpointName=endpoint_name)
        
        response = client.deregister_scalable_target(
            ServiceNamespace="sagemaker",
            ResourceId=resource_id,
            ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        )

    # view raw
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_instance_type',type=str,default='ml.m4.xlarge')
    parser.add_argument('--instance_type',type=str,default='ml.t2.medium')
    parser.add_argument('--model_prefix',type=str,default='dummy-whisper1')
    args = parser.parse_args()
    main(args)