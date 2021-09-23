import discord
from discord import channel
from discord.ext import commands
import random
from cooldown import cooldown
from tools import openfile,checklink,triggeredC,checklinkonfile,pF,callwrite,hmarkf,lmarkf,LoadUsers,cUSD,dmark,showf
from discord.ext import tasks
from itertools import cycle


client = commands.Bot(command_prefix = '.')

client.remove_command('help')

less_cooldown = 300
full_cooldown = 3600
med_cooldown = 1800

@tasks.loop(seconds=30)
async def checkcmc():
    usersmarks = LoadUsers()

    for key in usersmarks.keys():
        key2 = str(key)
        print(key2)
        rank,price,change1,change24 = cUSD(key2)
        values = usersmarks[key]

        for v in values:
            v2 = v.split("_")
            
            channel = client.get_channel(int(v2[4]))
            v2[2] = int(v2[2])
            if v2[3] == "higher":
                if price >= v2[2]:
                    await dmark(None,v2[1],v2[2],v2[0])
                    await channel.send(f"{v2[5]} Notification Triggered ! \n {v2[1]} Price got higher than: {v2[2]} USD")
                    
            else:
                if price <= v2[2]:
                    await dmark(None,v2[1],v2[2],v2[0])
                    await channel.send(f"{v2[5]} Notification Triggered  ! \n {v2[1]} Price got lower than: {v2[2]} USD")


status1 = cycle(["on","off"])
status2 = cycle(["on","off"])

async def mark(ctx,lh,moeda=None,preco=None):
    if moeda == None or preco == None:
        await ctx.send("faltou alguma coisa seu mongol")
    else:
        if moeda != "miota" and moeda != "btc" :
            await ctx.send("apenas miota ou btc mongoloide")
        else:
            channel = discord.utils.get(ctx.guild.channels, name=str(ctx.message.channel))
            channel_id = channel.id
            if lh == "l" :
        
               await lmarkf(ctx,channel_id,moeda,preco,str(ctx.message.author),ctx.author.mention)
            else:
                await hmarkf(ctx,channel_id,moeda,preco,str(ctx.message.author),ctx.author.mention)

@client.command()
async def setC(ctx):

    if str(ctx.message.author.id) == 260444527779643402 :
        x = next(status2)
        print(f"check task: {x}")
        if x == "on" :
            await checkcmc.start()
        else:
            await checkcmc.stop()

    else:
        await ctx.send(content="You don't have the enough power to do that",delete_after=5)


@client.event
async def on_ready():
    print('Bot is Ready.')

@client.command()
async def help(ctx):
    guild = str(ctx.message.channel.guild)
    channel = str(ctx.message.channel)
    
    response = cooldown(channel,guild,'h','help')
    if response == "ok_send":

        await ctx.send('```Hi this is the spec bot, feel free to use any of these commmands:\n\n.p: Shows iota price and ranking\n.meme: summons a random iota meme made by the spec community.\n\n.donate: Did you like the bot? Feel free to donate to help incentivize me to create more commands options (= ```')   
    elif response == "send_with_message":
        await ctx.send('```Hi this is the spec bot, feel free to use any of these commmands:\n\n.p: Shows iota price and ranking\n.meme: summons a random iota meme made by the spec community.\n\n.donate: Did you like the bot? Feel free to donate to help incentivize me to create more commands options (= ```')
    else: 
        await triggeredC(ctx,response)

@client.command()
async def nhelp(ctx):
    guild = str(ctx.message.channel.guild)
    channel = str(ctx.message.channel)
    
    response = cooldown(channel,guild,'h','help')
    if response == "ok_send":

        await ctx.send('```.hmark: Marca uma notificação acima do preço atual \n .lmark: marca uma notificação abaixo do preço atual \n .show: mostra notificações marcadas ativas \n .deln: deleta notificação  \n ```')
    elif response == "send_with_message":
        await ctx.send('```.hmark: Marca uma notificação acima do preço atual \n .lmark: marca uma notificação abaixo do preço atual \n .show: mostra notificações marcadas ativas \n .deln: deleta notificação  \n ```')
    else: 
        await triggeredC(ctx,response)

@client.command()
async def donate(ctx):
    guild = str(ctx.message.channel.guild.id)
    channel = str(ctx.message.channel.id)
    
    response = cooldown(channel,guild,'o','donate')
    if response == "ok_send":
        await ctx.send('```iota1qrgfnrrd908upkkucucapemk7n2hy3dcvwxv9kx63uv4pj88w6t0v48v7jh```')
    elif response == "send_with_message":
        await ctx.send('```iota1qrgfnrrd908upkkucucapemk7n2hy3dcvwxv9kx63uv4pj88w6t0v48v7jh```')   
    else: 
        await triggeredC(ctx,response)

@client.command()
async def p(ctx,arg=None,arg2=None):
    guild = str(ctx.message.channel.guild)
    channel = str(ctx.message.channel)
    
    response = cooldown(channel,guild,"pc",'p')
    if response == "ok_send" or response == "send_with_message":
        await pF(ctx,arg,arg2)
        
    else: 
        await triggeredC(ctx,response)

@client.command()
async def lmark(ctx,moeda=None,preco=None):
    
   await mark(ctx,'l',moeda,preco)

@client.command()
async def hmark(ctx,moeda=None,preco=None):
    
   await mark(ctx,"h",moeda,preco)


@client.command()
async def deln(ctx,moeda=None,preco=None):
    if moeda == None or preco == None:
        await ctx.send("faltou alguma coisa seu mongol")
    
    elif moeda == "miota" or moeda == "btc" :
       await dmark(ctx,moeda,preco,str(ctx.message.author))

    else:
        await ctx.send("apenas miota ou btc mongoloide")
       

@client.command()
async def show(ctx):
    user = ctx.message.author
    await showf(ctx,user)
   
@client.command()
async def price(ctx):
    await pF(ctx)

@client.command()
async def whereismyfuckinmoney(ctx):
    await pF(ctx)

@client.command()
async def whereisourfuckinmoney(ctx):
    await pF(ctx)

@client.command()
async def meme(ctx):
    guild = str(ctx.message.channel.guild.id)
    channel = str(ctx.message.channel.id)
    response = cooldown(channel,guild,'g','meme')
    randnumb = random.randint(1,222)
    if response == "ok_send" or response == "send_with_message" :
        await ctx.send(file=discord.File(f'./iotamemes/{randnumb}.jpg'))   
        
    else: 
        await triggeredC(ctx,response)         

client.run('Discord key')



