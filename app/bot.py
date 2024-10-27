import os
import logging
from dotenv import load_dotenv
from handlers import dp, bot


load_dotenv()
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')

# Отладочные сообщения
print(f"Loaded TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")
if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN is not set")




logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)



if __name__ == "__main__":
    # Запуск бота
    print("Запуск бота")
    try:
        dp.run_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        pass
