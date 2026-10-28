import telebot
from telebot import types

# 🤖 ВСТАВЬ СЮДА ТОКЕН СВОЕГО БОТА:
BOT_TOKEN = "8846318583:AAGCM30b_rupjQqrs6EXuVAT8NyFuyfB48Q"

# ID Николая
ADMIN_CHAT_ID = 822606772 

bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для отслеживания состояний пользователей (кто нажал «Задать вопрос»)
waiting_for_question = {}

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("📦Групи товарів")
    btn2 = types.KeyboardButton("🎁Акції та бонуси")
    btn3 = types.KeyboardButton("💬Задати питання агроному")
    btn4 = types.KeyboardButton("🕒Графік роботи і контакти")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name or "Без имени"
    
    # 🔍 Логируем в консоль ID и имя того, кто запустил бота
    print(f"[*] Пользователь запустил бота: ID={chat_id}, Имя={first_name}")
    
    waiting_for_question[chat_id] = False
    text = (
        "Вітаю у магазині Агроаптека. Я Ваш віртуальний агроном-помічник. "
        "Оберіть будь ласка що саме Вас цікавить."
    )
    bot.send_message(chat_id, text, reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == "📦Групи товарів":
        waiting_for_question[chat_id] = False
        response = (
            "🌱 В нашому асортименті:\n"
            "• 🌾 Насіння\n"
            "• 🛡️ Засоби захисту рослин\n"
            "• 🧪 Добрива\n"
            "• 🏺 Вазони\n"
            "• ✂️ Садовий інструмент\n"
            "• 📜️ Плівка теплична\n"
            "• 🌿 Агроволокно\n"
            "• 📦 Субстрати"
        )
        bot.send_message(chat_id, response, reply_markup=get_main_keyboard())
        
    elif text == "🎁Акції та бонуси":
        waiting_for_question[chat_id] = False
        response = "Для постійних клієнтів діє заохочувальна система знижок та бонусів. За деталями звертайтеся до менеджера."
        bot.send_message(chat_id, response, reply_markup=get_main_keyboard())
        
    elif text == "💬Задати питання агроному":
        waiting_for_question[chat_id] = True
        response = "💬Будь ласка, напишіть ваше запитання нижче в чаті, і ми передамо його агроному."
        bot.send_message(chat_id, response)
        
    elif text == "🕒Графік роботи і контакти":
        waiting_for_question[chat_id] = False
        response = (
            "🕒 Пн-Пт : 8.00-18.00 | Сб, Нд: 8.00-17.00\n"
            "📍 М. Роздільна вул Європейська 93а Маг АГРОАПТЕКА\n"
            "📞 Тел. 0660211027"
        )
        bot.send_message(chat_id, response, reply_markup=get_main_keyboard())
        
    else:
        if waiting_for_question.get(chat_id, False):
            user_name = message.from_user.first_name or "Без имени"
            
            # Получаем юзернейм или пишем, что его нет (с ID для подстраховки)
            if message.from_user.username:
                user_contact = f"@{message.from_user.username}"
            else:
                user_contact = f"нет юзернейма (ID: {chat_id})"
            
            # Чистый текст без звездочек
            admin_message = (
                "Нове питання агроному від клієнта!\n\n"
                f"Користувач: {user_name}\n"
                f"Юзернейм: {user_contact}\n"
                f"Питання: {text}"
            )
            
            # Пересылаем вопрос админу (без parse_mode, чтобы ничего не ломалось)
            try:
                bot.send_message(ADMIN_CHAT_ID, admin_message)
            except Exception as e:
                print(f"[!] Ошибка отправки админу: {e}")
            
            # Подтверждаем клиенту
            bot.send_message(
                chat_id, 
                "✅ Дякуємо! Ваше запитання передано агроному. Ми зв'яжемося з вами найближчим часом.",
                reply_markup=get_main_keyboard()і
            )
            waiting_for_question[chat_id] = False
        else:
            bot.send_message(chat_id, "Будь ласка, використовуйте кнопки меню нижче 👇", reply_markup=get_main_keyboard())

if __name__ == "__main__":
    print("🚀 Бот 'Агроаптека' запущен и ждет пользователей...")
    bot.infinity_polling()
