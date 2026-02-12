from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date

TOKEN = "8284703353:AAFWBuW3m9Xfd6dvK58JIyOVP1WqX2DMbe4"
ALLOWED_IDS = [5733226602, 2080411409]
SITE_URL = "https://pweper.online/?love=zlatenka"

# Дата начала отношений
START_DATE = date(2026, 1, 9)

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


def days_together():
    return (date.today() - START_DATE).days


def make_gift_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💝 Открыть подарок", url=SITE_URL))
    return kb


def is_allowed(msg: types.Message) -> bool:
    if msg.from_user.id not in ALLOWED_IDS:
        return False
    return True


# ─── /start ───────────────────────────────────────────────────────────────────
@dp.message_handler(commands=["start"])
async def cmd_start(msg: types.Message):
    if not is_allowed(msg):
        await msg.answer("Ты не Златенька 😼\nЭтот бот только для одной особенной девочки 💔")
        return

    days = days_together()

    text = (
        "💌 <b>Привет, моя дорогая Злата</b>\n\n"
        f"Мы вместе уже <b>{days} дней</b> — и каждый из них "
        "был подарком для меня 🌸\n\n"
        "Я приготовил кое-что особенное специально для тебя.\n"
        "Жми кнопку ниже — там твой подарок 💖"
    )

    await msg.answer(text, reply_markup=make_gift_keyboard())


# ─── /love ────────────────────────────────────────────────────────────────────
@dp.message_handler(commands=["love"])
async def cmd_love(msg: types.Message):
    if not is_allowed(msg):
        await msg.answer("Ты не Златенька 😼")
        return

    days = days_together()

    text = (
        "💗 <b>Я тебя люблю, Злата</b>\n\n"
        f"Уже <b>{days} дней</b> ты делаешь мою жизнь ярче ✨\n\n"
        "Твоя улыбка — лучшее, что я видел.\n"
        "Твой голос — лучшее, что я слышал.\n"
        "Ты — лучшее, что со мной случилось 🌹"
    )

    await msg.answer(text)


# ─── /days ────────────────────────────────────────────────────────────────────
@dp.message_handler(commands=["days"])
async def cmd_days(msg: types.Message):
    if not is_allowed(msg):
        await msg.answer("Ты не Златенька 😼")
        return

    days = days_together()

    text = (
        f"🗓 Мы вместе уже <b>{days} дней</b>\n\n"
        f"Это <b>{days * 24}</b> часов рядом с тобой 🕐\n"
        f"И <b>{days * 24 * 60}</b> минут, когда я думал о тебе 💭\n\n"
        "И я хочу ещё очень и очень много таких дней 💕"
    )

    await msg.answer(text)


# ─── /gift ────────────────────────────────────────────────────────────────────
@dp.message_handler(commands=["gift"])
async def cmd_gift(msg: types.Message):
    if not is_allowed(msg):
        await msg.answer("Ты не Златенька 😼")
        return

    text = (
        "🎁 <b>Твой подарок ждёт тебя</b>\n\n"
        "Я вложил в него всё, что чувствую к тебе.\n"
        "Открывай — он только для тебя 🩷"
    )

    await msg.answer(text, reply_markup=make_gift_keyboard())


# ─── Любое другое сообщение ───────────────────────────────────────────────────
@dp.message_handler()
async def echo(msg: types.Message):
    if not is_allowed(msg):
        await msg.answer("Ты не Златенька 😼")
        return

    text = msg.text.lower() if msg.text else ""

    # Если пишет что-то о любви
    if any(w in text for w in ["люблю", "love", "люб", "обожа"]):
        await msg.answer(
            "💖 Я тебя тоже люблю, моя дорогая Злата 💖\n\n"
            "Больше, чем ты думаешь ✨"
        )
        return

    # Если скучает
    if any(w in text for w in ["скуч", "жду", "хочу тебя"]):
        await msg.answer(
            "🥺 Я тоже скучаю по тебе...\n\n"
            "Но зато держи свой подарок, пока не встретимся 💝",
            reply_markup=make_gift_keyboard()
        )
        return

    # Обычное сообщение — напоминаем команды
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💝 Подарок",  callback_data="gift"),
        InlineKeyboardButton("💗 Признание", callback_data="love"),
        InlineKeyboardButton("🗓 Дней вместе", callback_data="days"),
    )

    await msg.answer(
        "Привет, моя дорогая ✨\n\n"
        "Что ты хочешь посмотреть?",
        reply_markup=kb
    )


# ─── Кнопки (callback) ────────────────────────────────────────────────────────
@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    if call.from_user.id not in ALLOWED_IDS:
        await call.answer("Ты не Златенька 😼", show_alert=True)
        return

    days = days_together()

    if call.data == "gift":
        await call.message.answer(
            "🎁 Твой подарок — только для тебя 🩷",
            reply_markup=make_gift_keyboard()
        )
    elif call.data == "love":
        await call.message.answer(
            "💗 <b>Я тебя люблю, Злата</b>\n\n"
            f"Уже {days} дней ты делаешь мою жизнь ярче ✨\n"
            "Ты — лучшее, что со мной случилось 🌹"
        )
    elif call.data == "days":
        await call.message.answer(
            f"🗓 Мы вместе уже <b>{days} дней</b>\n"
            f"Это <b>{days * 24}</b> часов рядом с тобой 🕐\n"
            "И я хочу ещё очень много таких дней 💕"
        )

    await call.answer()


if __name__ == "__main__":
    print("💗 Бот для Златеньки запущен...")
    executor.start_polling(dp, skip_updates=True)
