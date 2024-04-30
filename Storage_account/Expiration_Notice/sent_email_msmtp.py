import os
import config
import HTML_message
from email.mime.text import MIMEText 



def main():
    sender=config.sender
    recipients=config.recipients
    account_name=config.account_name
    test_recipients=config.test_recipients
    message=HTML_message.message

    mime=MIMEText(message, "html", "utf-8") #撰寫內文內容，以及指定格式為html，編碼格式為utf-8
    mime["Subject"]="Firewall policy expiration notification" #郵件標題
    mime["From"]=sender #寄件人的暱稱或是信箱
    mime["To"]=test_recipients #收件人
    #mime["Cc"]=sender #副本收件人
    msg=mime.as_string() #將msg將text轉成str
    # 寫入一個臨時文件
    with open('temp.txt', 'w') as f:
        f.write(msg)

    # 使用msmtp發送郵件
    result = os.system(f'msmtp -a {account_name} -t < temp.txt')

    # 刪除臨時文件
    os.remove('temp.txt')
    # 檢查結果碼
    if result == 0:
        print("郵件已成功發送")
        print("寄送給: ", test_recipients)
        print("--------------------------------------")
    else:
        print("--------------------------------------")

if __name__ == "__main__":
    main()
