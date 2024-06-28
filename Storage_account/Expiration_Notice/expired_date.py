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
    pattern = f'/home/kent/Azure_automation/Storage_account/Expiration_Notice/Daily_backup_data/Backup-{today}*'  # backup-2024-03-24T15_02_36.4734652Z.json
    # print(f'Pattern: {pattern}')
    files = glob.glob(pattern)
    # print(f'Files: {files}')
    if len(files) == 0:
        print(f'No file found for today: {pattern}')
        sys.exit(1)
    for filename in files:
        print("Access filename:")
        print(f"Backup-{today}.json")
        print()
    return filename

def open_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

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
            # 如果日期差異小於30天，則添加到list中
            if delta.days <= 30:
                filtered_data.append(data)
    print('Expired data:')
    if len(filtered_data) == 0:
        print('No data expired in 30 days')
    else:
        print(filtered_data)
    print()
    return filtered_data


def storage_names_as_json_and_excel(datas):
    # 儲存為JSON文件
    today = datetime.today().date()
    today=str(today)
    filename_json = f'{today}-expire-in-30-days.json'
    filename_excel = f'{today}-expire-in-30-days.xlsx'
    if len(datas) == 0:
        print('Result:')
        print('No data expired in 30 days, no file generated')
    else:
        # Save as JSON
        with open(f'/home/kent/Azure_automation/Storage_account/Expiration_Notice/Daily_expired_data/Json/{filename_json}', 'w', encoding='utf-8') as f:
            json.dump(datas, f)
        
        # Save as Excel
        df = pd.DataFrame(datas)
        df.to_excel(f'/home/kent/Azure_automation/Storage_account/Expiration_Notice/Daily_expired_data/Excel/{filename_excel}', index=True, header=False)

        print('Result:')
        print(f'The expired result have been stored in Daily_expired_data folder.')
        print("JSON File Name：",filename_json)
        print("Excel File Name：",filename_excel)

def get_mail_recipients(data_expired):
    recipient_list=[]
    for data in data_expired:
        # 分割data得到收件人
        parts = data.split('.')
        name_str = parts[1] if len(parts) > 2 else None
        name_str=name_str+"@company.com"
        recipient_list.append(name_str)
    recipients = ", ".join(recipient_list)
    #print(recipients)
    # 讀取config.py的內容
    with open("/home/kent/Azure_automation/Storage_account/Expiration_Notice/config.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # 找到recipients變量的定義並替換它
    new_lines = []
    for line in lines:
        if line.strip().startswith('recipients ='):
            new_lines.append(f'recipients = "{recipients}"\n')
        else:
            new_lines.append(line)
    # 將修改後的內容寫回config.py
    with open("/home/kent/Azure_automation/Storage_account/Expiration_Notice/config.py", 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    return recipients

def get_table_data(data_expired):
    # 開始構建HTML表格
    table_html = """
    <table style="border: 1px solid black; border-collapse: collapse;">
      <tr>
        <th style="border: 1px solid black; padding: 10px; text-align: center;">Order number</th>
        <th style="border: 1px solid black; padding: 10px; text-align: center;">Username</th>
        <th style="border: 1px solid black; padding: 10px; text-align: center;">Expiration date</th>
      </tr>
    """

    # 為每個項目添加一行
    for data in data_expired:
        order_number, username, expiry_date = data.split('.')
        table_html += f"""
        <tr>
          <td style="border: 1px solid black; padding: 10px; text-align: center;">{order_number}</td>
          <td style="border: 1px solid black; padding: 10px; text-align: center;">{username}</td>
          <td style="border: 1px solid black; padding: 10px; text-align: center;">{expiry_date}</td>
        </tr>
        """

    # 結束表格
    table_html += "</table>"

    return table_html

def replace_table(table_html):
    # 讀取HTML_message.py文件
    with open("/home/kent/Azure_automation/Storage_account/Expiration_Notice/HTML_message.py", 'r', encoding='utf-8') as f:
        html_message = f.read()

    # 尋找表格的開始和結束位置
    start = html_message.find('<table style="border: 1px solid black; border-collapse: collapse;">')
    end = html_message.find('</table>') + len('</table>')

    # 替換表格
    new_html_message = html_message[:start] + table_html + html_message[end:]

    # 將修改後的內容寫回HTML_message.py
    with open("/home/kent/Azure_automation/Storage_account/Expiration_Notice/HTML_message.py", 'w', encoding='utf-8') as f:
        f.write(new_html_message)

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
    storage_names_as_json_and_excel(data_expired)
    get_mail_recipients(data_expired)
    table_html=get_table_data(data_expired)
    replace_table(table_html)

if __name__ == "__main__":
    run()


58 2 * * 1 /usr/bin/python3 /home/kent/Azure_automation/Storage_account/Expiration_Notice/main.py >> /home/kent/Azure_automation/Storage_account/Expiration_Notice/cron.log 2>&1