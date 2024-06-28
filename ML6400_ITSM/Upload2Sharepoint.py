import configparser
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

# Read config.ini
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

def upload_file(Ticket_excel):

    # Setting the variables from the config.ini
    Username = config['Sharepoint']['username'].replace('"', '')
    Password = config['Sharepoint']['password'].replace('"', '')
    DepartmentSiteURL = config['Sharepoint']['Department_SiteURL'].replace('"', '')
    website = config['Sharepoint']['website'].replace('"', '')

    # Connect to the Sharepoint by using the shareplum
    authcookie = Office365(website, username=Username, password=Password).GetCookies()
    site = Site(DepartmentSiteURL, version=Version.v365, authcookie=authcookie)

    # Upload the file to the Sharepoint
    folder = site.Folder('Shared Documents/General/Azure_automation/ITSM')

    with open(Ticket_excel, mode='rb') as file:
            fileContent = file.read()
    folder.upload_file(fileContent, Ticket_excel)

def main(Ticket_excel):
    upload_file(Ticket_excel)

if __name__ == '__main__':
     Ticket_excel="Ticket_ITSM_Form_Department.xlsx"
     main(Ticket_excel)