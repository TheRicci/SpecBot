import asyncio
import re
from bs4 import BeautifulSoup
import requests
import discord
from datetime import datetime, timedelta  
from cooldown import cooldown
import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pickle

def cUSD(arg):
    arg = arg.upper()

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
        'symbol':f'{arg}',
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'CMC KEY',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    try:
        rank = data["data"][f"{arg}"]["cmc_rank"]
        price = data["data"][f"{arg}"]["quote"]["USD"]["price"]
        change1 = data["data"][f"{arg}"]["quote"]["USD"]["percent_change_1h"]
        change24 = data["data"][f"{arg}"]["quote"]["USD"]["percent_change_24h"]    
    except KeyError:
        return("a")

    return (rank,price,change1,change24)

async def hmarkf(ctx,ch,moeda,preco,user,user2):

    try:
        users = LoadUsers()
    except EOFError:
        users = {}

    try:
        users[f"{moeda}"].append(f"{user}_{moeda}_{preco}_higher_{ch}_{user2}")
    except KeyError:
        users[f"{moeda}"] = [f"{user}_{moeda}_{preco}_higher_{ch}_{user2}"]

    SaveUsers(users)
            
    await ctx.send("notification saved.")

async def lmarkf(ctx,ch,moeda,preco,user,user2):
    try:
        users = LoadUsers()
    except EOFError:
        users = {}

    try:
        users[f"{moeda}"].append(f"{user}_{moeda}_{preco}_lower_{ch}_{user2}")
    except KeyError:
        users[f"{moeda}"] = [f"{user}_{moeda}_{preco}_lower_{ch}_{user2}"]

    SaveUsers(users)
            
    await ctx.send("notification saved.")

async def dmark(ctx,moeda,preco,user,):
    
    usersmark = LoadUsers()
    
    for l in usersmark.values():

        for v in l:
            if f"{user}_{moeda}_{preco}" in v :
                l.remove(v)
                SaveUsers(usersmark)

                if ctx != None:
                    await ctx.send("notification deleted")
                    break
            
async def showf(ctx,user):

    usersmark = LoadUsers()
    
    for l in usersmark.values():
        
        for v in l:
            
            if f"{user}" in v :
                data = v.split("_")
                await ctx.send(f"Moeda: {data[1]}, Preço: {data[2]}, Mark: {data[3]}")
                

def LoadUsers():
    a_file = open("usersmark.txt", "rb")
    output = pickle.load(a_file)
    a_file.close()
    return(output)

def SaveUsers(usersmarks):
    a_file = open("usersmark.txt", "wb")
    pickle.dump(usersmarks, a_file)
    a_file.close()        
        
async def pF(ctx,arg,arg2,time=None):
    if arg == None:

        rank,price,change1,change24 = iota()

        retStr = f"```24h change: {round(change24,2)}% \n 1h change: {round(change1,2)}%```"

        if float(change24) > 0: 
            embed = discord.Embed(title=f"IOTA #{rank}",colour=32768)

        else:
            embed = discord.Embed(title=f"IOTA #{rank}",colour=9568256)

        embed.add_field(name=f"${round(price,4)} USD",value=retStr)
    
        if time == None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed,delete_after=600)

    elif arg2 == None:
        try:
            rank,price,change1,change24 = cUSD(arg)
        except ValueError:
            await ctx.send("Coin not found")
            pass

        retStr = f"```24h change: {round(change24,2)}% \n 1h change: {round(change1,2)}%```"

        if float(change24) > 0: 
            embed = discord.Embed(title=f"{arg} #{rank}",colour=32768)

        else:
            embed = discord.Embed(title=f"{arg} #{rank}",colour=9568256)

        embed.add_field(name=f"${round(price,3)} USD",value=retStr)

        await ctx.send(embed=embed)
    
    else:
        
        rank,price,change1,change24 = cUSD(arg)

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

        parameters = {
            'symbol':f'{arg}',
            'convert':f'{arg2}'
        }

        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'CMC KEY',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        
        arg = arg.upper()
        arg2 = arg2.upper()

        pricearg = data["data"][f"{arg}"]["quote"][f"{arg2}"]["price"]
        change1arg = data["data"][f"{arg}"]["quote"][f"{arg2}"]["percent_change_1h"]
        change24arg = data["data"][f"{arg}"]["quote"][f"{arg2}"]["percent_change_24h"]

        retStr = f"```24h change: {round(change24,2)}% \n 1h change: {round(change1,2)}%```"
        retStrArg = f"```24h change: {round(change24arg,2)}% \n 1h change: {round(change1arg,2)}%```"

        if float(change24) > 0: 
            embed = discord.Embed(title=f"{arg} #{rank}",colour=32768)

        else:
            embed = discord.Embed(title=f"{arg} #{rank}",colour=9568256)

        embed.add_field(name=f"${round(price,4)} USD",value=retStr)
        embed.add_field(name=f"{pricearg:.8f} {arg2}",value=retStrArg) 

        await ctx.send(embed=embed)


def iota():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
        'slug':'iota',
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'CMC KEY',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    rank = data["data"]["1720"]["cmc_rank"]
    price = data["data"]["1720"]["quote"]["USD"]["price"]
    change1 = data["data"]["1720"]["quote"]["USD"]["percent_change_1h"]
    change24 = data["data"]["1720"]["quote"]["USD"]["percent_change_24h"]

    return (rank,price,change1,change24)

def openfile(filename):
    with open(filename) as f:
        data = f.readline()
        return(data.split(',')) 

async def callwrite(user,name):
    my_file = open("calls.txt", "a")
    user = user
    my_file.write(f'{name}_{user} {datetime.now()},')
    my_file.close()
    

def checklink(link):
    check = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', link)
    return check

def checknone(arg):
    if arg == None:
        return "pic"
    else:
        return arg

async def triggeredC(ctx,response):
    if response == "nop":
        asyncio.sleep(2)
        await ctx.message.delete()
        await ctx.send(delete_after=3,content=f"Command not allowed here")
    else:
        asyncio.sleep(2)    
        await ctx.message.delete()
        await ctx.send(delete_after=3,content=f"You are on cooldown. wait for {response} minutes")

def checklinkonfile(link,file):
    links = openfile(file)
    if link in links:
        return "okay2"
    else:
        return "okay"


