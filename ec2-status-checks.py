import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-central-1")
ec2_resource = boto3.resource('ec2', region_name="eu-central-1")


def check_instance_status():

    # That will give us all the instances in th provided region 
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    
    """ Go to the Returns Response Syntax in the "describe_instance_status" documentation
        to see how to get what you exactly want from the output"""
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(f"Instance {status['InstanceId']} is {state} with instance status {ins_status} and system status {sys_status}")
    print("#############################\n")


schedule.every(5).seconds.do(check_instance_status)

# To run the scheduler
while True:
    schedule.run_pending()
