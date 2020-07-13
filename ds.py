import discord
import datetime
import youtube_dl
import pyowm
import radio
import os
import requests
import config
from discord.ext import commands
from discord.utils import get
from time import sleep
from discord import utils
owm = pyowm.OWM('23e383b1f9723c91e85317b5e6a95c15', language="ru")
prefix = ":"
players = {}
client = commands.Bot(command_prefix=prefix)
client.remove_command( 'help' )
observation = owm.weather_at_place('Almaty,KZ')
w = observation.get_weather()
windy = w.get_wind()['speed']
tempash = w.get_temperature('celsius')['temp']
gradusov = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,26,27,28,29,30,35,36,37,38,39,40,45,46,47,48,49,50]
gradusa = [2,3,4,22,23,24,32,33,34,42,43,44]
gradus = [1,21,31,41]

@client.command(pass_context=True)
async def w(ctx):
    if tempash in gradusov:
        await ctx.channel.send('В городе ' + 'Алматы' + ' сейчас ' + w.get_detailed_status() + ',' + ' температура сейчас составляет - ' + str(tempash) + ' градусов' + ',' + "\n" + 'текущая скорость ветра = ' + str(windy) + ' км/ч' + '.')  
    if tempash in gradusa:
        await ctx.channel.send('В городе ' + 'Алматы' + ' сейчас ' + w.get_detailed_status() + ',' + ' температура сейчас составляет - ' + str(tempash) + ' градуса' + ',' + "\n" + 'текущая скорость ветра = ' + str(windy) + ' км/ч' + '.')   
    if tempash in gradus:
        await ctx.channel.send('В городе ' + 'Алматы' + ' сейчас ' + w.get_detailed_status() + ',' + ' температура сейчас составляет - ' + str(tempash) + ' градус' + ',' + "\n" + 'текущая скорость ветра = ' + str(windy) + ' км/ч'  + '.')
     
@client.event
async def on_ready():
    print( 'BOT connected' )
    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'работника' ) )

@client.command( pass_context = True )
async def c( ctx, amount = 100 ):
    await ctx.channel.purge( limit = amount )

@client.command( pass_context = True )
@commands.has_permissions( administrator = True )
async def k( ctx, amount : int, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.kick( reason = reason, )
    await ctx.send(f'kick user { member.mention }')
    await ctx.channel.purge( limit=amount )

@client.command( pass_context = True )
async def help( ctx ):
    emb = discord.Embed( title = 'Инструкция по командам' )
    emb.add_field( name = '{}c'.format ( prefix ), value = 'Очистка чата' )
    emb.add_field( name = '{}k'.format ( prefix ), value = 'Удаление участника (Только админ) ' )
    emb.add_field(name = '{}m'.format(prefix), value = 'слушать музыку')
    emb.add_field(name = '{}w'.format(prefix), value = 'показ погоды в алматы')
    emb.add_field(name = '{}s'.format(prefix), value = 'стоп музыки')
    emb.add_field(name = '{}p'.format(prefix), value = 'пауза музыки')
    emb.add_field(name = '{}r'.format(prefix), value = 'продолжение музыки')
    emb.add_field(name = '{}j'.format(prefix), value = 'присоединение бота к голосовому каналу только если вы там есть')
    emb.add_field(name = '{}l'.format(prefix), value = 'отсоединение от голосового канала')
    await ctx.send( embed = emb )
    await ctx.send( 'Все команды писать с префиксом  -  ":" ' )

@client.event
async def on_member_join( member ):
    channel = client.get_channel(707873874489901069)
    role = discord.utils.get(member.guild.roles, id=710101627838660660)
    await member.add_roles( role )
    await channel.send( embed = discord.Embed(description = f'Добро пожаловать на наш Discord сервер {member.name} чтобы получить другую роль зайдите в текстовой канал "получение-роли"', color = discord.Colour.blue) )

@client.command(pass_context=True)
async def j(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to (channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот подключился к каналу : {channel}')

@client.command(pass_context=True)
async def l(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await connect.channel()
        await ctx.send(f'Бот отсоединился от канала : {channel}')

@client.command(pass_context=True)
async def m(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
                                           
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus.so')
    
@client.command(pass_context = True)
async def p(ctx):
    id = ctx.message.server.id
    players[id].pause()
    
@client.command(pass_context = True)
async def s(ctx):
    id = ctx.message.server.id
    players[id].stop()
    
@client.command(pass_context = True)
async def r(ctx):
    id = ctx.message.server.id
    players[id].resume()

token = os.environ.get('BOT_TOKEN')

client.run(str(token))