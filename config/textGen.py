from config.DBEngine import SQLiteDB

def cameraInfo(state, currentGreen):
    text = "--   Камера   ---\n\n"
    if state: 
        text+= "Стан: 🟢\n"
        if currentGreen: text += "🌱 Рослинність: " + str(currentGreen) + "\n"
    else: text+= "Стан: 🔴\n"
    return text


def arduinoInfo(state):
    text = "--   Arduino   --\n\n"
    if state: text+= "Стан: 🟢\n"
    else: text+= "Стан: 🔴\n"
    try: 
        db = SQLiteDB()
        data = db.get_last_record()
        text += "Час запису: \t" + str(data[0]) + "\n"
        text += "Освітлення: \t" + str(data[1]) + "\n"
        text += "Вугл. газ: \t" + str(data[2]) + " ppm\n"
        text += "Температура: \t" + str(data[3]) + " °C \n"
    except: pass
    finally: db.close()
    return text


def configInfo(conf):
    text = "--   Налаштування   --\n\n"
    text += "Нижня межа фільтру: " + str(conf.filter[0]) + "\n"
    text += "Верхня межа фільтру: " + str(conf.filter[1]) + "\n"
    return text

