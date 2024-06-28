import sys
import os
import configparser
from datetime import datetime
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
# import config

# today = datetime.now().strftime("%Y%m%d")
# today_str = datetime.now().strftime("%Y-%m-%d")
configg = configparser.ConfigParser()
configg.read('config.ini', encoding='utf-8')
connectionString=configg['azure_config']['connectionString'].replace('"', '')


def list_blob_in_container():
    container = ContainerClient.from_connection_string(connectionString, container_name="itsm-dailybackup")
    blob_list = container.list_blobs()
    for blob in blob_list:
        print('The Blob name is: ')
        print(blob.name + '\n')
        return blob.name
    else:
        print('Result:')
        print('There are no backup files today')
        sys.exit(1)

def download_blob_from_container(blob_name):
    blob = BlobClient.from_connection_string(connectionString, container_name="itsm-dailybackup", blob_name=blob_name)
    
    with open(blob_name, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)

def run():
   blob_name = list_blob_in_container()
   download_blob_from_container(blob_name)

if __name__ == '__main__':
    run()