from serial import Serial
from config.CameraController import CameraController
from time import sleep
from threading import Thread
from config.linux_commands import change_permissions
from config.DBEngine import SQLiteDB 

currentGreen = 0
active_threads = {"camera": None, "serial": None}


def stopThread(camera = False, serial = False):
    if camera and active_threads["camera"]: active_threads["camera"] = None 
    if serial and active_threads["serial"]: active_threads['serial'] = None

# SERIAL ______________________
def serialStart(bot, call):
    if active_threads["serial"] != None: bot.answer_callback_query(call.id, "🟠 Підключення вже встановлене"); return True
    active_threads["serial"] = Thread(target=SerialThread)
    active_threads["serial"].daemon = True
    active_threads["serial"].start()
    sleep(0.5)
    if checkSerial(): bot.answer_callback_query(call.id, "🟢 Підключення встановлене"); return True
    else: bot.answer_callback_query(call.id, "🔺 Помилка підключення, перевірте фізичне з'єднання контактів"); active_threads["serial"] = None; return False
    
def checkSerial():
    if active_threads["serial"] != None:
        if active_threads["serial"].is_alive(): return True
    return False

def SerialThread():
    global currentGreen
    change_permissions()
    try: ser = Serial('/dev/ttyUSB0', 9600) # Розраховано на підключення до Лінукс
    except: pass
    try: ser = Serial('COM4', 9600)         # При підключенні до Віндоус
    except: pass

    db = SQLiteDB()
    while active_threads["serial"] != None:
        try:
            if ser.in_waiting > 0:
                temperature = ser.readline().decode().strip().split("=")[1].strip()
                CO2         = ser.readline().decode().strip().split("=")[1].strip()
                light       = ser.readline().decode().strip().split("=")[1].strip()
                db.add_new_dataframe(float(temperature), float(light), float(CO2), currentGreen)
        except: active_threads["serial"] = None; break
        finally:db.close()

# CAMERA ______________________

def cameraStart(bot, call, conf):
    if active_threads["camera"] != None: bot.answer_callback_query(call.id, "🟠 Камера вже працює"); return True
    active_threads["camera"] = Thread(target=CameraThread, args=(conf.cameraSleep, conf.filter, ))
    active_threads["camera"].daemon = True
    active_threads["camera"].start(); sleep(2)
    if checkCamera(): bot.answer_callback_query(call.id, "🟢 Камера працює"); return True
    else: bot.answer_callback_query(call.id, "🔺 Камера не працює"); active_threads["camera"] = None; return False

def checkCamera():
    if active_threads["camera"] != None:
        if active_threads["camera"].is_alive():  return True
    return False

def CameraThread(camera_sleep, filter):
    global currentGreen
    while active_threads["camera"] != None:
        if CameraController.new():
        # if True:
            print("Start proc image")
            cm = CameraController()
            cm.crop()
            cm.filter(filter)
            currentGreen = cm.calculate()
            cm.save()
            print("Save proc image")
        else: active_threads["camera"] = None; break
        sleep(camera_sleep)