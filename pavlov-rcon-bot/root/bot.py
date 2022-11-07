# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import asyncio
import telebot
import json
from pavlov import PavlovRCON
from telebot.util import quick_markup
import yaml
from pathlib import Path
from telebot.async_telebot import AsyncTeleBot
import asyncio

conf = yaml.safe_load(Path('config.yaml').read_text())

token = conf['telegram_token']

bot = AsyncTeleBot(token)

help_message = "Доступные комманды \n/servers_info - получить информацио о серверрах\n/get_place - получить место на сервере"
print(conf['servers'].keys())

async def server_info(server):
    pavlov = PavlovRCON(
        conf['servers'][server]['host'],
        conf['servers'][server]['port'],
        conf['servers'][server]['password']
    ,timeout=20)
    info = await pavlov.send("ServerInfo",auto_close=True)
    result={
            "ServerName":info["ServerInfo"]["ServerName"],
            "PlayerCount":info["ServerInfo"]["PlayerCount"]
    }
    print(result)
    return result

async def servers_info():
    servers_info=[]
    for server in conf['servers'].keys():
        info=await server_info(server)
        servers_info.append(info)
    return [servers_info]


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False,resize_keyboard=True)
    server_info = telebot.types.KeyboardButton(text="/servers_info")
    get_place = telebot.types.KeyboardButton(text="/get_place")
    keyboard.add(server_info,get_place)
    await bot.send_message(message.from_user.id, help_message, reply_markup=keyboard)

@bot.message_handler(commands=['servers_info'])
async def send_servers_info(message):
    for server in conf['servers'].keys():
        info=await server_info(server)
        await bot.send_message(message.from_user.id, "{player_count}  {server_name}".format(server_name=info["ServerName"],
                                                           player_count=info["PlayerCount"]
                                                            ))


@bot.message_handler(func=lambda message: True)
async def echo_all(message):
	chat = message.text
	await bot.reply_to(message, "Нет такой команды: "+str(chat)+", смотри /help")

asyncio.run(bot.polling(non_stop=True))
