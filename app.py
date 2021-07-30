# -*- coding: utf-8 -*-
import discord
import time

from discord import channel
import schedule

from enum import Enum

client = discord.Client()

chat_channel_id = 869887391140306995      # 잡담 채널
control_channel_id = 870608206697738260   # 홍석근 조종실 채널
command_channel_id = 869893746911756298    # 명령어 채널

chat_channel = None
control_channel = None
command_channel = None

class DragonTime(Enum):
    Morning = 0
    Afternoon = 1
    Evening = 2
    Night = 3
    Dawn = 4


role_morning = '화룡 - 아침 (10:00)'
role_afternoon =  '화룡 - 낮 (13:00, 16:00)'
role_evening =  '화룡 - 저녁 (19:00)'
role_night = '화룡 - 밤 (22:00)'
role_dawn =  '화룡 - 새벽 (01:00)'

role_map = { \
    '아침':role_morning, \
    '낮':role_afternoon, \
    '저녁':role_evening, \
    '밤':role_night, \
    '새벽':role_dawn, \
}



def initialize():
    initialize_channel()

def initialize_channel():
    global control_channel_id
    global command_channel_id
    global chat_channel_id

    global control_channel
    global command_channel
    global chat_channel

    control_channel = client.get_channel(control_channel_id)
    command_channel = client.get_channel(command_channel_id)
    chat_channel = client.get_channel(chat_channel_id)


@client.event
async def on_ready(): 
    print(f'홍석근 ON : {client.user.name}, {client.user.id}')
    initialize()


@client.event
async def on_message(message): 

    content = message.content    

    # In command channel 
    if message.channel is command_channel:

        if content.startswith('!핑'): 
            await ping_action()
            return

        elif content.startswith('!화룡'):
            await dragon_action(message)
            return
    
    # In control channel
    elif message.channel is control_channel:
        await control_action(message)
        return

# Ping
async def ping_action():
    await command_channel.send(f'홍석근 반응 속도 : {round(round(client.latency, 4)*1000)}ms')

# Control
async def control_action(message):
    await chat_channel.send(message.content)

# Dragon    
async def dragon_action(message):
    global role_map

    member = message.author

    time_name = message.content.split()[1]
    role_name = role_map[time_name]
    role = discord.utils.get(message.guild.roles, name = role_name)

    if role in member.roles:
        await member.remove_roles(role)
        await command_channel.send(f'<@{member.id}> {role_name} 알림 추가')
    else:
        await member.add_roles(role)
        await command_channel.send(f'<@{member.id}> {role_name} 알림 삭제')
    

# 특정 함수 정의
async def notify_dragon_time(role_name):
    guild = client.get_guild(869887390657937409)
    role = discord.utils.get(guild.roles, name = role_name)
    await chat_channel.send(f'<@{role.id}> 화룡 가자 막내야')

 
 
# schedule.every().day.at('01:00').do(notify_dragon_time(role_dawn)) 
# schedule.every().day.at('19:00').do(notify_dragon_time(role_evening)) 
# schedule.every().day.at('22:00').do(notify_dragon_time(role_night)) 

# schedule.every().friday.at('13:00').do(notify_dragon_time(role_afternoon)) 
# schedule.every().friday.at('16:00').do(notify_dragon_time(role_afternoon)) 

# schedule.every().saturday.at('13:00').do(notify_dragon_time(role_afternoon)) 
# schedule.every().saturday.at('16:00').do(notify_dragon_time(role_afternoon)) 

# schedule.every().sunday.at('13:00').do(notify_dragon_time(role_afternoon)) 
# schedule.every().sunday.at('16:00').do(notify_dragon_time(role_afternoon)) 
 

# Start
token = 'ODcwNTk1OTgyNDM2NDc0OTIx.YQPDsQ.AuI1Iv9euyD_iz1uwTBN_zy7XlY'
client.run(token)

# #실제 실행하게 하는 코드
# while True:
#     schedule.run_pending()
#     time.sleep(6000)
