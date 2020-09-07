import discord
import datetime
import youtube_dl
import pyowm
import radio
import os
import requests
from discord.ext import commands
from discord.utils import get
from time import sleep
from discord import utils


prefix = "*"
players = {}
client = commands.Bot( command_prefix = prefix )
client.remove_command( 'help' )
observation = pyowm.OWM( '23e383b1f9723c91e85317b5e6a95c15', language = " ru " ).weather_at_place( 'Almaty,KZ' )
w = observation.get_weather()
windy = w.get_wind()[ 'speed' ]
tempash = w.get_temperature( 'celsius' )[ 'temp' ]
gradusov = [ 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,26,27,28,29,30,35,36,37,38,39,40,45,46,47,48,49,50 ]
gradusa = [ 2,3,4,22,23,24,32,33,34,42,43,44 ]
gradus = [ 1,21,31,41 ]


@client.command(pass_context=True)
async def weather( ctx ):
    if tempash in gradusov:
        await ctx.channel.send('В городе ' + 'Алматы' + ' сейчас ' + w.get_detailed_status() + ',' + ' температура сейчас составляет - ' + str( tempash ) + ' градусов' + ',' + "\n" + 'текущая скорость ветра = ' + str( windy ) + ' км/ч' + '.')  
    if tempash in gradusa:
        await ctx.channel.send('В городе ' + 'Алматы' + ' сейчас ' + w.get_detailed_status() + ',' + ' температура сейчас составляет - ' + str( tempash ) + ' градуса' + ',' + "\n" + 'текущая скорость ветра = ' + str( windy ) + ' км/ч' + '.')   
    if tempash in gradus:
        await ctx.channel.send('В городе ' + 'Алматы' + ' сейчас ' + w.get_detailed_status() + ',' + ' температура сейчас составляет - ' + str( tempash ) + ' градус' + ',' + "\n" + 'текущая скорость ветра = ' + str( windy ) + ' км/ч'  + '.')


@client.event
async def on_ready():
    print( 'BOT connected' )
    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'работника' ) )


@client.command( pass_context = True )
async def clear( ctx, amount = 100 ):
    await ctx.channel.purge( limit = amount )


@client.command( pass_context = True )
@commands.has_permissions( administrator = True )
async def kick( ctx, amount : int, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.kick( reason = reason, )
    await ctx.send( f'kick user { member.mention }' )
    await ctx.channel.purge( limit=amount )


@client.command( pass_context = True )
async def help( ctx ):
    emb = discord.Embed( title = 'Инструкция по командам' )
    emb.add_field( name = '{}c'.format ( prefix ), value = 'Очистка чата' )
    emb.add_field( name = '{}k'.format ( prefix ), value = 'Удаление участника (Только админ) ' )
    emb.add_field( name = '{}m'.format(prefix), value = 'слушать музыку' )
    emb.add_field( name = '{}w'.format(prefix), value = 'показ погоды в алматы' )
    emb.add_field( name = '{}s'.format(prefix), value = 'стоп музыки' )
    emb.add_field( name = '{}p'.format(prefix), value = 'пауза музыки' )
    emb.add_field( name = '{}r'.format(prefix), value = 'продолжение музыки' )
    emb.add_field( name = '{}j'.format(prefix), value = 'присоединение бота к голосовому каналу только если вы там есть' )
    emb.add_field( name = '{}l'.format(prefix), value = 'отсоединение от голосового канала' )
    await ctx.send( embed = emb )
    await ctx.send( 'Все команды писать с префиксом  - ' + prefix )


@client.event
async def on_member_join( member ):
    channel = client.get_channel( 707873874489901069 )
    role = discord.utils.get( member.guild.roles, id=710101627838660660 )
    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'Добро пожаловать на наш Discord сервер {member.name} чтобы получить другую роль зайдите в текстовой канал "получение-роли"', color = discord.Colour.blue ) )


@client.command( pass_context=True )
async def join( ctx ):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get( client.voice_clients, guild = ctx.guild )

    if voice and voice.is_connected():
        await voice.move_to ( channel )
    else:
        voice = await channel.connect()
        await ctx.send( f'Бот подключился к каналу : {channel}' )


@client.command( pass_context=True )
async def leave( ctx ):
    channel = ctx.message.author.voice.channel
    voice = get( client.voice_clients, guild = ctx.guild ) 

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await connect.channel()
        await ctx.send( f'Бот отсоединился от канала : {channel}' )


@client.command( pass_context=True )
async def m( ctx, url : str ):
    song_there = os.path.isfile( 'song.mp3' )

    try:
        if song_there:
            os.remove( 'song.mp3' )
            print( '[log] Старый файл удален' )
    except PermissionError:
        print( '[log] Не удалось удалить файл' )

    await ctx.send( 'Пожалуйста подождите' )

    voice = get( client.voice_clients, guild = ctx.guild )

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print( '[log] Загружаю музыку...' )
        ydl.download([url])
    
    for file in os.listdir( './' ):
        if file.endswith( '.mp3' ):
            name = file
            print( f'[log] Переименовываю файл: {file}' )
            os.rename( file, 'song.mp3' )

    voice.play( discord.FFmpegPCMAudio( 'song.mp3' ), after = lambda e: print( f'[log] {name}, Музыка завершилась' ))
    voice.source = discord.PCMVolumeTransformer( voice.source )
    voice.source.volume = 0.77

    song_name = name.rsplit( '-', 2 )
    await ctx.send( f'Сейчас играет : {song_name[0]}' )

    if not discord.opus.is_loaded():
        discord.opus.load_opus( 'libopus.so' )

   
@client.command( pass_context = True )
async def pause( ctx ):
    id = ctx.message.server.id
    players[id].pause()


@client.command( pass_context = True )
async def stop( ctx ):
    id = ctx.message.server.id
    players[id].stop()


@client.command( pass_context = True )
async def resume( ctx ):
    id = ctx.message.server.id
    players[id].resume()

T = os.environ.get('NzUxMzQ2MTc4NjE2MDY2MDU5.X1HvqA.ZjuDk3dOafgCHvxEFciicguUli0')

client.run(str(T))