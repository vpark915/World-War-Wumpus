from operator import getitem
from unicodedata import category
from venv import create
import discord 
import random
import threading
import emoji 
import management
from management import *
from sheets import *
from photoeditor import *
from discord.ext import commands 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint 
from PIL import Image
import math 

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents)

@client.event 
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

@client.command() 
#Registers the server to the google sheet. Makes sure that people cant register twice  
async def register_server(ctx):
    server_id=ctx.message.guild.id
    if checkExisting(str(server_id),'Servers') == True:
        await ctx.send('Your server is already registered!')
    elif checkExisting(str(server_id),'Servers') == False:
        await ctx.send(str(ctx.message.author) + ' is the Game Master!')
        await ctx.send('Registering...')
        addCell(server_id,'Servers')
        createFolder(str(server_id))
        createBaseSheets(str(server_id))
        user = ctx.message.author
        await ctx.guild.create_role(name="Game Master",colour = discord.Colour(0xffffff))
        role = discord.utils.get(user.guild.roles, name="Game Master")
        await user.add_roles(role)
        await ctx.send('Your server is now registered!')

@client.command()
#Player uses command when wants to join the game. Joining the game gets your username added to playerlist 
async def join_game(ctx):
    server_id=ctx.message.guild.id
    await ctx.send("Processing...")
    if checkExisting(str(server_id),'Servers') == False:
        await ctx.send("A game hasn't been created yet!")
    elif checkExisting(str(ctx.message.author),'PlayerList-'+str(server_id)):
        await ctx.send('You have already been registered for this game!')
    else: 
        await ctx.guild.create_role(name="World Leaders",colour = discord.Colour(0xffffff))
        addCell(str(ctx.message.author),'PlayerList-'+str(server_id))
        user = ctx.message.author
        role = discord.utils.get(user.guild.roles, name="World Leaders")
        await user.add_roles(role)
        await ctx.send(str(ctx.message.author.display_name) + ' has joined the game!')

