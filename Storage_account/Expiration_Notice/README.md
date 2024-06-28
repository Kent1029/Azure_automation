## Expiration_Notice
**Automator to download files from Azure Blob Storage and send an email notification to the user before they expired the access right.**


### Environment setup
```
conda create -n azure python=3.10
conda activate azure
pip install azure-storage-blob
```

### Create PostgreSQL database on [RDS (link)](https://consolewcp.company.com/#/DBlist)
You will recive the following information after you create the database.
1. Host
2. Database name
3. User
4. Password
5. Port

### Configuration
```
touch config.py
vim config.py
```
```python
#Configurations for the project
connectionString="<your connection_String>"
#connection_string = "DefaultEndpointsProtocol=https;AccountName=xxxx;AccountKey=xxxx;EndpointSuffix=core.windows.net"

#Mail
sender="<sender email>"
mail_server="<mail server>"
mail_port="<mail port>"
account_name="<VM account name>"#kent
recipients="<recipients email>"
#SQL
host="<Database host>"
dbname="<Database name>"
user="<Database user>" #The name when you create on the RDS
password="<Database password>"
port="<Database port>"#15248

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