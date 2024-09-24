import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-west-3")

'''Refer to EC2 Document in Boto to find all the functions you want with their
   inputs and outpust an everthing you need as a guide to get what you want '''

def create_volume_snapshots():

    # BackUp only Prod Servers..
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['prod']
            }
        ]
    )
    for volume in volumes['Volumes']:
        new_snapshot = ec2_client.create_snapshot(
        
            # Create Snapshots by referncing volume id 
            # which created by default and attached to each EC2 Server.. 
            VolumeId=volume['VolumeId']
        )
        print(new_snapshot)


schedule.every().day.do(create_volume_snapshots)

while True:
    schedule.run_pending()
