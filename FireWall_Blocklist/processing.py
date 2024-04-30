import json
import glob
import argparse
import pandas as pd

def get_NetWork_from_xlsx(file_path,sheet_name):
    # 讀取xlsx檔案的第一個分頁
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # 選擇[IP&URL]欄位的所有資料並轉換為list
    NetWork_list = df['IP & URL'].tolist()

    # 將每個URL中的'[.]'替換為'.'
    NetWork_list = [url.replace('[.]', '.') for url in NetWork_list]
    NetWork_number = len(NetWork_list)

    print("NetWork_list：",NetWork_list)
    print(f"共有{NetWork_number}筆NetWork data")
    # 回傳該list
    return NetWork_list

def get_FQDN_from_xlsx(file_path,sheet_name):
    # 讀取xlsx檔案的第一個分頁
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # 選擇[IP&URL]欄位的所有資料並轉換為list
    FQDN_list = df['IP & URL'].tolist()

    # 將每個URL中的'[.]'替換為'.'
    FQDN_list = [url.replace('[.]', '.') for url in FQDN_list]
    FQDN_number = len(FQDN_list)

    print("FQDN_list：",FQDN_list)
    print(f"共有{FQDN_number}筆FQDN data")
    # 回傳該list
    return FQDN_list

def replace_json(file_path,data_list):
    # raed and parse the json file
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    if file_path == 'FQDN.json':
        # replace "targetFqdns" value
        for rule in data['properties']['ruleCollections'][0]['rules']:
            rule['targetFqdns'] = data_list  
    elif file_path == 'NetWork.json':
        # replace "destinationAddresses" value
        for rule in data['properties']['ruleCollections'][0]['rules']:
            rule['destinationAddresses'] = data_list

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4) # indent=4: 縮排4個空格

    print(f"{file_path} has been replaced.")

def main(mode):
    #Receive the xlsx file path from the current folder
    xlsx_files_List = glob.glob('*.xlsx')

    #For each xlsx file, get the data and replace the json file
    for file_path in xlsx_files_List:
        if mode == 'NetWork':
            NetWork_list = get_NetWork_from_xlsx(file_path, 'Malicious & ACSI SOC - IP')
            replace_json('NetWork.json', NetWork_list)
        elif mode == 'FQDN':
            FQDN_list = get_FQDN_from_xlsx(file_path, 'Malicious & ACSI SOC - FQDN')
            replace_json('FQDN.json', FQDN_list)

if __name__ == "__main__":
    print("processing.py is running...")
    