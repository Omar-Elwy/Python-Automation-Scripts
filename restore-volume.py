# IDEA : Creating new volune from the latest snapshot available ##

import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="eu-west-3")
ec2_resource = boto3.resource('ec2', region_name="eu-west-3")

# The EC2 server which we want to recover its vloune from the latest snapshot
instance_id = "i-04f01be7a765eaf7e"

volumes = ec2_client.describe_volumes(
   
    # Get volumes attached to this EC2 Server
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

# We did that cause we excpect the instance to have pnly one attcahed volume to it..
instance_volume = volumes['Volumes'][0]

# Get all thhe snapshots that we created from that volume.. 
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    # filtering tags is very different from adding with tags
    # Here n the name we must specify predefind "Doc" value and values is list..
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

# A list of Snapshots sorted by 'StartTime' Key.. 
# "itemgetter" is a function from module "operator"
# "reverse=True" to get the most recent snapshots in the beginning of the list..
# "[0]" : Getting the first element of the list which is the latest snapshot..
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])

# Create volume from the latest snapshot BackUP..
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-3b",
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            # Adding tags is very different from filtering with tags
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                }
            ]
        }
    ]
)
# NOw we wnat to attach this volume to the EC2 server.. 

# We check the volume over and over untill its in the available state
# To be able to attach it to the Instance..
while True:
    
    # That wil give us the volume that we just created
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    # We printing the state of the volume  
    print(vol.state)
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'
        )
        break
