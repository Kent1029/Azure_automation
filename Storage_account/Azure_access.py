
import sys
import config 
from datetime import datetime
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient

connectionString = config.connectionString
today = datetime.today().date()
today_str = today.strftime('%Y-%m-%d')

def list_blobs():
    container = ContainerClient.from_connection_string(conn_str=connectionString, container_name="backups")
    blob_list = container.list_blobs()
    for blob in blob_list:
        if today_str in blob.name:
            print('The Blob name is: ')
            print(blob.name + '\n')
            return blob.name
    else:
        print('Result:')
        print('There are no backup files today')
        sys.exit(1)

def download_blob(blob_name):
    blob = BlobClient.from_connection_string(conn_str=connectionString, container_name="backups", blob_name=blob_name)

    with open(f"./Daily_backup_data/Backup-{today}.json", "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)

def run():
    blob_name=list_blobs()
    download_blob(blob_name)

if __name__ == '__main__':
    run()




