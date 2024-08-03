from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import F
import asyncio
import string
import random
from config import TOKEN, URL
from set_default_commands import set_default_commands
from user_keyboard import phone_number_btn, menu_btn
from api import check_user_by_id, check_user_by_phone, reset_password

BOT_TOKEN = TOKEN
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class User_Phone(StatesGroup):
    phone_number = State()


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await set_default_commands(bot)
    user_id = message.from_user.id
    check_id = await check_user_by_id(user_id)
    if check_id:
        keyboard = await menu_btn()
        await message.answer("Welcome Back", reply_markup=keyboard)
    else:
        keyboard = await phone_number_btn()
        await message.answer("Telefon raqam jo'nating", reply_markup=keyboard)
        await state.set_state(User_Phone.phone_number)
        print("State set to phone_number")


@dp.message(F.content_type.in_({"contact"}))
async def contact(message: types.Message, state: FSMContext):
    contact = message.contact
    phone_number = contact.phone_number
    user_first_name = contact.first_name

    await state.update_data(phone_number=phone_number)

    check_phone = await check_user_by_phone(phone_number)
    print(5353, check_phone)

    if check_phone:
        user_id = check_phone.get('id')
        await state.update_data(phone_number=phone_number, user_id=user_id)
        print(phone_number, user_id)
        keyboard = await menu_btn()
        await message.answer(f"Thank you, {user_first_name}!", reply_markup=keyboard)
    else:
        await message.answer(f"Iltimos sayt orqali ro'yhatdan o'ting. https://oson-test.uz/",
                             disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text == "Kontaktlar")
async def display_contacts(message: types.Message):
    telephone_numbers = [
        "+1234567890",
        "+0987654321",
        "+1122334455"
    ]
    contact_info = "\n".join(telephone_numbers)
    await message.answer(f"Here are the contact numbers:\n{contact_info}", reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text == "Mening Profilim")
async def my_profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get('phone_number', 'Noma\'lum')

    my_profile = [
        f"Ism: {message.from_user.first_name}",
        f"Telefon raqam: {phone_number}"
    ]
    user_info = "\n".join(my_profile)
    await message.answer(f"Mening profilim: \n{user_info}", reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text == 'Parol Yangilash')
async def reset_password_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    phone_number = data.get('phone_number')
    print(phone_number)
    user_id = data.get("user_id")
    print(user_id)
    telegram_id = message.from_user.id
    print(telegram_id)

    random_password = generate_random_password()
    result = await reset_password(password=random_password, user_id=user_id, telegram_id=telegram_id)

    if "detail" in result:
        await message.answer(f"Parolni yangilashda xato: {result['error']}")
    else:
        await message.answer(f"Sizning yangi parolingiz: {random_password}")


@dp.message(Command(commands=["yordam"]))
async def help(message: types.Message):
    help = [
        "👨‍💻 Telegram: @aripovjr",
        "📱 Telefon: +998902220917"
    ]
    support_info = "\n".join(help)
    await message.answer(f"Bemalol murojaat qiling: \n{support_info}\"", reply_markup=ReplyKeyboardRemove())


# Start polling
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
