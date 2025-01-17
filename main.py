import telebot
from telebot import types

from dotenv import load_dotenv
import os

from database import Database
db = Database()

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

user_form = {}

@bot.message_handler(commands=["export"])
def exporting(message):
    if message.chat.id == int(os.getenv("ADMIN1_ID")) or message.chat.id == int(os.getenv("ADMIN2_ID")):
        db.connect()
        db.export_into_sheets()
        db.close()

def handle_back(func):
    def wrapper(message, *args, **kwargs):
        if message.text == "🔙Назад":
            db.close()

            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton("✏️Заполнить форму")
            btn2 = types.KeyboardButton("🌐Сайт House System")

            markup.add(btn1, btn2)
            user_form[message.chat.id] = {"skills": [], "skills_dict":{
                                    "think": False,
                                    "communicate": False,
                                    "risk": False,
                                    "flexible": False,
                                    "perseverance": False,
                                    "teamwork": False,
                                    "plan": False,
                                    "globalthinking": False,
                                    "ethical": False,
                                    "makedecisions": False,
                                    "responsibility": False,
                                    "strong": False,
                                    "efficiency": False
            }}

            photo = open('pic/welcome.png', 'rb')
            bot.send_photo(message.chat.id, photo, caption=f"{message.from_user.first_name}, приветствуем тебя в боте по обработке обратной связи!", reply_markup=markup)
        else:
            return func(message, *args, **kwargs)
    return wrapper

@bot.message_handler(commands=["start"])
def start(message):
    user_form[message.chat.id] = {"skills": [], "skills_dict":{
                                    "think": False,
                                    "communicate": False,
                                    "risk": False,
                                    "flexible": False,
                                    "perseverance": False,
                                    "teamwork": False,
                                    "plan": False,
                                    "globalthinking": False,
                                    "ethical": False,
                                    "makedecisions": False,
                                    "responsibility": False,
                                    "strong": False,
                                    "efficiency": False
    }}

    # db.connect()
    # db.create()
    # db.close()

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("✏️Заполнить форму")
    btn2 = types.KeyboardButton("🌐Сайт House System")

    markup.add(btn1, btn2)

    photo = open('pic/welcome.png', 'rb')  
    bot.send_photo(message.chat.id, photo, caption=f"{message.from_user.first_name}, приветствуем тебя в боте по обработке обратной связи!", reply_markup=markup)

    bot.register_next_step_handler(message, on_click)
    
@bot.message_handler()
@handle_back
def on_click(message):
    if message.text == "✏️Заполнить форму":
        db.connect()

        user_form[message.chat.id] = {"skills": [], "skills_dict":{
                                    "think": False,
                                    "communicate": False,
                                    "risk": False,
                                    "flexible": False,
                                    "perseverance": False,
                                    "teamwork": False,
                                    "plan": False,
                                    "globalthinking": False,
                                    "ethical": False,
                                    "makedecisions": False,
                                    "responsibility": False,
                                    "strong": False,
                                    "efficiency": False
        }}
        

        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton("🔙Назад"))
        
        bot.send_message(message.chat.id, "Имя Фамилия", reply_markup=markup)
        bot.register_next_step_handler(message, user_name)

    if message.text == "📩Отправить":
        db.save_message(message, user_form)

        del user_form[message.chat.id]
        
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("✏️Заполнить форму")
        btn2 = types.KeyboardButton("🌐Сайт House System")

        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, "Форма успешно отправлена!", reply_markup=markup)
        
        db.close()
    
    if message.text == "🌐Сайт House System":
        bot.send_message(message.chat.id, "https://houses.primakov.school/")

