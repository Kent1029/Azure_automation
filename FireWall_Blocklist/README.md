## FireWall_Blocklist
**In the this part, you can add and modify the FQDN Block list from Trend Micro in the Firewall Policy Rule through the Azure API.**


### Environment setup
```
conda create -n azure python=3.10
conda activate azure
pip install azure-identity
```

### Configuration
```
touch config.py
vim config.py
```
```python
#FireWall_Blocklist
subscription_id=<> # Azure subscription ID
resource_group_name=<> # Azure resource group name
firewall_policy_name=<> # Azure Firewall Policy name
FQDN_rule_collection_group_name=<> # Azure Firewall FQDN rule collection group name
network_rule_collection_group_name=<> # Azure Firewall Network rule collection group name
```

## How to run ？
```bash
cd FireWall_Blocklist
python main_upload.py
```

## The script will do the following:
1. Extract the NetWork IP and FQDN data from the excel file.
2. Replace the temporary JSON file
3. Upload to Azure FireWall Rule collections
4. Success