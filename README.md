# AZURE AUTOMATION


This repository contains a collection of Azure Automation runbooks and scripts that can be used to automate common tasks in Azure.

## Storage Account
**Automator to download files from Azure Blob Storage and send an email notification to the user before they expired the access right.**


### Environment setup
```
conda create -n azure python=3.10
conda activate azure
pip install azure-storage-blob
```

### Configuration
```
touch config.py
vim config.py
```
```python
connectionString="<your connection_String>"
#connection_string = "DefaultEndpointsProtocol=https;AccountName=xxxx;AccountKey=xxxx;EndpointSuffix=core.windows.net"
email_account="<your email_accout>"
email_password="<your email_password>"
```

#### How to get connection string ？
1. Go to Azure Portal
2. Go to Storage Account
3. Go to Access Keys
4. Open the Azure cloud shell and run the following command
```bash
az storage account show-connection-string -n MyStorageAccount
```
5. Paste it in the config.py file
6. Done

## How to run ？
```bash
cd storage_account
python main.py
```

## What you will get ？

1. Download the daily backup data from the backup container of Azure Blob Storage in **Daily_backup_data** floder.
2. Recieve the expired data in **Daily_expired_data** floder.
3. Send an email notification to the user before they expired the access right.