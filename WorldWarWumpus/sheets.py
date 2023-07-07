import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from Google import Create_Service
from management import getSheetIdWithName

#Checks for existing servername within the server list 
def checkExisting(servername,sheetname):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    row = sheet.row_values(1) 
    col = sheet.col_values(1)
    for name in col:
        if(servername == name):
            return True
    return False

#A more sophisticated check existing, except now not exclusively servernames
def checkExistingComp(thing,sheetname,columnnum):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    col = sheet.col_values(columnnum)
    for i in range(len(col)):
        if col[i] == thing: 
            return True
    return False
    
#Formats the basic inventory when setting up 
def formatBaseInventory(sheetname):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    row = sheet.row_values(1) 
    col = sheet.col_values(1)

#Adds cell of a certain item to a column of a certain sheet 
def addCell(item,sheetname):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    row = sheet.row_values(1) 
    col = sheet.col_values(1)
    sheet.update_cell(len(col)+1,1,str(item))

#Gets all values from a category within a sheet 
def getValuesFromCategory(category,sheetname):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    row = sheet.row_values(1) 
    col = sheet.col_values(1)
    for i in range(len(row)):
        if row[i] == category:
            col = sheet.col_values(i+1)
            col.pop(0)
            return col
    return 'There is no such category '+str(category)

#A more sophisticated version of the function above 
def getValuesFromCategories(*args,sheetname):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    row = sheet.row_values(1) 
    col = sheet.col_values(1)
    categories = args
    data = [] 
    for a in range(len(categories)):
        for i in range(len(row)):
            if row[i] == categories[a]:
                col = sheet.col_values(i+1)
                col.pop(0)
                data.append(col)
    return data 

#Gets the values from the Status sheet for the status function
def getValuesFromCategoriesStatus(sheetname):
    #scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    #creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    #client = gspread.authorize(creds)
    #sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    API_VERSION = 'v4'
    API_NAME = 'sheets'
    CLIENT_SECRET_FILE = 'creds.json'
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    sheet_id = getSheetIdWithName(sheetname)
    sheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    row = sheet.row_values(1) 
    col = sheet.col_values(1)
    categories = sheet.col_values(1)
    categories.pop(0)
    data = [] 
    #info = []
    for a in range(len(categories)):
        for i in range(len(col)):
            if col[i] == categories[a]:
                info = []
                row = sheet.row_values(i+1)
                info.append(categories[a])
                info.append('coordinates: ' + str(row[1])+','+str(row[2])+ '\nhp: '+ str(row[3]))
                data.append(info)
    return data 


def getItemList(sheetname,place):
    #Gets the value of an item in the first column at a certain place 
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    row = sheet.row_values(1)
    col = sheet.col_values(1)
    return col[place]

#Gets length of column of a certain sheet 
def colLength(sheetname,colnum):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    row = sheet.row_values(1)
    col = sheet.col_values(colnum)
    return len(col)

#Adds column to sheet 
def addColumn(list,sheetname,column):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetname).sheet1
    #data = sheet.get_all_records()
    row = sheet.row_values(1) 
    for item in list:
        col = sheet.col_values(column)
        sheet.update_cell(len(col)+1,column,str(item))

#Creates the base master info sheet Work in Progress
def createBaseMaster(name):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open(name).sheet1
    categories = ['object','continent','hp','xcoor','ycoor']
    sheet.insert_row(categories)

#Creates the base inventory
def createBaseInventory(name,continent):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open('Inventory-'+name).sheet1
    #data = sheet.get_all_records()
    categories = ['Continent','Budget','FootSoldiers']
    values1 = [continent,'300000']
    sheet.insert_row(values1)
    sheet.insert_row(categories)

#Creates the base status sheet 
def createBaseStatus(name,country):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open('Status-'+name).sheet1
    categories = ['object','xcoor','ycoor','hp']
    sheet.insert_row(categories)

#Adds any item to the inventory 
def addAny(continent,username,server_id):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    price = 5000
    inventory = client.open('Inventory-'+str(username)+'-'+str(server_id)).sheet1
    status = client.open('Status-'+str(username)+'-'+str(server_id)).sheet1
    Masterinfo = client.open('MasterInfo-'+str(server_id)).sheet1
    #data = sheet.get_all_records()
    row1 = inventory.row_values(1) 
    col2 = status.col_values(1)
    mastercol = Masterinfo.col_values(1)
    if int(price) > int(inventory.row_values(2)[1]):
        return False
    else: 
        inventory.update_cell(2,2,int(inventory.row_values(2)[1])-price)
        col1 = inventory.col_values(3)
        #col2 = status.col_values(a+1) 
        #print(len(col2))
        thingname = 'FootSoldiers-'+str(len(col1)+1)
        inventory.update_cell(len(col1)+1,3,thingname)
        status.update_cell(len(col2)+1,1,thingname)
        status.update_cell(len(col2)+1,4,100)
        status.update_cell(len(col2)+1,2,'h')
        status.update_cell(len(col2)+1,3,'h')
        Masterinfo.update_cell(len(mastercol)+1,1,thingname)
        Masterinfo.update_cell(len(mastercol)+1,2,continent)
        Masterinfo.update_cell(len(mastercol)+1,3,100)
        Masterinfo.update_cell(len(mastercol)+1,4,'h')
        Masterinfo.update_cell(len(mastercol)+1,5,'h')
                    #status.update_cell(len(col2)+1+i,5,thing)
        return True 

#Gets continent of username
def getContinent(username,server_id):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    inventory = client.open('PlayerList-'+str(server_id)).sheet1
    col = inventory.col_values(1)
    continents = inventory.col_values(2)
    for i in range(len(col)):
        if col[i] == username: 
            return continents[i]