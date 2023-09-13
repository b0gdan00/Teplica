from telebot.types import Message, CallbackQuery
from telebot import TeleBot
from config.configs import SysProperty
from config.CameraController import ORIG_IMG_PATH, PROC_IMG_PATH
from config.threads import cameraStart, serialStart, checkCamera, checkSerial, stopThread
from config.Keyboards import keyControll, keyCamera, keyArduino, keySettings, closeForImage
from config.textGen import cameraInfo, arduinoInfo, configInfo
from config.statisctic import createPlot
from config.linux_commands import reload_service, git_update

BOGDANS_ID = "348691140"
bot = TeleBot("5820766754:AAEmxTSqYkB3Lgyv6YKgwNZWd58E5p5o8dM")
conf = SysProperty(bot)


@bot.message_handler(commands=["c", "con", "control"])
def controller(message : Message):
    bot.send_message(message.chat.id, "None", reply_markup=keyControll())


@bot.callback_query_handler(lambda call: call.data == "close")
def close(call : CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(lambda call: call.data.split()[1] == "main")
def main(call : CallbackQuery):
    com = call.data.split()[0]
    
    if com == "camera":
        state = checkCamera()
        from config.threads import currentGreen
        text = cameraInfo(state, currentGreen)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyCamera(state, conf))
        
    elif com == "arduino":
        state = checkSerial()
        text = arduinoInfo(state)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyArduino(state))

    elif com == "settings":
        bot.edit_message_text(configInfo(conf), call.message.chat.id, call.message.message_id, reply_markup=keySettings())

    elif com == "statistic":
        createPlot()
        with open("Images/stat.png", "rb") as file: bot.send_photo(call.message.chat.id, file, reply_markup=closeForImage())


@bot.callback_query_handler(lambda call: call.data.split()[0] == "arduino")
def image(call : CallbackQuery):
    com = call.data.split()[1]
    state = False
    if com == "on":
        state = serialStart(bot, call)
        if state == False: return None
    elif com == "off": stopThread(serial=True); state = checkSerial()
    elif com == "update": state = checkSerial()
    else: return None
    try:bot.edit_message_text(arduinoInfo(state), call.message.chat.id, call.message.message_id, reply_markup=keyArduino(state))
    except: pass


@bot.callback_query_handler(lambda call: call.data.split()[0] == "camera")
def image(call : CallbackQuery):
    com = call.data.split()[1]
    state = False

    if com == "on":
        state = cameraStart(bot, call, conf)
        if state == False: return None
    elif com == "off": stopThread(camera=True); state = checkCamera()
    elif com == "-" and conf.cameraSleep >60: conf.cameraSleep -= 60; state = checkCamera()
    elif com == "+": conf.cameraSleep += 60; state = checkCamera()
    elif com == "update": stopThread(camera=True); state = cameraStart(bot, call, conf)
    else: return None
    try: from config.threads import currentGreen; bot.edit_message_text(cameraInfo(state, currentGreen), call.message.chat.id, call.message.message_id, reply_markup=keyCamera(state, conf))
    except: pass


@bot.callback_query_handler(lambda call: call.data.split()[0] == "conf")
def settings(call : CallbackQuery):
    if call.data.split()[1] == "filter":
        if   call.data.split()[2] == "upper": bot.register_next_step_handler_by_chat_id(call.message.chat.id, conf.parseUpperFilter)
        elif call.data.split()[2] == "lower": bot.register_next_step_handler_by_chat_id(call.message.chat.id, conf.parseLowerFilter)
    elif call.data.split()[1] == "restart": reload_service()
    elif call.data.split()[1] == "update": bot.answer_callback_query(call, git_update())


@bot.callback_query_handler(lambda call: call.data.split()[0] == "image")
def image(call : CallbackQuery):       
    if call.data.split()[1] == "orig":
        with open(ORIG_IMG_PATH, "rb") as file: bot.send_photo(call.message.chat.id, file, reply_markup=closeForImage())
    else: 
        with open(PROC_IMG_PATH, "rb") as file: bot.send_photo(call.message.chat.id, file, reply_markup=closeForImage())


bot.polling(non_stop=True)