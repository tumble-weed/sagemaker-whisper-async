

 provider "aws" {
     access_key = "<ACCESS_KEY>"
     secret_key = "<SECRET_KEY>"
     region = "<REGION>"
 }
 

 variable "user_data" {
     default = <<EOF
     {
         echo "ECS_CLUSTER=whisper_cluster"
     } >> /etc/ecs/ecs.config
     EOF
 }
 

 resource "aws_ecs_cluster" "whisper_cluster"{
     name = "whisper_cluster"
 }
 

 resource "aws_instance" "ec2_whisper" {
     #name = "ec2_whisper"
     tags = {
     Name = "ec2_whisper"
     }
     ami = "ami-0f0fe3100d00e9eda"
     #instance_type = "t2.micro"
     instance_type = "g4dn.xlarge"
     # security_group = "web-server"
     key_name = "aniket1"
     # cluster_id = whisper_cluster.id
     user_data = "${var.user_data}"
 }
 

 resource  "aws_iam_role" "ecs_task_execution_role1"{
 name = "ecs_task_execution_role1"
 
 assume_role_policy = <<EOF
 {
     "Version": "2012-10-17",
     "Statement":[
     {
         "Action":"sts:AssumeRole",
         "Effect":"Allow",
         "Principal":{
         "Service":"ecs-tasks.amazonaws.com"
         },
         "Sid":""
         
     }
     ]
 }
 EOF
 }


 resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy"{
 #name = "ecs_task_execution_policy"
 role = "${aws_iam_role.ecs_task_execution_role1.name}"
 policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
 }


resource "aws_ecs_task_definition" "task_whisper" {
family = "task_whisper"
network_mode = "bridge"
execution_role_arn = "${aws_iam_role.ecs_task_execution_role1.arn}"
#task_role_arn
requires_compatibilities = ["EC2"]

container_definitions = <<EOF
[
{
"name":"whisper-container",
"image":"whisper-async:latest",
"portMappings":[{
    "hostPort":80,
    "containerPort":80
}],
"memoryReservation": 16384,
"essential": true
}
]
EOF
}
