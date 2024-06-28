## Department Create Ticket to ITSM System

**In this code, you can easily automatically create tickets to the ITSM system according to daily user needs.**

### Environment setup
```
conda create -n azure python=3.10
conda activate azure
pip install azure-identity
pip install -r requirements.txt
```
### Configuration
```
touch config.ini
vim config.ini
```

```python
#Azure Storage Account Blob
[azure_config]
connectionString = <>

#Token by ITSM account
[headers]
Authorization = <>

#ITSM Variable
[Devops]
Workgroup = <>
Subcategory = <>
PrimaryCI = <>

[Cloud]
Workgroup = <>
Subcategory = <>
PrimaryCI = <>

[Data]
Workgroup = <>
Subcategory = <>
PrimaryCI = <>

#ITSM URL
[URL] 
PRD = <>
QA = <>

#ITSM Account
[Account]
username = <>
password = <>

#Microsoft account
[Sharepoint]
username = <>
password = <>
DepartmentSiteURL = <> #"https://xxxxxx.sharepoint.com/teams/MLxxxxxx/"
website = <> #"https://xxxxxx.sharepoint.com"
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
cd ITSM_Automation
python Department_create_ticket_api.py
```

## The script will do the following:
1. Doload the Block List-IOC Info excel file from the Azure Storage Blob.
2. Extract the NetWork IP and FQDN data from the excel file.
3. Replace the temporary JSON file
4. Upload to Azure FireWall Rule collections
5. Success

# Power Automate Describe


```
#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 Kent Huang, All Rights Reserved 
#
# @Time    : 2024/06/27
# @Author  : Kent Huang
# @File    : README.md
# @Project : ITSM_Automation
```
