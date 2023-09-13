from json import load, dump
from telebot import TeleBot


filename    = "configs.json"

class SysProperty:

    filter      = [[22, 68, 72], [120, 255, 255]]
    cameraSleep = 60
    bot : TeleBot

    def __init__(self, bot) -> None:
        self.bot = bot

    def load(self):
        with open(filename, "r", encoding="utf_8") as file:
            data : dict         = load(file)

            self.filter         = data.get("filter", self.filter)
            self.cameraSleep    = data.get("cameraSleep", self.cameraSleep)

    def save(self):
        with open(self.filename, "w", encoding="utf_8") as file: dump(self.__as_dict__(), file)
            
    def parseUpperFilter(self, message):
        self.bot.send_message(message.chat.id, "🔸 Очикуються 3 числа від 0 до 255 через пробіл.\n\nПоточні значення:\t" + str(self.filter[1]))
        nums = message.text.lower().split()
        if len(nums) == 3:
            try: nums = list(map(int, nums))
            except: self.bot.send_message(message.chat.id, "🔺 Введені дані не вірні" + str(self.filter[1])); return False
            for i in nums:
                if i < 0 or i > 255: return False
            self.filter[1] = nums; 
            self.bot.reply_to(message, "✅ Дані оновлено")
            return True    
        
    def parseLowerFilter(self, message):
        self.bot.send_message(message.chat.id, "🔸 Очикуються 3 числа від 0 до 255 через пробіл.\n\nПоточні значення:\t" + str(self.filter[1]))
        nums = message.text.lower().split()
        if len(nums) == 3:
            try: nums = list(map(int, nums))
            except: self.bot.send_message(message.chat.id, "🔺 Введені дані не вірні" + str(self.filter[1])); return False
            for i in nums:
                if i < 0 or i > 255: return False
            self.filter[0] = nums
            self.bot.reply_to(message, "✅ Дані оновлено")
            return True                  

    def __as_dict__(self) -> dict: return {"filter": self.filter, "cameraSleep": self.cameraSleep}


            