@handle_back
def user_name(message):    
    user_form[message.chat.id]['name'] = message.text

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🐉E", callback_data="east")
    btn2 = types.InlineKeyboardButton("🦁W", callback_data="west")
    btn3 = types.InlineKeyboardButton("🐅S", callback_data="south")
    btn4 = types.InlineKeyboardButton("🐻‍❄️N", callback_data="north") 

    if message.text != "" and not "house" in user_form[message.chat.id].keys():
        markup.row(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Выберите House", reply_markup=markup)
    elif message.text != "" and "house" in user_form[message.chat.id].keys():
        bot.send_message(message.chat.id, "❗Упс, не та кнопка")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    markup = types.InlineKeyboardMarkup()
    
    house = ["east", "west", "north", "south"]
    exp = ["Опыт публичного выступления", "Социальный опыт", "Организаторский опыт", "Опыт творчества", "Опыт наставничества", "Спортивный опыт", "Опыт участника"]

    if callback.data in house:
        user_form[callback.message.chat.id]['house'] = callback.data

        btn1 = types.InlineKeyboardButton("Опыт публичного выступления", callback_data="Опыт публичного выступления")
        btn2 = types.InlineKeyboardButton("Социальный опыт", callback_data="Социальный опыт")
        btn3 = types.InlineKeyboardButton("Организаторский опыт", callback_data="Организаторский опыт")
        btn4 = types.InlineKeyboardButton("Опыт творчества", callback_data="Опыт творчества")
        btn5 = types.InlineKeyboardButton("Опыт наставничества", callback_data="Опыт наставничества")
        btn6 = types.InlineKeyboardButton("Спортивный опыт", callback_data="Спортивный опыт")
        btn7 = types.InlineKeyboardButton("Опыт участника", callback_data="Опыт участника")
        
        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        markup.row(btn4)
        markup.row(btn5)
        markup.row(btn6)
        markup.row(btn7)

        bot.edit_message_text("Какой опыт ты получил?", callback.message.chat.id, callback.message.message_id, reply_markup=markup)

    if callback.data in exp:
        user_form[callback.message.chat.id]['exp'] = callback.data

        btn1 = types.InlineKeyboardButton("5", callback_data="5")
        btn2 = types.InlineKeyboardButton("10", callback_data="10")
        btn3 = types.InlineKeyboardButton("15", callback_data="15")
        
        markup.row(btn1, btn2, btn3)

        bot.edit_message_text("Кол-во полученных баллов", callback.message.chat.id, callback.message.message_id, reply_markup=markup)

    if callback.data == "5":
        user_form[callback.message.chat.id]['points'] = callback.data

        bot.send_message(callback.message.chat.id, "Что именно ты сделал?")

        bot.register_next_step_handler(callback.message,  wrap_on_click("5"))

    btns = ["think", "communicate", "risk", "flexible", "perseverance", "teamwork", "plan", "globalthinking", "ethical", "makedecisions", "responsibility", "strong", "efficiency"]
    
    callback_text_skills = {
        "think": "Мыслить",
        "communicate": "Коммуницировать",
        "risk": "Уметь рисковать",
        "flexible": "Быть гибким",
        "perseverance": "Быть упорным",
        "teamwork": "Работать в команде",
        "plan": "Уметь планировать",
        "globalthinking": "Осознавать важность глобального мышления",
        "ethical": "Осознавать важность этических норм",
        "makedecisions": "Уметь принимать решения",
        "responsibility": "Нести ответственность за свои решения",
        "strong": "Оценивать сильные стороны и точки роста",
        "efficiency": "Верить в собственную эффективность"
    }
    
    if callback.data in btns and callback_text_skills[callback.data] not in user_form[callback.message.chat.id]["skills"]:
        user_form[callback.message.chat.id]["skills"].append(callback_text_skills[callback.data])
        
        user_form[callback.message.chat.id]["skills_dict"][callback.data] = not user_form[callback.message.chat.id]["skills_dict"][callback.data]

        markup = types.InlineKeyboardMarkup()

        for callback_skill, selected in user_form[callback.message.chat.id]["skills_dict"].items():
            skill = callback_text_skills[callback_skill]

            if selected == True:
                btn_text = f"✅ {skill}"
            else:
                btn_text = skill

            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_skill))
        
        if user_form[callback.message.chat.id]["points"] == "15":
            markup.add(types.InlineKeyboardButton("✅Я готов", callback_data="✅Я готов"))

        if user_form[callback.message.chat.id]["points"] == "10":
            markup.add(types.InlineKeyboardButton("✅Готов", callback_data="✅Готов"))

        if user_form[callback.message.chat.id]["points"] == "5":
            markup.add(types.InlineKeyboardButton("✅Готово", callback_data="✅Готово"))

        bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)
        
    elif callback.data in btns and callback_text_skills[callback.data] in user_form[callback.message.chat.id]["skills"]:
        skills_list = user_form[callback.message.chat.id]["skills"]
        

        for skill in skills_list:
            if skill == callback_text_skills[callback.data]:
                skills_list.remove(skill)
        
        user_form[callback.message.chat.id]["skills_dict"][callback.data] = not user_form[callback.message.chat.id]["skills_dict"][callback.data]

        markup = types.InlineKeyboardMarkup()

        for callback_skill, selected in user_form[callback.message.chat.id]["skills_dict"].items():
            skill = callback_text_skills[callback_skill]

            if selected == True:
                btn_text = f"✅ {skill}"
            else:
                btn_text = skill

            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_skill))
        
        if user_form[callback.message.chat.id]["points"] == "15":
            markup.add(types.InlineKeyboardButton("✅Я готов", callback_data="✅Я готов"))

        if user_form[callback.message.chat.id]["points"] == "10":
            markup.add(types.InlineKeyboardButton("✅Готов", callback_data="✅Готов"))

        if user_form[callback.message.chat.id]["points"] == "5":
            markup.add(types.InlineKeyboardButton("✅Готово", callback_data="✅Готово"))

        bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)
        
    if callback.data == "✅Готово" and user_form[callback.message.chat.id]["skills"] != "":
        markup = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton("Да", callback_data="Да")
        no = types.InlineKeyboardButton("Нет", callback_data="Нет")
        markup.row(yes, no)

        bot.send_message(callback.message.chat.id, f"Хотел бы ты повторить этот опыт/посоветовать его другу?", reply_markup=markup)
    
    if callback.data == "✅Готово" and user_form[callback.message.chat.id]["skills"] == "":
        bot.send_message(callback.message.chat.id, "❗️Выбери скиллы, которые прокачал")

    if callback.data == "✅Готов" and user_form[callback.message.chat.id]["skills"] != "":
        bot.send_message(callback.message.chat.id, "Как именно ты прокачал выбранный скил (или скилы)?")
        bot.register_next_step_handler(callback.message, on_click10_skills)
    
    if callback.data == "✅Готов" and user_form[callback.message.chat.id]["skills"] == "":
        bot.send_message(callback.message.chat.id, "❗️Выбери скиллы, которые прокачал")

    if callback.data == "✅Я готов" and user_form[callback.message.chat.id]["skills"] != "":
        bot.send_message(callback.message.chat.id, "Как именно ты прокачал выбранный скил (или скилы)?")
        bot.register_next_step_handler(callback.message,  on_click15_skills)
    
    if callback.data == "✅Я готов" and user_form[callback.message.chat.id]["skills"] == "":
        bot.send_message(callback.message.chat.id, "❗️Выбери скиллы, которые прокачал")

    team_work = ["удалась", "не-удалась", "не-относится"]
    team_work_15 = ["удалась-15", "не-удалась-15", "не-относится-15"]
    
    if callback.data == "Да" or callback.data == "Нет" or callback.data in team_work or callback.data in team_work_15:
        callback_text_team_15 = {
            "удалась-15": "Работа в команде удалась",
            "не-удалась-15": "Работа в команде не удалась",
            "не-относится-15": "Работа в команде к этому опыту не относится"
        }

        callback_text_team = {
            "удалась": "Работа в команде удалась",
            "не-удалась": "Работа в команде не удалась",
            "не-относится": "Работа в команде к этому опыту не относится"
        }

        if callback.data == "Да" or callback.data == "Нет":
            user_form[callback.message.chat.id]['repeat'] = callback.data
        elif callback.data in team_work_15:
            user_form[callback.message.chat.id]['team_work'] = callback_text_team_15[callback.data]
        else:
            user_form[callback.message.chat.id]['team_work'] = callback_text_team[callback.data]
        
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("👎1", callback_data="1rate")
        btn2 = types.InlineKeyboardButton("2", callback_data="2rate")
        btn3 = types.InlineKeyboardButton("3", callback_data="3rate")
        btn4 = types.InlineKeyboardButton("4", callback_data="4rate")
        btn5 = types.InlineKeyboardButton("5", callback_data="5rate")
        btn6 = types.InlineKeyboardButton("6", callback_data="6rate")
        btn7 = types.InlineKeyboardButton("7", callback_data="7rate")
        btn8 = types.InlineKeyboardButton("8", callback_data="8rate")
        btn9 = types.InlineKeyboardButton("9", callback_data="9rate")
        btn10 = types.InlineKeyboardButton("🌟10", callback_data="10rate")
        markup.row(btn1, btn2, btn3)
        markup.row(btn4, btn5, btn6)
        markup.row(btn7, btn8, btn9)
        markup.row(btn10)   

        bot.send_message(callback.message.chat.id, "Оцени как ты справился с этим опытом по 10-бальной шкале", reply_markup=markup)

    rates = ["1rate","2rate","3rate","4rate","5rate","6rate","7rate","8rate","9rate","10rate",]            

    if callback.data in rates:
        callback_text_rates = {
            "1rate": "1",
            "2rate": "2",
            "3rate": "3",
            "4rate": "4",
            "5rate": "5",
            "6rate": "6",
            "7rate": "7",
            "8rate": "8",
            "9rate": "9",
            "10rate": "10"
        }

        user_form[callback.message.chat.id]['result'] = callback_text_rates[callback.data]
        
        markup = types.ReplyKeyboardMarkup()
        send = types.KeyboardButton("📩Отправить")
        cancel = types.KeyboardButton("🔙Назад")
        
        markup.row(send, cancel)

        bot.send_message(callback.message.chat.id, "Отправить форму?", reply_markup=markup)
        
        bot.register_next_step_handler(callback.message, on_click)
    
    if callback.data == "10":
        user_form[callback.message.chat.id]['points'] = callback.data

        bot.send_message(callback.message.chat.id, "Что именно ты сделал?", reply_markup=markup)

        bot.register_next_step_handler(callback.message, wrap_on_click("10"))

    if callback.data == "15":
        user_form[callback.message.chat.id]['points'] = callback.data

        bot.send_message(callback.message.chat.id, "Что именно ты сделал?", reply_markup=markup)

        bot.register_next_step_handler(callback.message, wrap_on_click("15"))

