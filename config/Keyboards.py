from telebot.types import InlineKeyboardButton as Button
from telebot.types import InlineKeyboardMarkup as Keyboard

close = Button("🔻 Закрити 🔻", callback_data="close")

def closeForImage():
    keyboard = Keyboard()
    keyboard.add(close)
    return keyboard

def keyControll():
    keyboard = Keyboard()
    keyboard.add(Button("📷 -- Камера -- 📷", callback_data="camera main"))
    keyboard.add(Button("📟 -- Arduino -- 📟", callback_data="arduino main"))
    keyboard.add(Button("⚙️ -- Налаштування -- ⚙️", callback_data="settings main"))
    keyboard.add(Button("📈 -- Статистика -- 📉", callback_data="statistic main"))
    keyboard.add(close)
    return keyboard

def keyCamera(state, conf):
    keyboard = Keyboard()
    if not state: keyboard.add(Button("🔄 Увімкнути", callback_data="camera on"))
    else: 
        keyboard.add(Button("⏸ Вимкнути", callback_data="camera off"))
        keyboard.add(Button("📘 Оригінал", callback_data="image orig"), Button("Обробка 📙", callback_data="image proc"))
        keyboard.add(
            Button("◀️", callback_data="camera -"), 
            Button("⏱ " + str(conf.cameraSleep) + " сек.", callback_data="camera sleep"), 
            Button("▶️", callback_data="camera +"))
        
    keyboard.add(Button("🔂 Оновити", callback_data="camera update"))
    keyboard.add(close)
    return keyboard


def keyArduino(state):
    keyboard = Keyboard()
    if not state: keyboard.add(Button("🔄 Увімкнути", callback_data="arduino on"))
    else: keyboard.add(Button("⏸ Вимкнути", callback_data="arduino off"))
    keyboard.add(Button("🔂 Оновити", callback_data="arduino update"))
    keyboard.add(close)
    return keyboard

def keySettings():
    keyboard = Keyboard()
    keyboard.add(Button("🔄 Перезапуск серверу", callback_data="conf restart"))
    keyboard.add(Button("👾 Оновлення версії коду", callback_data="conf update"))
    keyboard.add(Button("📤 Верхній рівень фільтру", callback_data="conf filter upper"))
    keyboard.add(Button("📥 Нижній рівень фільтру ", callback_data="conf filter lower"))
    keyboard.add(close)
    return keyboard
