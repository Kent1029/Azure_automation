import expired_date
import Azure_access
import sent_email_msmtp

def main():
    Azure_access.run()
    expired_date.run()
    sent_email_msmtp.main()

if __name__ == "__main__":
    main()

 
# crontab -e 
# 0 1 * * 1-5 /usr/bin/python3 /home/kent/Azure_automation/Storage_account/main.py >> /home/kent/cron.log 2>&1
