import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from config import settings
from settings import PHONE, ADDRESS, HOURS, INFO, CONTACTS
from services import SERVICES, PRICES


def menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 Услуги", callback_data="services")],
        [InlineKeyboardButton(text="💰 Цены", callback_data="prices")],
        [
            InlineKeyboardButton(text="ℹ️ О нас", callback_data="info"),
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
        ],
        [InlineKeyboardButton(text="📝 Записаться", callback_data="booking")],
    ])


def services_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=cb)]
        for cb, (title, _) in SERVICES.items()
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Меню", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Здравствуйте! 👋\nЯ бот автосервиса *VOLVO 7* — специализируемся "
        "на Volvo и Geely.\nВыберите раздел:",
        parse_mode="Markdown",
        reply_markup=menu_kb(),
    )


@dp.callback_query(F.data == "menu")
async def back_to_menu(cb: CallbackQuery):
    await cb.message.answer("Главное меню:", reply_markup=menu_kb())
    await cb.answer()


@dp.callback_query(F.data == "info")
async def show_info(cb: CallbackQuery):
    await cb.message.answer(INFO, parse_mode="Markdown", reply_markup=menu_kb())
    await cb.answer()


@dp.callback_query(F.data == "contacts")
async def show_contacts(cb: CallbackQuery):
    await cb.message.answer(
        CONTACTS,
        parse_mode="Markdown",
        reply_markup=menu_kb(),
    )
    await cb.answer()


@dp.callback_query(F.data == "booking")
async def show_booking(cb: CallbackQuery):
    await cb.message.answer(
        f"📝 *Запись на сервис*\n\n"
        f"📞 Позвоните нам: [{PHONE}](tel:{PHONE.replace('+', '')})\n\n"
        f"⏰ Время работы: {HOURS}\n\n"
        f"📍 Адрес: {ADDRESS}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Наш сайт", url="https://volvo7.ru/")],
            [InlineKeyboardButton(text="⬅️ Меню", callback_data="menu")],
        ]),
    )
    await cb.answer()


@dp.callback_query(F.data == "services")
async def show_services(cb: CallbackQuery):
    await cb.message.answer(
        "🛠 *Услуги — выберите категорию:*",
        parse_mode="Markdown",
        reply_markup=services_kb(),
    )
    await cb.answer()


@dp.callback_query(F.data.startswith("serv_"))
async def show_service(cb: CallbackQuery):
    title, items = SERVICES[cb.data]
    text = f"*{title}*\n\n" + "\n".join(f"• {i}" for i in items)
    await cb.message.answer(text, parse_mode="Markdown", reply_markup=services_kb())
    await cb.answer()


@dp.callback_query(F.data == "prices")
async def show_prices(cb: CallbackQuery):
    lines = [f"*{cat}*\n{desc}\n" for cat, desc in PRICES.items()]
    await cb.message.answer(
        "💰 *Цены*\n\n" + "\n".join(lines) +
        "\n⚠️ Окончательная стоимость определяется после осмотра "
        "автомобиля и диагностики — и фиксируется до начала работ.",
        parse_mode="Markdown",
        reply_markup=menu_kb(),
    )
    await cb.answer()


bot = Bot(token=settings.bot_token)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