@bot.message_handler()
@handle_back
def on_click15_skills(message):
    user_form[message.chat.id]['exactly'] = message.text

    bot.send_message(message.chat.id, "Столкнулся ли ты со сложностями при планировании или во время реализации опыта?")
    bot.register_next_step_handler(message, on_click15_difficult)

@bot.message_handler()
@handle_back
def on_click15_difficult(message):
    user_form[message.chat.id]['difficulties'] = message.text

    bot.send_message(message.chat.id, "Что стало мотивацией для реализации опыта?")
    bot.register_next_step_handler(message, on_click15_motivation)

@bot.message_handler()
@handle_back
def on_click15_motivation(message):
    user_form[message.chat.id]['motivation'] = message.text
        
    bot.send_message(message.chat.id, "Опиши свой самый успешный момент в работе")
    bot.register_next_step_handler(message, on_click15_success)

@bot.message_handler()
@handle_back
def on_click15_success(message):
        user_form[message.chat.id]['moment'] = message.text

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("К этому опыту не относится", callback_data="не-относится-15")
        btn2 = types.InlineKeyboardButton("Работа в команде не удалась", callback_data="не-удалась-15")
        btn3 = types.InlineKeyboardButton("Работа в команде удалась", callback_data="удалась-15")

        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        
        bot.send_message(message.chat.id, "Удалось ли поработать в команде?", reply_markup=markup)

