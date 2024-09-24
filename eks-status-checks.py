import boto3

client = boto3.client('eks', region_name="eu-west-3")

# "list_clusters()" Fun that List all the clusters in that region
# As usual we get the output structure frol the "Response Syntax" part in the EKS in Boto doc..
# So we get that entry 'clusters' from there..
# So now that vaariable is a list of cluster names..
clusters = client.list_clusters()['clusters']

for cluster in clusters:
    # describe_cluster()" Fun that give us a lot of info about the clsuters
    # but we iterate its output to get only the values we want
    response = client.describe_cluster(
        name=cluster
    )
    # that give us the cluster dic and we get the values we want using the keys..
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']

    print(f"Cluster {cluster} status is {cluster_status}")
    print(f"Cluster endpoint: {cluster_endpoint}")
    print(f"Cluster version: {cluster_version}")
