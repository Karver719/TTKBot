import json


with open('lemmas.json', 'r', encoding='utf-8') as f:
    lemmas = json.load(f)


def search(text):
    for word in text.split():
        for category, lemma_list in lemmas.items():
            if word in lemma_list:
                if category == 'greetings':
                    return "Приветствую"
                elif category == "farewells":
                    return "Досвидания"
                elif category == "gratitude":
                    return "Всегда пожалуйста"
                elif category == "insults":
                    return "Я вас не знаю"
                elif category == "apruve":
                    return True


import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest



#Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Войти как клиент ТТК", callback_data='ttk_command'),
            InlineKeyboardButton("Заключить новый договор", callback_data='dogovor_command'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Привет! Я простой бот. Выберите действие:',
        reply_markup=reply_markup
    )


# Обработчик команды /ttk
async def ttk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Добро пожалоавть Клиент ТТК"
    await update.message.reply_text(help_text)


# Обработчик команды /dogovor
async def dogovor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = "Вы выбрали заключить новый договор"
    await update.message.reply_text(about_text)


# Обработчик нажатий на кнопки
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    try:
        await query.answer()  # Отвечаем на callback query

        # Подготавливаем новое сообщение и клавиатуру
        new_message = ""
        show_back_button = True

        if query.data == 'ttk_command':
            new_message = "Добро пожалоавть Клиент ТТК"
        elif query.data == 'dogovor_command':
            new_message = "Вы выбрали заключить новый договор"
        elif query.data == 'info_command':
            new_message = "Это информационное сообщение."
        elif query.data == 'back_to_menu':
            show_back_button = False
            new_message = 'Выберите действие:'
            keyboard = [
                [
                    InlineKeyboardButton("Войти как клиент ТТК", callback_data='ttk_command'),
                    InlineKeyboardButton("Заключить новый договор", callback_data='dogovor_command'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(new_message, reply_markup=reply_markup)
            return

        # Добавляем кнопку "Назад"
        keyboard = [[InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')]] if show_back_button else []
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем обновленное сообщение
        await query.edit_message_text(
            text=new_message,
            reply_markup=reply_markup
        )

    except BadRequest as e:
        pass



load_dotenv()
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
application = Application.builder().token(TELEGRAM_TOKEN).build()


def stop_buttons():
    application.shutdown()

def buttons():

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ttk", ttk_command))
    application.add_handler(CommandHandler("dogovor", dogovor_command))

    # Добавляем обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_click))
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)
