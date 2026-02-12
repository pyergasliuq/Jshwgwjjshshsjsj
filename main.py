from aiogram import Bot, Dispatcher, executor, types

TOKEN = "8284703353:AAFWBuW3m9Xfd6dvK58JIyOVP1WqX2DMbe4"
ALLOWED_IDS = [5733226602, 2080411409]
SITE_URL = "https://pweper.online"

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    if msg.from_user.id not in ALLOWED_IDS:
        await msg.answer("Ты не златенька 😼")
        return

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "💗 Открыть подарок",
        url=SITE_URL
    ))

    await msg.answer(
        "Держи ссылочку, дорогая 💖",
        reply_markup=kb
    )

if __name__ == "__main__":
    executor.start_polling(dp)
