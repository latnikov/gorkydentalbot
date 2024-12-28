from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command  # Новый механизм фильтрации
import asyncio

# Токен бота от BotFather
TOKEN = "7304345177:AAG_WmqN2UzKfZfMA33z6kx6wf9eA36iyoE"

# ID менеджера, куда отправлять заявки
MANAGER_ID = 7325952862

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Простая клавиатура
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True
)

async def remove_webhook():
    bot = Bot(token="7304345177:AAG_WmqN2UzKfZfMA33z6kx6wf9eA36iyoE")
    await bot.delete_webhook()
    print("Webhook удален")
    await bot.session.close()

asyncio.run(remove_webhook())

# Роутер для обработки сообщений
router = Router()

@router.message(Command("start"))  # Используем Command вместо commands=["start"]
async def start_handler(message: Message):
    await message.answer("Здравствуйте! Напишите, пожалуйста, ваш вопрос.", reply_markup=menu_keyboard)

@router.message()
async def message_handler(message: Message):
    text = message.text.lower()

    if text in ["здравствуйте", "добрый день", "привет"]:
        await message.answer("Добрый день! Напишите, пожалуйста, ваш вопрос.")
    elif "подожди" in text:
        await message.answer("Хорошо, я подожду.")
    else:
        # Отправляем заявку менеджеру
        await bot.send_message(
            MANAGER_ID,
            f"Поступила новая заявка от @{message.from_user.username or message.from_user.first_name}: {text}"
        )
        await message.answer("Понял вас, перевожу на менеджера.")

# Регистрация роутеров
dp.include_router(router)

# Главная функция для запуска бота
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
