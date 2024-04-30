from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import json
import config

def main(mode):
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=config.subscription_id,
    )

    if mode == "NetWork":
        with open('NetWork.json') as f:
            parameters = json.load(f)

        #start the upload
        print("Uploading Network rule collection group...")
        response = client.firewall_policy_rule_collection_groups.begin_create_or_update(
            resource_group_name=config.resource_group_name,
            firewall_policy_name=config.firewall_policy_name,
            rule_collection_group_name=config.network_rule_collection_group_name,
            parameters=parameters).result()
        print(response)
        print("Network rule collection group upload successfully.")

    elif mode == "FQDN":
        with open('FQDN.json') as f:
            parameters = json.load(f)
        
        #start the upload
        print("Uploading FQDN rule collection group...")
        response = client.firewall_policy_rule_collection_groups.begin_create_or_update(
            resource_group_name=config.resource_group_name,
            firewall_policy_name=config.firewall_policy_name,
            rule_collection_group_name=config.FQDN_rule_collection_group_name,
            parameters=parameters).result()
        print(response)
        print("FQDN rule collection group upload successfully.")

if __name__ == "__main__":
    main()