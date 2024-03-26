import smtplib
import config
from email.mime.text import MIMEText 

email_account = config.email_account
email_password = config.emil_password
recipient=config.recipient
sender=config.sender
copy_recipient=config.copy_recipient
mail_server=config.mail_server
mail_port=config.mail_port


mime=MIMEText("你好世界 hollo world!", "plain", "utf-8") #撰寫內文內容，以及指定格式為plain，語言為中文
mime["Subject"]="test測試" #郵件標題
mime["From"]=sender #寄件人的暱稱或是信箱
mime["To"]=recipient #收件人
mime["Cc"]=copy_recipient #副本收件人
msg=mime.as_string() #將msg將text轉成str


smtp=smtplib.SMTP(mail_server,mail_port)  #googl的ping
smtp.ehlo() #申請身分
smtp.starttls() #加密文件，避免私密信息被截取
smtp.login(email_account, email_password) 
from_addr=email_password
to_addr=[recipient] #收件人
status=smtp.sendmail(from_addr, to_addr, msg)
if status=={}:
    print("郵件傳送成功!")
else:
    print("郵件傳送失敗!")
smtp.quit()