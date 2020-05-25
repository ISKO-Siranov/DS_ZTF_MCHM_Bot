import discord
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import pyowm
import radio

import os
from time import sleep
import requests

prefix = '>'

client = commands.Bot(command_prefix=prefix)
client.remove_command( 'help' )

hello_words = ['hello','Hello','hi','Hi','привет','Привет',]
question = ['что ты умеешь?','че ты умеешь?','что здесь делать?','че здесь делать?']

@client.command(pass_context=True)
async def weather(ctx):
    owm  =  pyowm.OWM ( '23e383b1f9723c91e85317b5e6a95c15', language = "ru" )
    
    city = 'В каком городе узнать погоду??'
    
    await ctx.channel.send(city)
    
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    tempa = get_temperature('celsius')['temp']
    windy = get_wind()['speed']
    vlazhnost = get_humidity()['87']
    
    await ctx.channel.send( 'В городе ' + city + ' сейчас ' + w + ' температура сейчас ' + tempa + ',' + ' скорость ветра состовляет = ' + windy + ',' + ' также текущая влажность = ' + vlazhnost )
    
@client.event

async def on_ready():
    print( 'BOT connected' )

    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'server' ) )

@client.command( pass_context = True )

async def clear( ctx, amount = 100 ):
    await ctx.channel.purge( limit = amount )

@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, amount : int, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason, )
    await ctx.send(f'kick user { member.mention }')
    await ctx.channel.purge( limit=amount )

@client.event

async def on_message( message ):
    await client.process_commands( message )
    author = message.author
    msg = message.content.lower()

    if msg in hello_words:
        await message.channel.send(f' Здравствуйте {author.mention} чем могу быть полезен? ')
    if msg in question:
        await message.channel.send(f' {author.mention} для полной инфы пропишите команду - !help ')

@client.command( pass_context = True )

async def help( ctx ):
    emb = discord.Embed( title = 'Инструкция по командам' )

    emb.add_field( name = '{}clear'.format ( prefix ), value = 'Очистка чата' )
    emb.add_field( name = '{}kick'.format ( prefix ), value = 'Удаление участника (Только админ) ' )
    emb.add_field( name = '{}time'.format ( prefix ), value = 'Показ времени' )
    emb.add_field(name='{}play'.format(prefix), value='слушать музыку')

    await ctx.send( embed = emb )
    await ctx.send( 'Все команды писать с префиксом  ">" ')

@client.command( pass_context = True )

async def time( ctx ):
    emb = discord.Embed( title = 'Your title', description = 'Вы сможете узнать текущие время', colour = discord.Colour.purple(), url = 'https://www.timeserver.ru/' )

    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.set_image( url = 'https://images.unsplash.com/photo-1501139083538-0139583c060f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80' )
    emb.set_thumbnail( url = 'https://png.pngtree.com/element_our/png_detail/20181010/time-icon-vector-png_125592.jpg' )

    now_date = datetime.datetime.now()

    emb.add_field( name = 'Показ времени', value = 'Время : {}'.format( now_date ) )

    await ctx.send( embed = emb )

@client.event

async def on_member_join( member ):
    channel = client.get_channel(707873874489901069)

    role = discord.utils.get(member.guild.roles, id=710101627838660660)

    await member.add_roles( role )
    await channel.send( embed = discord.Embed(description = f'Добро пожаловать на наш Discord сервер {member.name} чтобы получить другую роль зайдите в текстовой канал "получение-роли"', color = 0x0c0c0c) )

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()

@client.command()
async def leave(ctx):
    try:
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        all_user = list(map(lambda x: x.name, channel.members))
        name_bot = ctx.guild.get_member(673636483281977402).name
        if name_bot in all_user:
            await voice.disconnect()
        else:
            await ctx.channel.send('Вы должы быть в канале с ботом, чтобы отключить его.')

    except:
        await ctx.channel.send('Вы должы быть в канале с ботом, чтобы отключить его.')

@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Пожалуйста ожидайте')

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print('[] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'[log] {name}, музыка завершилась'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.77

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')
    
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus.so')
    
@client.command
async def radio(ctx, urs: str):
    rs = radioShow()    
    
    await ctx.channel.send(rs + 'Выберите радиостанцию')

token = os.environ.get('BOT_TOKEN')

client.run(str(token))
