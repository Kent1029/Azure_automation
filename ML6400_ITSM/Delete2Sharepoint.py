import configparser
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from datetime import datetime, timedelta

# Read config.ini
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

# Setting the date to be used in the file name
now = datetime.now()
date = now.strftime("%m_%d")

yesterday = datetime.now() - timedelta(days=1)
yesterday_date = yesterday.strftime("%m_%d")

# Read config.ini
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

def delete_file(Ticket_excel):

    # Setting the variables from the config.ini
    Username = config['Sharepoint']['username'].replace('"', '')
    Password = config['Sharepoint']['password'].replace('"', '')
    Department_SiteURL = config['Sharepoint']['Department_SiteURL'].replace('"', '')
    website = config['Sharepoint']['website'].replace('"', '')

    # Connect to the Sharepoint by using the shareplum
    authcookie = Office365(website, username=Username, password=Password).GetCookies()
    site = Site(Department_SiteURL, version=Version.v365, authcookie=authcookie)

    # Delete the file from the Sharepoint
    folder = site.Folder('Shared Documents/General/Azure_automation/ITSM')
    folder.delete_file(yesterday_date+"_"+Ticket_excel)

def main(Ticket_excel):
    delete_file(Ticket_excel)

if __name__ == '__main__':
     Ticket_excel="Ticket_ITSM_Form_Department.xlsx"
     main(Ticket_excel)