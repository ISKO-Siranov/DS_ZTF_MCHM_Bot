import discord
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl

import os
from time import sleep
import requests

prefix = '>'

client = commands.Bot(command_prefix=prefix)
client.remove_command( 'help' )

hello_words = ['hello','Hello','hi','Hi','привет','Привет',]
question = ['что ты умеешь?','че ты умеешь?','что здесь делать?','че здесь делать?']
bad = ['Иди нах','иди нах']

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
    if msg in bad:
        await message.channel.send(f'WHY YOU BULLING ME? {author.mention} FUCKING BITCH WHY YOU BULLING ME?')

@client.command( pass_context = True )

async def help( ctx ):
    emb = discord.Embed( title = 'Инструкция по командам' )

    emb.add_field( name = '{}clear'.format ( prefix ), value = 'Очистка чата' )
    emb.add_field( name = '{}kick'.format ( prefix ), value = 'Удаление участника (Только админ) ' )
    emb.add_field( name = '{}time'.format ( prefix ), value = 'Показ времени' )
    emb.add_field(name='{}cool'.format(prefix), value='с помощью этой команды вы сможете увидеть самое лучшее что вы видели в жизни')
    emb.add_field(name='{}play'.format(prefix), value='с помощью этой команды вы сможете слушать музыку просто введите команду !play пробел и url музыкального клипа с youtube, также не забудьте зайти в голосовой канал и прописать !join чтобы бот защел и вы его слышали (музыку) и также !leave чтобы бот вышел соответственно')

    await ctx.send( embed = emb )
    await ctx.send( 'Все команды писать с префиксом ">" ')

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

@client.command(pass_context=True)

async def cool( ctx ):
    emb = discord.Embed(title='КЛИКНИ НА ЭТУ НАДПИСЬ И СМОЖЕШЬ УВИДЕТЬ ЧУДО', description='Я ПРОСТО АФИГЕЛ КОГДА УВИДЕЛ ЭТО',colour=discord.Colour.red(), url='https://www.youtube.com/watch?v=9Nqe2TzAZX0')

    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    emb.set_image(url='https://i.ytimg.com/vi/9Nqe2TzAZX0/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&amp;rs=AOn4CLAyA6mqCl9DDPZIHmoWxiFZBHN2vw')
    emb.set_thumbnail(url='https://i.ytimg.com/vi/9Nqe2TzAZX0/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&amp;rs=AOn4CLAyA6mqCl9DDPZIHmoWxiFZBHN2vw')

    emb.add_field(name='ЭТО ПРОСТО ЖЕСТЬ', value='ПОСМОТРИ ПРЯМО СЕЙЧАС')

    await ctx.send(embed=emb)

@client.event

async def on_member_join( member ):
    channel = client.get_channel(707873874489901069)

    role = discord.utils.get(member.guild.roles, id=710101627838660660)

    await member.add_roles( role )
    await channel.send( embed = discord.Embed(description = f'Добро пожаловать на наш Discord сервер {member.name} чтобы получить другую роль зайдите в текстовой канал "получение-роли"', color = 0x0c0c0c) )

@client.command(pass_contex=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоеденился к каналу: {channel}')

@client.command(pass_contex=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот отключился от канала: {channel}')

@client.command(pass_context=True)
async def music(ctx, url: str):
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

    voice.play(discord.FFmpegPCMAudio('song.mp3'),after=lambda e: print(f'[log] {name}, музыка завершилась'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.77

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')

token = os.environ.get('BOT_TOKEN')

client.run(str(token))
