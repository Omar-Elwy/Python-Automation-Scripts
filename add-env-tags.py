import boto3

# Some Functions are avaialbe in client & others in resource
# So we have to make sure which one to call depends on the functions we use..

ec2_client_paris = boto3.client('ec2', region_name="eu-west-3")
ec2_resource_paris = boto3.resource('ec2', region_name="eu-west-3")

ec2_client_frankfurt = boto3.client('ec2', region_name="eu-central-1")
ec2_resource_frankfurt = boto3.resource('ec2', region_name="eu-central-1")

# We initializing empty lists to collect the instances IDs while looping..
instance_ids_paris = []
instance_ids_frankfurt = []

# That will give us all the instances in the region "describe_instances()"
#"Resevations" is a list
reservations_paris = ec2_client_paris.describe_instances()['Reservations']

 """ Go to the Returns Response Syntax in the "describe_instances()" function in the 
 BOTO documentation to see how to get what you exactly want from the output """
# now we will iterate the "Reservations" list..
for res in reservations_paris:
    instances = res['Instances']

# we went to "instances" key which is also a list inside the Dictionery    
    for ins in instances:
        instance_ids_paris.append(ins['InstanceId'])

# "create_tags" function can add tags to any type of AWS resources
# This is the request syntax part from the "create_tags" function in the Boto documentation
response = ec2_resource_paris.create_tags(

    # resources accepts a list of strings which we provided here
    Resources=instance_ids_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

# That will give us all the instances in the region
reservations_frankfurt = ec2_client_frankfurt.describe_instances()['Reservations']
for res in reservations_frankfurt:
    instances = res['Instances']
    for ins in instances:
        instance_ids_frankfurt.append(ins['InstanceId'])


response = ec2_resource_frankfurt.create_tags(
    Resources=instance_ids_frankfurt,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)
