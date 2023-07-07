import sys
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFilter,ImageColor
from logging import root
import os
import matplotlib
from sys import api_version 
from Google import Create_Service 
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from management import getFolderIdWithName
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io 
from management import * 
from sheets import * 
from googleapiclient.http import MediaIoBaseDownload
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import numpy as np
from os.path import exists
import random
#Gets the photo ID of the file in question 
def getPhotoId(name):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    response = service.files().list().execute() 
    folders = response.get('files')
    for i in folders:
        if i.get('name') == str(name)+'.png':
            id = i.get('id')
            return id 
    return "That doesn't exist"
    

#Waits until a function returns something, I don't think it works 
def waitUntil(condition, output): #defines function
    wU = True
    while wU == True:
        if condition: #checks the condition
            wU = False
            output

#Downloads a photo off the google drive 
def downloadPhoto(name):
    file_exists = os.path.exists(name + '.png')
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    file_id = getPhotoId(name)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO((name),'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    downloaded = False
    while done is False:
        status, done = downloader.next_chunk()
    filePath = open(name)   
    while downloaded == False: 
        if os.path.exists(name):
            downloaded = True 
            filePath = open(name)
    filePath.close()
    return True 

#Downloads the photo 
def downloadAndRenamePhoto(name,ending):
    waitUntil(downloadPhoto(name),os.replace(name,name+ending))


#Experimental command to place a soldier on an already downloaded map 
def placeSoldier(xcoor,ycoor,name):
    initialImage = Image.open(name+'.png')
    image1 = Image.new("RGBA", initialImage.size)
    image1.paste(initialImage) 
    pix = image1.load()
    print(pix[30,30])
    pix[xcoor,ycoor] = (245,40,145,0)
    image1.save(name+'.png')
    image1.close()


#Places the home base of the player on the map 
def placeHomeBasePlayer(xcoor,ycoor,name):
    filePath = open(name+'.png')
    initialImage = Image.open(name+'.png')
    image1 = Image.new("RGBA",initialImage.size)
    image1.paste(initialImage)
    pix = image1.load()
    pix[int(xcoor),int(ycoor)] = (13,13,13)
    pix[int(xcoor)+1,int(ycoor)] = (13,13,13)
    pix[int(xcoor)-1,int(ycoor)] = (13,13,13)
    pix[int(xcoor),int(ycoor)+1] = (13,13,13)
    pix[int(xcoor)+1,int(ycoor)+1] = (13,13,13)
    pix[int(xcoor)-1,int(ycoor)+1] = (13,13,13)
    image1.save(name+'.png')
    image1.close()
    return True 

#Generates a random x coordinate within a region 
def generateX(continent):
    if str(continent) == 'North America':
        return random.randrange(35,50)
    if str(continent) == 'South America':
        return random.randrange(55,70)
    if str(continent) == 'Europe':
        return random.randrange(110,125)
    if str(continent) == 'Asia':
        return random.randrange(140,165)
    if str(continent) == 'Africa':
        return random.randrange(95,115)
    if str(continent) == 'Oceania':
        return random.randrange(165,180)
    if str(continent) == 'Antarctica':
        return random.randrange(90,185)

#Generates a random y coordinate within a region 
def generateY(continent):
    if str(continent) == 'North America':
        return random.randrange(40,55)
    if str(continent) == 'South America':
        return random.randrange(75,100)
    if str(continent) == 'Europe':
        return random.randrange(30,45)
    if str(continent) == 'Asia':
        return random.randrange(25,60)
    if str(continent) == 'Africa':
        return random.randrange(58,70)
    if str(continent) == 'Oceania':
        return random.randrange(90,105)
    if str(continent) == 'Antarctica':
        return random.randrange(130,143)   

#Places the home bases within the actual world, universal map 
def placeHomeBaseWorld(xcoor,ycoor,name,continent):
    initialImage = Image.open(name+'.png')
    image1 = Image.new("RGBA",initialImage.size)
    image1.paste(initialImage)
    pix = image1.load()
    if str(continent) == 'North America':
        pix[int(xcoor),int(ycoor)] = (255,130,130)
        pix[int(xcoor)+1,int(ycoor)] = (255,130,130)
        pix[int(xcoor)-1,int(ycoor)] = (255,130,130)
        pix[int(xcoor),int(ycoor)+1] = (255,130,130)
        pix[int(xcoor)+1,int(ycoor)+1] = (255,130,130)
        pix[int(xcoor)-1,int(ycoor)+1] = (255,130,130)
    if str(continent) == 'South America':
        pix[int(xcoor),int(ycoor)] = (165,255,164)
        pix[int(xcoor)+1,int(ycoor)] = (165,255,164)
        pix[int(xcoor)-1,int(ycoor)] = (165,255,164)
        pix[int(xcoor),int(ycoor)+1] = (165,255,164)
        pix[int(xcoor)+1,int(ycoor)+1] = (165,255,164) 
        pix[int(xcoor)-1,int(ycoor)+1] = (165,255,164)
    if str(continent) == 'Europe':
        pix[int(xcoor),int(ycoor)] = (165,251,255)
        pix[int(xcoor)+1,int(ycoor)] = (165,251,255)
        pix[int(xcoor)-1,int(ycoor)] = (165,251,255)
        pix[int(xcoor),int(ycoor)+1] = (165,251,255)
        pix[int(xcoor)+1,int(ycoor)+1] = (165,251,255) 
        pix[int(xcoor)-1,int(ycoor)+1] = (165,251,255)
    if str(continent) == 'Africa':
        pix[int(xcoor),int(ycoor)] = (255,157,0)
        pix[int(xcoor)+1,int(ycoor)] = (255,157,0)
        pix[int(xcoor)-1,int(ycoor)] = (255,157,0)
        pix[int(xcoor),int(ycoor)+1] = (255,157,0)
        pix[int(xcoor)+1,int(ycoor)+1] = (255,157,0) 
        pix[int(xcoor)-1,int(ycoor)+1] = (255,157,0)
    if str(continent) == 'Asia':
        pix[int(xcoor),int(ycoor)] = (170,170,0)
        pix[int(xcoor)+1,int(ycoor)] = (170,170,0)
        pix[int(xcoor)-1,int(ycoor)] = (170,170,0)
        pix[int(xcoor),int(ycoor)+1] = (170,170,0)
        pix[int(xcoor)+1,int(ycoor)+1] = (170,170,0)
        pix[int(xcoor)-1,int(ycoor)+1] = (170,170,0)
    if str(continent) == 'Oceania':
        pix[int(xcoor),int(ycoor)] = (146,0,255)
        pix[int(xcoor)+1,int(ycoor)] = (146,0,255)
        pix[int(xcoor)-1,int(ycoor)] = (146,0,255)
        pix[int(xcoor),int(ycoor)+1] = (146,0,255)
        pix[int(xcoor)+1,int(ycoor)+1] = (146,0,255) 
        pix[int(xcoor)-1,int(ycoor)+1] = (146,0,255)
    if str(continent) == 'Antarctica':
        pix[int(xcoor),int(ycoor)] = (13,13,13)
        pix[int(xcoor)+1,int(ycoor)] = (13,13,13)
        pix[int(xcoor)-1,int(ycoor)] = (13,13,13)
        pix[int(xcoor),int(ycoor)+1] = (13,13,13)
        pix[int(xcoor)+1,int(ycoor)+1] = (13,13,13) 
        pix[int(xcoor)-1,int(ycoor)+1] = (13,13,13)
    image1.save(name+'.png')
    image1.close()
    return True 

#Places the bases
def placeBases(xcoor,ycoor,name):
    initialImage = Image.open(name+'.png')
    image1 = Image.new("RGBA",initialImage.size)
    image1.paste(initialImage)
    pix = image1.load()
    pix[int(xcoor),int(ycoor)] = (84,48,53)
    pix[int(xcoor)+1,int(ycoor)] = (84,48,53)
    pix[int(xcoor)-1,int(ycoor)] = (84,48,53)
    pix[int(xcoor),int(ycoor)+1] = (84,48,53)
    pix[int(xcoor)+1,int(ycoor)+1] = (84,48,53)
    pix[int(xcoor)-1,int(ycoor)+1] = (84,48,53)
    image1.save(name+'.png')
    image1.close()
    return True 


#Uploads image to the drive
def upload(name,parent):
    done = False
    SCOPES = ['https://www.googleapis.com/auth/drive']
    folder_id = getFolderIdWithName(parent)
    #creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    drive = Create_Service('creds.json','drive', 'v2', SCOPES)
    new_parent = {
        'id': str(folder_id)
    }
    filePath = open(name+'.png')
    image_id = getPhotoId(name)
    if image_id == "That doesn't exist":
        file_metadata = {'title': name+'.png'}
        media = MediaFileUpload(name+'.png',
                            mimetype='image/png')
        file = drive.files().insert(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        image_id = file.get('id')
        parent = drive.parents().insert(fileId = str(image_id), body=new_parent).execute()
        filePath.close()
        return True 
    else:
        deleted = drive.files().delete(fileId = image_id).execute()
        file_metadata = {'title': name+'.png'}
        media = MediaFileUpload(name+'.png',
                            mimetype='image/png')
        file = drive.files().insert(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        image_id = file.get('id')
        parent = drive.parents().insert(fileId = str(image_id), body=new_parent).execute()
        filePath.close()
        return True

    
#uploads image under new name to the drive
def uploadNewName(name,newname,parent):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    folder_id = getFolderIdWithName(parent)
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    drive = Create_Service('creds.json','drive', 'v2', SCOPES)
    new_parent = {
        'id': str(folder_id)
    }
    filePath = open(name+'.png')
    image_id = getPhotoId(name)
    if image_id == "That doesn't exist":
        file_metadata = {'title': newname+'.png'}
        media = MediaFileUpload(name+'.png',
                            mimetype='image/png')
        file = drive.files().insert(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        image_id = file.get('id')
        parent = drive.parents().insert(fileId = str(image_id), body=new_parent).execute()
        filePath.close()
        return True 
    else:
        deleted = drive.files().delete(fileId = image_id).execute()
        file_metadata = {'title': newname+'.png'}
        media = MediaFileUpload(name+'.png',
                            mimetype='image/png')
        file = drive.files().insert(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        image_id = file.get('id')
        parent = drive.parents().insert(fileId = str(image_id), body=new_parent).execute()
        filePath.close()
        return True 
    return 

#plots the image using matplotlib
def plotImage(imagename):
    img = mpimg.imread(imagename + '.png')
    imgplot = plt.imshow(img,interpolation='nearest')
    x = 200
    y = 143 
    plt.xticks(np.arange(0, x, 10))
    plt.yticks(np.arange(0, y, 10))
    plt.xlabel('x-axis (max 200)')
    plt.ylabel('y-axis (max 143)')
    plt.savefig(imagename + "plotted.png")
    plt.close()
    return True 

#plots the image and then zooms in on the specified coordinate 
def plotImageZoom(imagename,zoomx,zoomy):
    img = mpimg.imread(imagename + '.png')
    imgplot = plt.imshow(img,interpolation='nearest')
    x = 200
    y = 143 
    limx = int(zoomx) + 20
    limy = int(zoomy) + 20
    plt.xticks(np.arange(0, x, 10))
    plt.yticks(np.arange(0, y, 10))
    plt.xlabel('x-axis (max' + str(limx)+')')
    plt.ylabel('y-axis (max' + str(limy)+')')
    plt.xlim(limx - 40, limx)
    plt.ylim(limy, limy - 40)
    plt.savefig(imagename + "plotted.png")
    plt.close() 
    return True 

#90% working soldier scouting function, has bugs that I didn't have time to fix but it is able to find trajectory of where soldier would walk and then 
# return a list of all the enemies the soldier found and killed    
def placeNewSoldierProto(server_id, username,imagename,xcoor,ycoor):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open('Inventory-'+str(username) + '-' + str(server_id)).sheet1
    status = client.open('Status-'+str(username)+'-'+str(server_id)).sheet1
    Masterinfo = client.open('MasterInfo-'+str(server_id)).sheet1 
    col = sheet.col_values(1)
    statcol = status.col_values(1)
    xcol = status.col_values(2)
    hit = False 
    exists = False
    for i in range(len(xcol)):
        if xcol[i] == 'h':
            exists = True 
    if len(statcol) == 1: 
        return False 
    elif exists == False: 
        return False
    downloadAndRenamePhoto(imagename, ".png")
    filePath = open(imagename+'.png')
    initialImage = Image.open(imagename+'.png')
    image1 = Image.new("RGBA",initialImage.size)
    image1.paste(initialImage)
    continent = col[1]
    basex = int(col[2])
    basey = int(col[3])
    pix = image1.load()
    diffx = int(xcoor) - int(basex)
    diffy = int(ycoor) - int(basey)
    found = [] 
    xcol = Masterinfo.col_values(4)
    ycol = Masterinfo.col_values(5)
    cont = Masterinfo.col_values(2)
    for b in range(0,abs(diffy)+1):
        for c in range(0,int(abs(diffx)/abs(diffy))+1):
            if diffy < 0: 
                y = basey - b
            else: 
                y = basey + b 
            if diffx < 0: 
                x = basex + (b*int(diffx/abs(diffy)))-c 
            else:
                x = basex + (b*int(diffx/abs(diffy)))+c
            if pix[x,y] == (255,130,130) or pix[x,y] == (165,255,164) or pix[x,y] == (165,251,255) or pix[x,y] == (255,157,0) or pix[x,y] == (170,170,0) or pix[x,y] == (146,0,255) or pix[x,y] == (13,13,13):
                found.append(str(x) + ',' + str(y))
                if c == int(abs(diffx)/abs(diffy)) and b == abs(diffy):
                    for i in range(len(xcol)): 
                        if xcol[i] == x and ycol[i] == y:
                            for i in range(len(col)):
                                if 'FootSoldiers' in col[i] and xcol[i] == 'h':
                                    status.update_cell(i+1,2,str(x))
                                    status.update_cell(i+1,3,str(y)) 
                            target = cont[i]
                            targetinv = client.open('Inventory-'+str(target)+str(server_id)).sheet1
                            money = targetinv.col_values(2)
                            targetmoney = money[1] - 50000 - (len(found)*300)
                            targetinv.update_cell(2,2,targetmoney)
                            money = targetinv.col_values(2)
                            if money[1] <= 0: 
                                return str(target) + ' has LOST!!'
            else: 
                for i in range(len(col)):
                    if 'FootSoldiers' in col[i] and xcol[i] == 'h':
                        status.update_cell(i+1,2,str(x))
                        status.update_cell(i+1,3,str(y))
    return found  
            #pix[x,y] = (255,255,255)
    #for i in range(len(found)):
        
    print(str(found))
    
    image1.save(imagename + 'testing.png')
    filePath.close()
    