# IDEA : Iterate the snapshots we have in AWS while Sorting them by date to deter old ones

import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="eu-west-3")

# we referncing the volumes that we are working with..
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['prod']
        }
    ]
)

# we iterating the volumes that get from "describe_volumes"..
for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
    
        # To get only the snapshots we created ourselves,
        #cause ther are snapshots that are created by default by AWS itself..
        OwnerIds=['self'],
        
        # Getting snapshots by their volumes ids attached to them..
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )
    
    # A list of Snapshots sorted by 'StartTime' Key..
    # "itemgetter" is a function from module "operator"
    # "reverse=True" to get the most recent snapshots in the beginning of the list..  
    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    # To begin iterating and cleaning up from the third snapshot 
    # As we want to keep the 2 most recent ones..
    for snap in sorted_by_date[2:]:
        # delete each snapshot in our loop by refrencing snapshot ID 
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        print(response)
        
# And surely we can put all of this in a function and refrence it by scheduler###        


