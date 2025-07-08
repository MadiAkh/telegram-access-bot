import os
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.restricted import get_admin_ids, get_user_ids, get_all_admins, has_exceeded_retries, get_reject_count
from .keyboards import get_keyboard_for_role, main_menu_kb

router = Router()
SUPER_ADMIN_ID = int(os.getenv("SUPER_ADMIN_ID"))

@router.message(lambda message: message.text == "🏡 Главное меню")
async def handle_main_menu(message: types.Message):
    user_id = message.from_user.id
    keyboard, text = get_keyboard_for_role(user_id, SUPER_ADMIN_ID, get_admin_ids, get_user_ids)

    if keyboard:
        await message.answer(text, reply_markup=keyboard)
    elif has_exceeded_retries(user_id):
        await message.answer("❌ Вам трижды было отказано в доступе. Повторный запрос невозможен.")
    else:
        full_name = message.from_user.full_name
        reject_count = get_reject_count(user_id)
        await message.answer(
            "⏳ Ваш ID и имя отправлены администратору на подтверждение.",
            reply_markup=main_menu_kb
        )
        for admin_id in get_all_admins():
            try:
                await message.bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"👤 Пользователь ID: `{user_id}`\n"
                        f"Имя: {full_name} просит доступ как пользователь.\n"
                        f"❌ Отказов ранее: {reject_count}"
                    ),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="✅ Дать доступ", callback_data=f"approve_user:{user_id}"),
                            InlineKeyboardButton(text="❌ Отказать", callback_data=f"deny_user:{user_id}")
                        ]
                    ]),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"[❌ Ошибка отправки админу{admin_id}]: {e}")

@router.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    keyboard, text = get_keyboard_for_role(user_id, SUPER_ADMIN_ID, get_admin_ids, get_user_ids)

    if keyboard:
        await message.answer(text, reply_markup=keyboard)
        await message.answer("Выберите действие 👆🏼",reply_markup=main_menu_kb)
    elif has_exceeded_retries(user_id):
        await message.answer("❌ Вам трижды отказано в доступе. Повторный запрос невозможен.")
    else:
        full_name = message.from_user.full_name
        reject_count = get_reject_count(user_id)
        await message.answer(
            "⏳ Ваш ID и имя отправлены администратору на подтверждение.",
            reply_markup=main_menu_kb
        )
        for admin_id in get_all_admins():
            try:
                await message.bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"👤 Пользователь ID: `{user_id}`\n"
                        f"Имя: {full_name} просит доступ как пользователь.\n"
                        f"❌ Отказов ранее: {reject_count}"
                    ),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="✅ Дать доступ", callback_data=f"approve_user:{user_id}"),
                            InlineKeyboardButton(text="❌ Отказать", callback_data=f"deny_user:{user_id}")
                        ]
                    ]),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"[❌ Ошибка отправки админу {admin_id}]: {e}")