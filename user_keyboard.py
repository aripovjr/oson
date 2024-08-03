from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


async def phone_number_btn():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="📱 Telefon raqam yuborish", request_contact=True)
    )
    return keyboard.as_markup(resize_keyboard=True)


async def menu_btn():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="Mening Profilim"),
        KeyboardButton(text="Kontaktlar"),
        KeyboardButton(text="Parol Yangilash")
    )
    return keyboard.as_markup(resize_keyboard=True)
