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

prefix = '>'

players = {}

client = commands.Bot(command_prefix=prefix)
client.remove_command( 'help' )

observation = owm.weather_at_place('Almaty,KZ')
w = observation.get_weather()
windy = w.get_wind()['speed']
tempash = w.get_temperature('celsius')['temp']

hello_words = ['hello','Hello','hi','Hi','привет','Привет',]
question = ['что ты умеешь?','че ты умеешь?','что здесь делать?','че здесь делать?']
gradusov = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,26,27,28,29,30,35,36,37,38,39,40,45,46,47,48,49,50]
gradusa = [2,3,4,22,23,24,32,33,34,42,43,44]
gradus = [1,21,31,41]

@client.command(pass_context=True)
async def weather(ctx):
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
        await message.channel.send(f' {author.mention} для полной инфы пропишите команду - >help ')

@client.command( pass_context = True )
async def help( ctx ):
    emb = discord.Embed( title = 'Инструкция по командам' )
    emb.add_field( name = '{}clear'.format ( prefix ), value = 'Очистка чата' )
    emb.add_field( name = '{}kick'.format ( prefix ), value = 'Удаление участника (Только админ) ' )
    emb.add_field( name = '{}time'.format ( prefix ), value = 'Показ времени' )
    emb.add_field(name='{}play'.format(prefix), value='слушать музыку')
    emb.add_field(name='{}weather'.format(prefix), value='показ погоды в алматы')
    await ctx.send( embed = emb )
    await ctx.send( 'Все команды писать с префиксом  - ">"  ')

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
    await channel.send( embed = discord.Embed(description = f'Добро пожаловать на наш Discord сервер {member.name} чтобы получить другую роль зайдите в текстовой канал "получение-роли"', color = discord.Colour.blue) )

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await ctx.send('Бот присоединился')

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await ctx.send('Бот вышел из голосового канала')

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
                                           
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus.so')
    
@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    
@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    
@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            # получаем объект канала
            channel = self.get_channel(payload.channel_id)
            # получаем объект сообщения
            message = await channel.fetch_message(payload.message_id)
            # получаем объект пользователя который поставил реакцию
            member = utils.get(message.guild.members, id=payload.user_id)

            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                # объект выбранной роли (если есть)
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])

                if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(
                        member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print(
                        '[ERROR] Too many roles for user {0.display_name}'.format(member))

            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        # получаем объект канала
        channel = self.get_channel(payload.channel_id)
        # получаем объект сообщения
        message = await channel.fetch_message(payload.message_id)
        # получаем объект пользователя который поставил реакцию
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)  # эмоджик который выбрал юзер
            # объект выбранной роли (если есть)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(
                member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
    
token = os.environ.get('BOT_TOKEN')

client.run(str(token))
