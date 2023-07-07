from logging import root
import os
from sys import api_version 
from Google import Create_Service 
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

#Creates folder with certain name 
def createFolder(name):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    service.files().create(body = file_metadata).execute()

#Creates a folder under a certain parent 
def createFolderComp(name,parent):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    file_metadata = {
        'name': name+'-'+parent,
        'parents': [str(getFolderIdWithName(parent))],
        'mimeType': 'application/vnd.google-apps.folder',
    }
    service.files().create(body = file_metadata).execute()

#Creates a sheet under a parent 
def createSheet(name,parent):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    folder_id = getFolderIdWithName(parent)
    #creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = Create_Service('creds.json','drive', 'v2',SCOPES)
    file1_metadata = {
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'title': str(name),
    }
    new_parent = {
        'id': str(folder_id)
    }
    domain_permission = {
        'value':'wump-506@world-war-wumpus.iam.gserviceaccount.com',
        'type': 'user',
        'role': 'writer',
    }
    res1 = service.files().insert(body=file1_metadata).execute()
    sheet1_id = res1.get('id')
    givePermission1 = service.permissions().insert(fileId=str(sheet1_id), body=domain_permission, fields="id",sendNotificationEmails = False).execute()
    parent1 = service.parents().insert(fileId = str(sheet1_id), body=new_parent).execute()

#Example and template I was using early on 
def createBaseSheetsEXAMPLE():
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    #Blank Spreadsheet File 
    playerListOpt = {
        'properties': {
            'title': 'PlayerList'
        }
    }
    playerList = service.spreadsheets().create(body = playerListOpt,fields='spreadsheetId').execute()

#Same thing 
def folderEXAMPLE():
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'").execute()
    folders = response.get('files')
    print(folders[0].get('id'))

#Gets the folder Id of a named folder 
def getFolderIdWithName(name):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'").execute()
    folders = response.get('files')
    for i in range(len(folders)):
        if str(folders[i-1].get('name')) == str(name):
            return folders[i-1].get('id')

#Gets the id of a named sheet 
def getSheetIdWithName(name):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    response = service.files().list(q="mimeType = 'application/vnd.google-apps.spreadsheet'").execute()
    sheets = response.get('files')
    for i in range(len(sheets)):
        if str(sheets[i-1].get('name')) == str(name):
            return sheets[i-1].get('id')

#creates base sheets for the players 
def createBaseSheets(name):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    folder_id = getFolderIdWithName(name)
    #creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    drive = Create_Service('creds.json','drive', 'v2', SCOPES)
    file1_metadata = {
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'title': 'PlayerList-'+str(name),
    }
    new_parent = {
        'id': str(folder_id)
    }
    file2_metadata = {
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'title': 'CountriesPicking-'+str(name),
    }
    file3_metadata = {
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'title': 'MasterInfo-'+str(name),
    }
    domain_permission = {
        'value':'wump-506@world-war-wumpus.iam.gserviceaccount.com',
        'type': 'user',
        'role': 'writer',
    }
    res1 = drive.files().insert(body=file1_metadata).execute()
    res2 = drive.files().insert(body=file2_metadata).execute()
    res3 = drive.files().insert(body=file3_metadata).execute()
    sheet2_id = res2.get('id')
    sheet1_id = res1.get('id')
    sheet3_id = res3.get('id')
    givePermission1 = drive.permissions().insert(fileId=str(sheet1_id), body=domain_permission, fields="id",sendNotificationEmails = False).execute()
    givePermission2 = drive.permissions().insert(fileId=str(sheet2_id), body=domain_permission, fields="id",sendNotificationEmails = False).execute()
    givePermission3 = drive.permissions().insert(fileId=str(sheet3_id), body=domain_permission, fields="id",sendNotificationEmails = False).execute()
    parent1 = drive.parents().insert(fileId = str(sheet1_id), body=new_parent).execute()
    parent2 = drive.parents().insert(fileId = str(sheet2_id), body=new_parent).execute()
    parent3 = drive.parents().insert(fileId = str(sheet3_id), body=new_parent).execute()

#deletes a folder of a certain name 
def deleteFolder(foldername): 
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    file_id = getFolderIdWithName(foldername)
    service.files().delete(fileId=file_id).execute()