@bot.message_handler()
@handle_back
def on_click10_skills(message):
        user_form[message.chat.id]['exactly'] = message.text

        bot.send_message(message.chat.id, "Столкнулся ли ты со сложностями при планировании или во время реализации опыта?")
        bot.register_next_step_handler(message, on_click10_difficult)

@bot.message_handler()
@handle_back
def on_click10_difficult(message):
        user_form[message.chat.id]['difficulties'] = message.text

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("К этому опыту не относится", callback_data="не-относится")
        btn2 = types.InlineKeyboardButton("Работа в команде не удалась", callback_data="не-удалась")
        btn3 = types.InlineKeyboardButton("Работа в команде удалась", callback_data="удалась")

        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)

        bot.send_message(message.chat.id, "Удалась ли работа в команде", reply_markup=markup)

def wrap_on_click(points):
    @bot.message_handler()
    @handle_back    
    def on_click(message):
        user_form[message.chat.id]['done'] = message.text

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Мыслить", callback_data="think")
        btn2 = types.InlineKeyboardButton("Коммуницировать", callback_data="communicate")
        btn3 = types.InlineKeyboardButton("Уметь рисковать", callback_data="risk")
        btn4 = types.InlineKeyboardButton("Быть гибким", callback_data="flexible")
        btn5 = types.InlineKeyboardButton("Быть упорным", callback_data="perseverance")
        btn6 = types.InlineKeyboardButton("Работать в команде", callback_data="teamwork")
        btn7 = types.InlineKeyboardButton("Уметь планировать", callback_data="plan")
        btn8 = types.InlineKeyboardButton("Осознавать важность глобального мышления", callback_data="globalthinking")
        btn9 = types.InlineKeyboardButton("Осознавать важность этических норм", callback_data="ethical")
        btn10 = types.InlineKeyboardButton("Уметь принимать решения", callback_data="makedecisions")
        btn11 = types.InlineKeyboardButton("Нести ответственность за свои решения", callback_data="responsibility")
        btn12 = types.InlineKeyboardButton("Оценивать сильные стороны и точки роста", callback_data="strong")
        btn13 = types.InlineKeyboardButton("Верить в собственную эффективность", callback_data="efficiency")

        if points == "15":
            btn14 = types.InlineKeyboardButton("✅Я готов", callback_data="✅Я готов")

        if points == "10":
            btn14 = types.InlineKeyboardButton("✅Готов", callback_data="✅Готов")

        if points == "5":
            btn14 = types.InlineKeyboardButton("✅Готово", callback_data="✅Готово")
        btns = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14]
        
        for btn in btns:
            markup.add(btn)

        bot.send_message(message.chat.id, "Какой/какие skill/skills удалось прокачать во время планирования и реализации опыта?", reply_markup=markup)

    return on_click

bot.polling(non_stop=True)