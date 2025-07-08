from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.restricted import (
    add_user_id,
    remove_user_id,
    get_user_ids,
    get_admin_ids,
    increment_reject,
    get_all_users_info
)
from aiogram.types import CallbackQuery


router = Router()
simple_admin_router = router

admin_state = {}

@simple_admin_router.message(Command(commands=["start", "admin"]))
async def show_admin_panel(message: types.Message):
    user_id = message.from_user.id
    if user_id not in get_admin_ids():
        await message.answer("❌ У вас нет прав администратора.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Посмотреть пользователей", callback_data="admin_view_users")],
        [InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="admin_add_user")],
        [InlineKeyboardButton(text="➖ Удалить пользователя", callback_data="admin_remove_user")]
    ])
    await message.answer("🔧 Админ-панель", reply_markup=keyboard)


@simple_admin_router.callback_query(lambda c: c.data == "admin_view_users")
async def view_users(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in get_admin_ids():
        await callback.answer("❌ Нет прав", show_alert=True)
        return

    users_data = get_all_users_info()["users"]
    msg = "👤 <b>Пользователи</b>\n" + "\n".join(
        f"{u['id']} — {u['name']}" for u in users_data
    ) if users_data else "⚠️ Список пуст"
    await callback.message.answer(msg, parse_mode="HTML")
    await callback.answer()


@simple_admin_router.callback_query(lambda c: c.data in ["admin_add_user", "admin_remove_user"])
async def ask_user_id(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in get_admin_ids():
        await callback.answer("❌ Нет прав", show_alert=True)
        return

    action = callback.data.replace("admin_", "")
    admin_state[user_id] = action
    await callback.message.answer(f"⌨️ Введите ID пользователя, которого хотите добавить.")
    await callback.answer()


@simple_admin_router.message()
async def process_user_id(message: types.Message):
    user_id = message.from_user.id
    if user_id not in admin_state:
        return

    action = admin_state.pop(user_id)
    try:
        target_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Введите корректный ID.")
        return

    if action == "add_user":
        user = await message.bot.get_chat(target_id)
        name = user.username or user.first_name or "Без имени"
        add_user_id(target_id, name)
        await message.answer(f"✅ Пользователь {target_id} ({name}) добавлен.")
    elif action == "remove_user":
        remove_user_id(target_id)
        await message.answer(f"🗑️ Пользователь {target_id} удалён.")

@simple_admin_router.callback_query(lambda c: c.data.startswith("approve_user:"))
async def approve_user_callback(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    user = await callback.bot.get_chat(user_id)
    name = user.username or user.first_name or "Без имени"
    add_user_id(user_id, name)
    await callback.message.bot.send_message(user_id, "✅ Вам выданы права пользователя!")
    await callback.message.edit_text("👤 Доступ предоставлен пользователю.")


@simple_admin_router.callback_query(lambda c: c.data.startswith("deny_user:"))
async def deny_user_callback(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])

    increment_reject(user_id)  # ⬅️ фиксируем отказ

    try:
        await callback.message.bot.send_message(
            user_id,
            "❌ Вам отказано в доступе."
        )
    except Exception as e:
        print(f"[❌ Не удалось отправить уведомление пользователю {user_id}]: {e}")

    await callback.message.edit_text("⛔ Доступ отклонён.")
