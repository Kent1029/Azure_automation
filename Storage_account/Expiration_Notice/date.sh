week_number=$(date +\%U)
date_today=$(date)
echo "Week number is: "$week_number
echo "Today is:"$date_today
week_number=$((week_number + 1))
if ((week_number % 2 == 0 ))
then
  echo "This is an even week. No action is taken."
  #python3 /home/kent/Azure_automation/Storage_account/main.py

else
  echo "This is an odd week. Running main.py..."
  python3 /home/kent/Azure_automation/Storage_account/main.py

fi

echo "--------------------------------------------------------"

#0 1 * * 1 /home/kent/Azure_automation/Storage_account/date.sh >> /home/kent/cron.log 2>&1

#隔週跑一次的判斷code，首先判斷今天是不是偶數週，如果是偶數週就不執行，如果是奇數週就執行main.py