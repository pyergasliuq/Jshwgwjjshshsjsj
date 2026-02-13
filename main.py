import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from datetime import date

TOKEN = "8284703353:AAFWBuW3m9Xfd6dvK58JIyOVP1WqX2DMbe4"
ALLOWED_IDS = [5733226602, 2080411409]
SITE_URL = "https://pweper.ru/Valentine.html?love=zlatenka"

START_DATE = date(2026, 1, 9)

bot = Bot(token=TOKEN)
dp = Dispatcher()


def days_together():
    return (date.today() - START_DATE).days


def make_gift_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💝 Открыть подарок", url=SITE_URL)]
    ])


def make_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💝 Подарок",    callback_data="gift"),
            InlineKeyboardButton(text="💗 Признание",  callback_data="love"),
        ],
        [
            InlineKeyboardButton(text="🗓 Дней вместе", callback_data="days"),
        ]
    ])


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_IDS


@dp.message(Command("start"))
async def cmd_start(msg: Message):
    if not is_allowed(msg.from_user.id):
        await msg.answer("Ты не Златенька 😼\nЭтот бот только для одной особенной девочки 💔")
        return
    days = days_together()
    await msg.answer(
        "💌 <b>Привет, моя дорогая Злата</b>\n\n"
        f"Мы вместе уже <b>{days} дней</b> — и каждый из них "
        "был подарком для меня 🌸\n\n"
        "Я приготовил кое-что особенное специально для тебя.\n"
        "Жми кнопку ниже — там твой подарок 💖",
        reply_markup=make_gift_keyboard(), parse_mode="HTML"
    )


@dp.message(Command("love"))
async def cmd_love(msg: Message):
    if not is_allowed(msg.from_user.id):
        await msg.answer("Ты не Златенька 😼")
        return
    days = days_together()
    await msg.answer(
        "💗 <b>Я тебя люблю, Злата</b>\n\n"
        f"Уже <b>{days} дней</b> ты делаешь мою жизнь ярче ✨\n\n"
        "Твоя улыбка — лучшее, что я видел.\n"
        "Твой голос — лучшее, что я слышал.\n"
        "Ты — лучшее, что со мной случилось 🌹",
        parse_mode="HTML"
    )


@dp.message(Command("days"))
async def cmd_days(msg: Message):
    if not is_allowed(msg.from_user.id):
        await msg.answer("Ты не Златенька 😼")
        return
    days = days_together()
    await msg.answer(
        f"🗓 Мы вместе уже <b>{days} дней</b>\n\n"
        f"Это <b>{days * 24}</b> часов рядом с тобой 🕐\n"
        f"И <b>{days * 24 * 60}</b> минут, когда я думал о тебе 💭\n\n"
        "И я хочу ещё очень и очень много таких дней 💕",
        parse_mode="HTML"
    )


@dp.message(Command("gift"))
async def cmd_gift(msg: Message):
    if not is_allowed(msg.from_user.id):
        await msg.answer("Ты не Златенька 😼")
        return
    await msg.answer(
        "🎁 Твой подарок — только для тебя 🩷",
        reply_markup=make_gift_keyboard(), parse_mode="HTML"
    )


@dp.message(F.text)
async def echo(msg: Message):
    if not is_allowed(msg.from_user.id):
        await msg.answer("Ты не Златенька 😼")
        return
    text = msg.text.lower()
    if any(w in text for w in ["люблю", "love", "люб", "обожа"]):
        await msg.answer(
            "💖 Я тебя тоже люблю, моя дорогая Злата 💖\n\nБольше, чем ты думаешь ✨",
            parse_mode="HTML"
        )
        return
    if any(w in text for w in ["скуч", "жду", "хочу тебя"]):
        await msg.answer(
            "🥺 Я тоже скучаю по тебе...\n\nНо зато держи свой подарок, пока не встретимся 💝",
            reply_markup=make_gift_keyboard(), parse_mode="HTML"
        )
        return
    await msg.answer(
        "Привет, моя дорогая ✨\n\nЧто ты хочешь посмотреть?",
        reply_markup=make_menu_keyboard(), parse_mode="HTML"
    )


@dp.callback_query()
async def callback(call: CallbackQuery):
    if not is_allowed(call.from_user.id):
        await call.answer("Ты не Златенька 😼", show_alert=True)
        return
    days = days_together()
    if call.data == "gift":
        await call.message.answer("🎁 Твой подарок — только для тебя 🩷", reply_markup=make_gift_keyboard(), parse_mode="HTML")
    elif call.data == "love":
        await call.message.answer(
            f"💗 <b>Я тебя люблю, Злата</b>\n\nУже {days} дней ты делаешь мою жизнь ярче ✨\nТы — лучшее, что со мной случилось 🌹",
            parse_mode="HTML"
        )
    elif call.data == "days":
        await call.message.answer(
            f"🗓 Мы вместе уже <b>{days} дней</b>\nЭто <b>{days * 24}</b> часов рядом с тобой 🕐\nИ я хочу ещё очень много таких дней 💕",
            parse_mode="HTML"
        )
    await call.answer()


async def main():
    print("💗 Бот для Златеньки запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