@client.command() 
#Starting the game sets up the discord and all the materials needed for the game to finish 
async def start_game(ctx):
    server_id=ctx.message.guild.id
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    for i in ctx.guild.by_category(): 
        if i[0].name == 'World War Wumpus':
            await ctx.send("A game is already in progress!")
            return 
    if checkExisting(str(server_id),'Servers') == False:
        await ctx.send("A game hasn't been created yet!")
        return 
    for i in ctx.message.author.roles:
        if str(i.name) == "Game Master": 
            await ctx.send('Generating necessary assets...')
            await ctx.guild.create_category_channel("World War Wumpus")
            await ctx.guild.create_role(name="North America",colour = discord.Colour(0x053afa))
            await ctx.guild.create_role(name="South America",colour = discord.Colour(0xda32f0))
            await ctx.guild.create_role(name="Europe",colour = discord.Colour(0xf2fa07))
            await ctx.guild.create_role(name="Asia",colour = discord.Colour(0xfc2c19))
            await ctx.guild.create_role(name="Africa",colour = discord.Colour(0xfcbc19))
            await ctx.guild.create_role(name="Oceania",colour = discord.Colour(0x0c4f0c))
            await ctx.guild.create_role(name="Antarctica",colour = discord.Colour(0xaef9fc))
            NA = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='North America') : discord.PermissionOverwrite(read_messages=True)
            }
            SA = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='South America') : discord.PermissionOverwrite(read_messages=True)
            }
            EU = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='Europe') : discord.PermissionOverwrite(read_messages=True)
            }
            AS = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='Asia') : discord.PermissionOverwrite(read_messages=True)
            }
            AF = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='Africa') : discord.PermissionOverwrite(read_messages=True)
            }
            OCE = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='Oceania') : discord.PermissionOverwrite(read_messages=True)
            }
            ANT = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='Antarctica') : discord.PermissionOverwrite(read_messages=True)
            }
            DIP = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                discord.utils.get(ctx.guild.roles, name='World Leaders') : discord.PermissionOverwrite(read_messages=True)
            }
            for i in range(len(ctx.guild.categories)):
                if ctx.guild.categories[i].name == 'World War Wumpus':
                    await ctx.guild.create_text_channel('Diplomatic Talks',overwrites=DIP, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('North America', overwrites=NA, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('South America', overwrites=SA, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('Europe', overwrites=EU, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('Asia', overwrites=AS, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('Africa', overwrites=AF, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('Oceania', overwrites=OCE, category=ctx.guild.categories[i])
                    await ctx.guild.create_text_channel('Antarctica', overwrites=ANT, category=ctx.guild.categories[i])
            sheet1 = client.open('CountriesPicking-'+str(server_id)).sheet1
            sheet2 = client.open('PlayerList-'+str(server_id)).sheet1
            sheet3 = client.open('MasterInfo-'+str(server_id)).sheet1
            col2 = sheet2.col_values(1)
            continents = ['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Oceania']
            addColumn(continents, 'CountriesPicking-'+str(server_id),1)
            uploadNewName('basedpixelmapplotted','pixelmap-'+str(server_id)+'plotted',server_id)
            uploadNewName('basedpixelmap','pixelmap-'+str(server_id),str(server_id))
            for i in range(colLength('PlayerList-'+str(server_id),1)):
                col1 = sheet1.col_values(1)
                await ctx.send(emoji.demojize('🎲'+str(getItemList('PlayerList-'+str(server_id),i)) +' is now rolling for their Continent🎲'))
                picked = False 
                while picked == False:
                    playerCont = continents[random.randrange(0,6)]
                    for a in range(len(col1)):
                        if(col1[a] == playerCont): 
                            sheet3 = client.open('MasterInfo-'+str(server_id)).sheet1
                            picked = True
                            sheet1.update_cell(a+1,1,"changed")
                            sheet2.update_cell(i+1,2,str(playerCont))
                            randomX = int(generateX(playerCont))
                            randomY = int(generateY(playerCont))
                            createFolderComp(col2[i],str(server_id))
                            createSheet('Inventory-'+col2[i]+'-'+str(server_id),col2[i]+'-'+str(server_id))
                            createSheet('Status-'+col2[i]+'-'+str(server_id),col2[i]+'-'+str(server_id))
                            createBaseInventory(str(col2[i])+'-'+str(server_id),str(playerCont))
                            createBaseStatus(str(col2[i])+'-'+str(server_id),str(playerCont))
                            sheet4 = client.open('Inventory-'+col2[i]+'-'+str(server_id)).sheet1
                            sheet4.update_cell(3,1,str(randomX))
                            sheet4.update_cell(4,1,str(randomY))
                            uploadNewName('basedpixelmap','pixelmap-'+str(server_id)+'-'+str(col2[i]),str(col2[i])+'-'+str(server_id))
                            uploadNewName('basedpixelmapplotted','pixelmap-'+str(server_id)+'-'+str(col2[i])+'plotted',str(col2[i])+'-'+str(server_id))
                            uploadNewName('basedpixelmap','pixelmap-'+str(server_id)+'-'+str(col2[i]) + '-background',str(col2[i])+'-'+str(server_id))
                            downloadAndRenamePhoto('pixelmap-'+str(server_id)+'-'+str(col2[i]),'.png')
                            downloadAndRenamePhoto('pixelmap-'+str(server_id),'.png')
                            downloadAndRenamePhoto('pixelmap-'+str(server_id)+'-'+str(col2[i])+'-background','.png')
                            waitUntil(placeHomeBaseWorld(randomX,randomY,'pixelmap-'+str(server_id),playerCont),plotImage('pixelmap-'+str(server_id)))
                            waitUntil(placeHomeBasePlayer(randomX,randomY,'pixelmap-'+str(server_id)+'-'+str(col2[i])),plotImage('pixelmap-'+str(server_id)+'-'+str(col2[i])))
                            upload('pixelmap-'+str(server_id),str(server_id))
                            upload('pixelmap-'+str(server_id)+'-'+str(col2[i]),str(col2[i])+'-'+str(server_id))
                            upload('pixelmap-'+str(server_id)+'plotted',str(server_id))
                            upload('pixelmap-'+str(server_id)+'-'+str(col2[i])+'plotted',str(col2[i])+'-'+str(server_id))
                            upload('pixelmap-'+str(server_id)+'-'+str(col2[i])+'-background',str(col2[i])+'-'+str(server_id))
                            Mastercol = sheet3.col_values(1)
                            sheet3.update_cell(len(Mastercol)+1,1,str(col2[i]))
                            sheet3.update_cell(len(Mastercol)+1,2,playerCont)
                            sheet3.update_cell(len(Mastercol)+1,3,'500')
                            sheet3.update_cell(len(Mastercol)+1,4,str(randomX))
                            sheet3.update_cell(len(Mastercol)+1,5,str(randomY))
                            """
                            os.remove('pixelmap-'+str(server_id)+'.png')
                            os.remove('pixelmap-'+str(server_id)+'-'+str(col2[i])+'.png')
                            """
                            role = discord.utils.get(ctx.message.author.guild.roles, name=str(playerCont))
                            username = str(col2[i])[:-5]
                            member = discord.utils.get(ctx.guild.members, name=username)
                            await member.add_roles(role)
                await ctx.send(str(col2[i])+' is ' + str(playerCont))
            os.remove('pixelmap-'+str(server_id)+'plotted.png')
            os.remove('pixelmap-'+str(server_id)+'.png')
            for i in range(colLength('PlayerList-'+str(server_id),1)):
                os.remove('pixelmap-'+str(server_id)+'-'+str(col2[i])+".png")
                os.remove('pixelmap-'+str(server_id)+'-'+str(col2[i])+'-background.png')
                os.remove('pixelmap-'+str(server_id)+'-'+str(col2[i])+'plotted.png')
            await ctx.send('Everyone has been assigned a country. Let the games begin!')
            print("process finished")  
            return 
    await ctx.send("You don't have the permissions to do that!")
           
@client.command()
#displays the map, the map can be displayed zoomed into a singular spot using the coordinate system 
async def display_map(ctx,*args):
    server_id = ctx.message.guild.id
    username = ctx.message.author
    embed1 = discord.Embed(title = "A Map From Your Perspective", description='.display_map <x> <y>\nYou can zoom into a specified x and y if you want to', colour = discord.Colour.purple())
    embed1.set_footer(text='Fueled from the sweat and tears of Vinnie Park')
    if len(args) == 0:
        downloadAndRenamePhoto('pixelmap-'+str(server_id)+'-'+str(username)+'plotted','.png') 
        image = Image.open('pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png')
        newimage = image.resize((1000,715),resample=Image.Dither.NONE)
        newimage.save('pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png')
        file = discord.File('pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png', 'pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png')
        embed1.set_image(url="attachment://"+'pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png')
    elif len(args) == 2: 
        xzoom = int(args[0])
        yzoom = int(args[1])
        #print(xzoom)
        #print(yzoom)
        downloadAndRenamePhoto('pixelmap-'+str(server_id)+'-'+str(username),'.png')
        image = Image.open('pixelmap-'+str(server_id)+'-'+str(username)+'.png')
        plotImageZoom('pixelmap-'+str(server_id)+'-'+str(username),xzoom,yzoom)
        newimage = image.resize((1000,715),resample=Image.Dither.NONE)
        newimage.save('pixelmap-'+str(server_id)+'-'+str(username)+'.png')
        file = discord.File('pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png', 'pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png')
        embed1.set_image(url="attachment://"+'pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png') 
        os.remove('pixelmap-'+str(server_id)+'-'+str(username)+'.png')
    embed2 = discord.Embed(title = "Base and Soldiers", colour = 0x0d0d0d)
    await ctx.send(file=file,embed=embed1)
    await ctx.send(embed=embed2)
    os.remove('pixelmap-'+str(server_id)+'-'+str(username)+'plotted.png')

@client.command()
#Initial bot testing commands from the very beginning
async def ping(ctx):
    server_id=ctx.message.guild.id
    print(client.get_guild(server_id).members)
    await ctx.send('Pong!')

@client.command() 
async def reset_everything(ctx):
    #Help for clearing everything after I have tested a feature 
    server_id = ctx.message.guild.id
    roleList = ctx.guild.roles 
    channelList = ctx.guild.by_category()
    contains = True
    num = len(ctx.guild.roles)
    for i in channelList:
        if i[0].name == 'World War Wumpus':
            channels = i[1]
            for a in channels:
                await a.delete()
            await i[0].delete()
    while contains == True:
        if num == 0:
            contains = False
        if str(ctx.guild.roles[num-1].name) != 'World War Wumpus' and str(ctx.guild.roles[num-1].name) != str(ctx.guild.default_role.name):
            await ctx.guild.roles[num-1].delete()
        num -= 1    
    deleteFolder(server_id)
    await ctx.send("I have reset the roles and channels")


@client.command()
#non operational, meant for a future build if people were to be able to set up their own settings.
async def rules(ctx):
    embed=discord.Embed(
    title=emoji.demojize("🎖️Current Rules🎖️"),
        description='These are the current rules for World War Wumpus',
        color=discord.Color.red(),
        inline=True)
    embed.add_field(name="Peace Timer", value="3 days", inline=True)
    embed.add_field(name="Funds Timer", value="3 days", inline=True)
    embed.add_field(name="Funds Amount", value="$100,000", inline=True)

    embed.add_field(name="Starting Budget", value="$2,000,000", inline=True)
    embed.add_field(name="Countries", value="All", inline=True)
    embed.set_footer(text="Created by Vinnie Park")
    await ctx.send(embed=embed)
    
@client.command()
#command that will help people get familiarized with their commands
async def help_commands(ctx):
    embed=discord.Embed(
    title=emoji.demojize("🤖Commands🤖"),
        description="Here's a list of some helpful commands",
        color=discord.Color.red(),
        inline=True)
    embed.add_field(name=".help_commands", value="Gives a list of all commands", inline=False)
    embed.add_field(name=".inventory", value="Gives you your inventory", inline=False)
    embed.add_field(name=".status", value="Gives you stats", inline=False)
    embed.add_field(name=".transport_soldier <x> <y>", value="Transports soldier to a location on the map, soldier is planted there", inline=False)
    embed.add_field(name=".display_map <x> <y>", value="Displays map of your knowledge", inline=False)
    await ctx.send(embed=embed)

@client.command() 
#command that will spawn troops into your inventory and status, each has HP 
async def spawn(ctx,*args):
    await ctx.send("Processing Request...")
    server_id = ctx.message.guild.id
    username = ctx.message.author
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open('Inventory-'+str(username)+'-'+str(server_id)).sheet1
    if len(args) == 0: 
        await ctx.send(".spawn <thing> <number> . \nThings you can spawn:\nFoot Soldiers")
    elif len(args) == 1: 
        thing = args[0]
        if addAny(getContinent(username,server_id),username,server_id) == False: 
            await ctx.send("You do not have the funds")
        else: 
            await ctx.send("You have added 1 " + str(thing) + " to your arsenal")
  
@client.command()
#shows the inventory and what's in it 
async def inventory(ctx):
    username = ctx.message.author
    server_id = ctx.message.guild.id
    sheetname = 'Inventory-' + str(username) + '-' + str(server_id)
    inventory = getValuesFromCategories('Foot Soldiers', 'Medics', 'Airplanes', 'Tanks', 'Naval Ships',sheetname=sheetname)
    embed=discord.Embed(title='Your Current Inventory', description="A list of your current military assets", color=discord.Color.red(),inline = False)
    for i in range(len(inventory)):
        if i == 0: 
            embed.add_field(name='Soldiers', value=str(inventory[i]),inline = False)
        if i == 1: 
            embed.add_field(name='Medics', value=str(inventory[i]),inline = False)
        if i == 2: 
            embed.add_field(name='Airplanes', value=str(inventory[i]),inline = False)
        if i == 3: 
            embed.add_field(name='Tanks', value=str(inventory[i]),inline = False)
        if i == 4: 
            embed.add_field(name='Naval Ships', value=str(inventory[i]),inline = False)
    await ctx.send(embed=embed)

@client.command()
#shows the status and current state of your troops, location, health, etc. 
async def status(ctx):
    username = ctx.message.author
    server_id = ctx.message.guild.id 
    sheetname = 'Status-' + str(username) + '-' + str(server_id)
    status = getValuesFromCategoriesStatus(sheetname)
    embed=discord.Embed(title='All Status of Items', description="A list of your current military assets", color=discord.Color.red(),inline = False)
    for i in range(len(status)):
        embed.add_field(name=status[i][0], value=status[i][1])
    await ctx.send(embed=embed)


@client.command()
#Doesn't work as google drive API stopped working and halted my progress with this feature, meant to provide user with ability to 
#scout out area and attack enemy troops 
async def transport_soldier(ctx,coordx,coordy):
    #display_map(ctx)
    username = ctx.message.author
    server_id = ctx.guild.id
    embed=discord.Embed(
    title=emoji.demojize("Transport"),
        description="Details about where you will transport your troop",
        color=discord.Color.red(),
        inline=True)
    embed.add_field(name=".transport_soldier <coordx> <coordy>", value="How many troops, where you'll transport. Takes the troops closest to home base", inline=False) 
    placeNewSoldierProto(server_id,username,"pixelmap-" + str(server_id),coordx,coordy)  
    await ctx.send(embed=embed)



@client.command()
#Future command that will enable you to make scouting posts 
async def posts(ctx):
    embed=discord.Embed(
    title=emoji.demojize("Posts"),
        description="Details about where and what your soldiers will spy",
        color=discord.Color.red(),
        inline=True)
    embed.add_field(name="<coordinates> <type>", value="Where you will set up a post and what type", inline=False)
    await ctx.send(embed=embed)

@client.command() 
#Future command that will allow you to trade troops for money with other players 
async def trade(ctx):
    embed=discord.Embed(
    title=emoji.demojize("Trading"),
        description="Details about how you'll trade with other countries",
        color=discord.Color.red(),
        inline=True)
    embed.add_field(name="Offers Received", value="Offers to you will appear here", inline=False)
    embed.add_field(name="Offers Sent", value="Offers sent to others will appear here", inline=False)
    embed.add_field(name="<country> <type of offer> <amount> <type of receive> <amount>", value="Who you're trading with, what you'll trade, what you'll get in return", inline=False)
    await ctx.send(embed=embed)


client.run('OTcwODg2OTkzMDE1ODg1OTA1.YnCe-Q.2cwenIPopx1BSoz-uk9ORE_b1es')