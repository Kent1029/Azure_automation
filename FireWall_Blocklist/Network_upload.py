from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import json
import config

def main():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=config.subscription_id,
    )
    # 從 JSON 檔案中讀取數據
    with open('NetWork.json') as f:
        parameters = json.load(f)

    response = client.firewall_policy_rule_collection_groups.begin_create_or_update(
        resource_group_name=config.resource_group_name,
        firewall_policy_name=config.firewall_policy_name,
        rule_collection_group_name=config.network_rule_collection_group_name,
        parameters=parameters).result()
    print(response)


# x-ms-original-file: specification/network/resource-manager/Microsoft.Network/stable/2023-09-01/examples/FirewallPolicyRuleCollectionGroupWithHttpHeadersToInsert.json
if __name__ == "__main__":
    main()