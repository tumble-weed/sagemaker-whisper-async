model_prefix="dummy-whisper-async"
# instance_type="ml.m6g.xlarge"
# instance_type="ml.t2.medium" # for base
instance_type="ml.g4dn.xlarge"
train_instance_type="ml.m4.xlarge"
autoscaling=false
python cleanup.py --endpoint_name "${model_prefix}-endpoint" --endpoint_config_name "${model_prefix}-endpoint" --model_name $model_prefix --autoscaling False
bash build_and_push.sh $model_prefix true
sleep 5 # will this fix unable to get credentials error?
python deploy.py --train_instance_type $train_instance_type --instance_type $instance_type --model_prefix $model_prefix --autoscaling $autoscaling