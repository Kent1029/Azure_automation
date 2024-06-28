import re
import time
import json
import shutil
import openpyxl
import configparser
import Azure_access
import pandas as pd
import requests as req
from datetime import datetime, timedelta, date

# Import the functions we wrote
import Upload2Sharepoint
import Delete2Sharepoint

# Read config.ini
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
Ticket_excel="Ticket_ITSM_Form_Department.xlsx"

# Read Excel and filter the data by yesterday date
def read_excel(excel_path):
    df = pd.read_excel(excel_path, sheet_name='Form1')
    df['SubmitTime'] = pd.to_datetime(df['SubmitTime'])
    yesterday = datetime.now() - timedelta(days=1)
    df = df[df['SubmitTime'] > yesterday]
    df = df.reset_index(drop=True)

    SubmitTimes=df['SubmitTime']
    UserMails=df["UserMail"]
    UserNames=df["UserName"]
    AdminNames=df["AdminName"]
    ProblemTitles=df["ProblemTitle"]
    ProblemDescriptions=df["ProblemDescription"]
    SolutionWays=df["SolutionWay"]
    Urgents=df["Urgent"]

    return SubmitTimes, UserMails, UserNames, AdminNames, ProblemTitles, ProblemDescriptions, SolutionWays, Urgents

# Print the values in the Excel for testing
def print_excel_values(excel_path):
    df = pd.read_excel(excel_path, sheet_name='Form1')
    print(df)

# Record the ticket number in the Excel
def record_ticket_number(response, SubmitTime, UserMail, UserName, AdminName, ProblemTitle, ProblemDescription, SolutionWay, Urgent):
    json_data = json.loads(response.text)
    messages = json_data["Messages"][0]
    ticket_numbers = re.search(r'"(.*?)"', messages).group(1)
            
    wb = openpyxl.load_workbook(Ticket_excel, data_only=True)
    sheet1=wb['sheet1'] 
    sheet1.append([SubmitTime, UserMail, UserName, AdminName, ProblemTitle, ProblemDescription, SolutionWay, Urgent, ticket_numbers])
    wb.save(Ticket_excel)
    print("Ticket number recorded: ", ticket_numbers)
    print("------------------------------------")

# Call the API
def callAPI(SubmitTimes, UserMails, UserNames, AdminNames, ProblemTitles, ProblemDescriptions, SolutionWays, Urgents):
    
    # Read config.ini for the URL and headers
    url = config['URL']['PRD'].replace('"', '')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': config['headers']['Authorization'].replace('"', '')
    }

    # Call the API for each row in the Excel
    for i in range(len(UserNames)):
        SubmitTime=SubmitTimes[i]
        UserMail=UserMails[i]
        UserName=UserNames[i]
        AdminName=AdminNames[i]
        ProblemTitle=ProblemTitles[i]
        ProblemDescription=ProblemDescriptions[i]
        SolutionWay=SolutionWays[i]
        Urgent=str(Urgents[i])

        if AdminName=="IHTMCHANG" or AdminName == "IHLIZZYLIAO" or AdminName == "IHRITALIU" or AdminName == "HQKENTHUANG":
            Workgroup= config['Devops']['Workgroup'].replace('"', '')
            Subcategory= config['Devops']['Subcategory'].replace('"', '')
            PrimaryCI= config['Devops']['PrimaryCI'].replace('"', '')
        elif AdminName == "HQKEYNESLEE" or AdminName == "HQYUNALIN" or AdminName == "WITJOHNNYLIN":
            Workgroup= config['Cloud']['Workgroup'].replace('"', '')
            Subcategory= config['Cloud']['Subcategory'].replace('"', '')
            PrimaryCI= config['Cloud']['PrimaryCI'].replace('"', '')
        elif AdminName == "IHMARKKCLI" or AdminName == "IHCINDYHSU" or AdminName == "IHJERRYCLHSU"or AdminName == "IHELLYCHANG":
            Workgroup= config['Data']['Workgroup'].replace('"', '')
            Subcategory= config['Data']['Subcategory'].replace('"', '')
            PrimaryCI= config['Data']['PrimaryCI'].replace('"', '')

        data={
            "CreateInfraSRTicket":{
                "ContactName":UserName,
                "Assignee":AdminName,
                "Title":ProblemTitle,
                "Description":ProblemDescription,
                "Medium":SolutionWay,
                "Urgency":Urgent,
                "Workgroup":Workgroup, #視服務改變
                "Subcategory":Subcategory, #視服務改變
                "PrimaryCI":PrimaryCI, #Affected CI,視服務改變
                "Impact":"2", #不變
                "Location":"GDC", #不變
                }
            }
        
        # Call the API
        response = req.post(url, headers=headers, data=json.dumps(data))

        # Print the response status code and text
        today = date.today()
        print("------------------------------------")
        print(today)
        print("Status_code：",response.status_code)
        print("Response.text：",response.text)

        #To avoid the API call limit
        time.sleep(2)

        # Record the ticket number in the Excel
        record_ticket_number(response, SubmitTime, UserMail, UserName, AdminName, ProblemTitle, ProblemDescription, SolutionWay, Urgent)

if __name__ == '__main__':

    #Download the latest file from Azure Blob Storage
    Azure_access.run()

    #Move the downloaded file and the folder
    excel_path="ITSM_Form_Department.xlsx"
    floder_path="Excel_file"

    #Read Excel
    SubmitTimes, UserMails, UserNames, AdminNames, ProblemTitles, ProblemDescriptions, SolutionWays, Urgents=read_excel(excel_path)
    
    #Call API
    callAPI(SubmitTimes, UserMails, UserNames, AdminNames, ProblemTitles, ProblemDescriptions, SolutionWays, Urgents)
    
    #Upload the file to the Sharepoint
    Upload2Sharepoint.main(Ticket_excel)

    #Delete the yesterday file from the Sharepoint
    Delete2Sharepoint.main(Ticket_excel)
    
    #Move the downloaded file and the folder
    now = datetime.now()
    date_string = now.strftime("%m_%d")
    shutil.move(excel_path, floder_path+"/"+date_string+"_"+excel_path)

