import json
import glob
import sys
import pandas as pd
from datetime import datetime


def get_today_filename():
    # 取得今天日期
    # 用今天日期當標頭，找出當天的檔案
    today = datetime.today().date()
    today=str(today)
    pattern = f'./Daily_backup_data/Backup-{today}*'  # backup-2024-03-24T15_02_36.4734652Z.json
    # print(f'Pattern: {pattern}')
    files = glob.glob(pattern)
    # print(f'Files: {files}')
    if len(files) == 0:
        print(f'No file found for today: {pattern}')
        sys.exit(1)
    for filename in files:
        print("Access filename:")
        print(filename)
        print()
    return filename

def open_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# def extract_rule_name(data):
#     datas=[]
#     for resource in data['resources']:
#         # 檢查是否存在properties和ruleCollections
#         if 'properties' in resource and 'ruleCollections' in resource['properties']:
#             # 遍歷每一個ruleCollections
#             for ruleCollection in resource['properties']['ruleCollections']:
#                 # 檢查是否存在rules
#                 if 'rules' in ruleCollection:
#                     # 遍歷每一個rules
#                     for rule in ruleCollection['rules']:
#                         # 檢查是否存在name並print
#                         if 'name' in rule:
#                             # print(rule['name'])
#                             datas.append(rule['name'])
#     print(datas)
#     return datas

def extract_rule_name(data):
    datas = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'name':
                datas.append(value)
            else:
                datas.extend(extract_rule_name(value))
    elif isinstance(data, list):
        for item in data:
            datas.extend(extract_rule_name(item))
    return datas

def clean_rule_name(datas):
    # 清洗資料
    names_clean = [name for name in datas if name.count('_') > 0 and name.count('.') >= 2 and name.startswith('G')]
    # print(names_clean)
    return names_clean

def cauculate_rule_expire(datas):
    # 計算有沒有過期
    today = datetime.today().date()

    filtered_data=[]
    for data in datas:
        # 分割data得到日期
        parts = data.split('.')
        date_str = parts[2] if len(parts) > 2 else None

        # 檢查日期部分的格式是否正確
        if date_str and date_str.isdigit() and len(date_str) == 8:
            # 將日期字符串轉換為日期類別
            item_date = datetime.strptime(date_str, '%Y%m%d').date()
            # 計算日期差異
            delta = item_date -today
            # 如果日期差異小於7天，則添加到list中
            if delta.days <= 7:
                filtered_data.append(data)
    print('Expired data:')
    if len(filtered_data) == 0:
        print('No data expired in 7 days')
    else:
        print(filtered_data)
    print()
    return filtered_data


def storage_names_as_json_and_excel(datas):
    # 儲存為JSON文件
    today = datetime.today().date()
    today=str(today)
    filename_json = f'{today}-expire-in-7-days.json'
    filename_excel = f'{today}-expire-in-7-days.xlsx'
    if len(datas) == 0:
        print('Result:')
        print('No data expired in 7 days, no file generated')
    else:
        # Save as JSON
        with open(f'./Daily_expired_data/Json/{filename_json}', 'w') as f:
            json.dump(datas, f)
        
        # Save as Excel
        df = pd.DataFrame(datas)
        df.to_excel(f'./Daily_expired_data/Excel/{filename_excel}', index=True, header=False)

        print('Result:')
        print(f'The expired result have been stored in Daily_expired_data folder.')
        print("JSON File Name：",filename_json)
        print("Excel File Name：",filename_excel)

def sent_email(data_expired):
    recipient_list=[]
    for data in data_expired:
        # 分割data得到日期
        parts = data.split('.')
        date_str = parts[1] if len(parts) > 2 else None
        date_str=date_str+"@wistron.com"
        recipient_list.append(date_str)
    recipients = ", ".join(recipient_list)
    #print(recipients)
    return recipients


def run():
    # 程式執行的主要流程
    filename=get_today_filename()
    data=open_json_file(filename)
    # 把name取出來
    data=extract_rule_name(data)
    # 資料清洗
    data_clean=clean_rule_name(data)
    #計算有沒有過期
    data_expired=cauculate_rule_expire(data_clean)
    # 儲存為JSON和Excel文件
    #storage_names_as_json_and_excel(data_expired)
    recipients=sent_email(data_expired)
    
    # 讀取config.py的內容
    with open('config.py', 'r') as f:
        lines = f.readlines()
    # 找到recipients變量的定義並替換它
    new_lines = []
    for line in lines:
        if line.strip().startswith('recipients ='):
            new_lines.append(f'recipients = "{recipients}"\n')
        else:
            new_lines.append(line)
    # 將修改後的內容寫回config.py
    with open('config.py', 'w') as f:
        f.writelines(new_lines)
    


if __name__ == "__main__":
    run()