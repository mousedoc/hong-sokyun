# -*- coding: utf-8 -*-
import discord
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from discord import channel
from enum import Enum


client = discord.Client()

is_ready = False

chat_channel_id = 869887391140306995      # 잡담 채널
control_channel_id = 870608206697738260   # 홍석근 조종실 채널
command_channel_id = 869893746911756298    # 명령어 채널

chat_channel = None
control_channel = None
command_channel = None

role_afternoon = '화룡 - 낮 (13:00, 16:00)'
role_evening = '화룡 - 저녁 (19:00)'
role_night = '화룡 - 밤 (22:00)'
role_dawn = '화룡 - 새벽 (01:00)'

role_map = {
    '낮': role_afternoon,
    '저녁': role_evening,
    '밤': role_night,
    '새벽': role_dawn,
}


def initialize():
    global is_ready

    initialize_channel()
    is_ready = True


def initialize_channel():
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
    role = discord.utils.get(message.guild.roles, name=role_name)

    if role in member.roles:
        await member.remove_roles(role)
        await command_channel.send(f'<@{member.id}> {role_name} 알림 삭제')
    else:
        await member.add_roles(role)
        await command_channel.send(f'<@{member.id}> {role_name} 알림 추가')


async def notify_dragon_time(role_name):
    guild = client.get_guild(869887390657937409)
    role = discord.utils.get(guild.roles, name=role_name)
    await chat_channel.send(f'<@&{role.id}> 화룡 가자 막내야')


async def time_scheduler():
    change_hour = False
    last_hour = -1

    while is_ready == False:
        await asyncio.sleep(1)

    while True:
        
        now = datetime.now()
        current_min = now.minute
        current_hour = now.hour
        
        if current_min >= 0 and current_min <= 10:

            change_hour = last_hour is not current_hour
            last_hour = current_hour

            if change_hour is True:
                if current_hour == 1:
                    await notify_dragon_time(role_dawn)
                elif current_hour == 19:
                    await notify_dragon_time(role_evening)
                elif current_hour == 22:
                    await notify_dragon_time(role_night)

                # 금, 토, 일
                if now.weekday() >= 4 and now.weekday() <= 6:
                    if current_hour == 13:
                        await notify_dragon_time(role_afternoon)
                    elif current_hour == 16:
                        await notify_dragon_time(role_afternoon)




# Start
token = 'YOUR BOT TOKEN'
client.loop.create_task(time_scheduler())
client.run(token)

