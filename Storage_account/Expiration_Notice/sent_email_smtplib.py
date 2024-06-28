import smtplib
import config
from email.mime.text import MIMEText 

email_account = config.email_account
email_password = config.emil_password
sender=config.sender
recipient=config.recipient
copy_recipient=config.copy_recipient
mail_server=config.mail_server
mail_port=config.mail_port
recipients=config.recipients
message=config.message

mime=MIMEText(message, "plain", "utf-8") #撰寫內文內容，以及指定格式為plain，語言為中文
mime["Subject"]="Mail test測試" #郵件標題
mime["From"]=sender #寄件人的暱稱或是信箱
mime["To"]=recipients #收件人
mime["Cc"]=sender #副本收件人
msg=mime.as_string() #將msg將text轉成str


smtp=smtplib.SMTP(mail_server,mail_port)  #mail server and port number
smtp.ehlo() #申請身分
# smtp.starttls() #mail server不支援傳輸層安全 (TLS)私密性與驗證，俗稱 SSL加密。
# smtp.ehlo()
# smtp.login(email_account, email_password) 
from_addr=email_account
to_addr=[recipient] #收件人
status=smtp.sendmail(from_addr,to_addr, msg)
if status=={}:
    print("郵件傳送成功!")
    print("寄送給: ", recipients)
else:
    print("郵件傳送失敗!")
smtp.quit()