import boto3
import botocore
import sagemaker
from sagemaker import get_execution_role
import argparse
def main(args):
    # Get the boto3 session and sagemaker client, as well as the current execution role
    sess = boto3.Session()
    sm = sess.client('sagemaker')
    ecr = sess.client('ecr') 
    autoscaling_client = sess.client('application-autoscaling') 
    if args.endpoint_name:
        try:
            sm.delete_endpoint(EndpointName=args.endpoint_name)
            print(f'ENDPOINT {args.endpoint_name} deleted')
        except botocore.exceptions.ClientError as e:
            print(e)
            print('------ ignoring and proceeding ------')
    if args.endpoint_config_name:
        try:        
            sm.delete_endpoint_config(EndpointConfigName=args.endpoint_config_name)
            print(f'ENDPOINT CONFIG {args.endpoint_config_name} deleted')
        except botocore.exceptions.ClientError as e:
            print(e)            
            print('------ ignoring and proceeding ------')
    if args.model_name:
        try:        
            sm.delete_model(ModelName=args.model_name)
            print(f'Model {args.model_name} deleted')
        except botocore.exceptions.ClientError as e:
            print(e)            
            print('------ ignoring and proceeding ------')
    """
    if args.repository:
        ecr.batch_delete_image(
        registryId=,
        repositoryName=,
        imageTag=[
            {
                
            }
        ]
    )
    """
    if args.autoscaling:
        resource_id = (
        "endpoint/" + args.endpoint_name + "/variant/" + "AllTraffic"
    )  # This is the format in which application autoscaling references the endpoint
        response = autoscaling_client.deregister_scalable_target(
            ServiceNamespace="sagemaker",
            ResourceId=resource_id,
            ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        )
        print(f'autoscaling {resource_id} deleted')
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Don't put default values to prevent accidental deletion
    parser.add_argument('--endpoint_name',type=str,help='dummy-whisper1')
    parser.add_argument('--endpoint_config_name',type=str,help='dummy-whisper1-endpoint')
    parser.add_argument('--model_name',type=str,help='dummy-whisper1')
    parser.add_argument('--autoscaling',type=lambda s:(s.lower() == 'true'),default=False)
    args = parser.parse_args()
    main(args)
    
    