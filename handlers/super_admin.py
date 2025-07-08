import os
from aiogram import Router, types 
from middlewares.restricted import (
    add_user_id, remove_user_id,
    add_admin_id, remove_admin_id,
    get_admin_ids, get_user_ids,
    is_super_admin, get_all_users_info
)

SUPER_ADMIN_ID = int(os.getenv("SUPER_ADMIN_ID"))
router = Router()
super_admin_router = router

@super_admin_router.callback_query(lambda c: c.data == "view_all")
async def view_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if not is_super_admin(user_id):
        await callback.message.answer("❌ Только SUPER ADMIN может это сделать.")
        return

    data = get_all_users_info()
    admins = data["admins"]
    users = data["users"]

    msg = f"👑 <b>SUPER ADMIN:</b>\n{SUPER_ADMIN_ID}\n\n"
    msg += "👮‍♂️ <b>Админы</b>\n"
    msg += "\n".join(
        f"{a.get('id', '❌нет id')} — {a.get('name', '❌нет name')}"
    for a in admins if isinstance(a, dict)
) + "\n\n"
    msg += "👤 <b>Пользователи</b>\n" + "\n".join(f"{u['id']} — {u['name']}" for u in users)

    await callback.message.answer(msg, parse_mode="HTML")
    await callback.answer()

@super_admin_router.callback_query(lambda c: c.data in ["add_user", "remove_user", "add_admin", "remove_admin"])
async def ask_id(callback: types.CallbackQuery):
    action = callback.data
    router_data[callback.from_user.id] = action

    # Формируем текст в зависимости от действия
    action_texts = {
        "add_user":     ("➕  Введите ID Пользователя, которого хотите добавить"),
        "remove_user":  ("🗑️  Введите ID Пользователя, которого хотите удалить"),
        "add_admin":    ("➕  Введите ID Админа, которого хотите добавить"),
        "remove_admin": ("🗑️  Введите ID Админа, которого хотите удалить"),
    }

    rus_text = action_texts.get(action, ("Введите ID"))

    await callback.message.answer(f"{rus_text}")
    await callback.answer()

router_data = {}

@super_admin_router.message()
async def process_id_input(message: types.Message):
    user_id = message.from_user.id
    if user_id not in router_data:
        return

    action = router_data[user_id]
    try:
        target_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Введите корректный числовой ID без букв, повторно:")
        return
    if action == "add_user":
        user = await message.bot.get_chat(target_id)
        name = user.username or user.first_name or "Без имени"
        add_user_id(target_id, name)
        await message.answer(f"✅ Пользователь с ID {target_id} ({name}) добавлен.")

    elif action == "remove_user":
        if target_id in get_admin_ids():
            await message.answer("❌ Этот ID принадлежит админу, а не пользователю.")
            return
        if target_id not in get_user_ids():
            await message.answer("❌ Такого ID нет в списке пользователей.")
            return
        remove_user_id(target_id)
        await message.answer(f"🗑️ Пользователь с ID {target_id} удалён.")
        try:
            await message.bot.send_message(
                target_id,
                "⚠️ Вы больше не являетесь пользователем, вам закрыт доступ. По вопросам обратитесь к администратору бота."
            )
        except Exception as e:
            print(f"[❌ Не удалось отправить уведомление пользователю {target_id}]: {e}")

    elif action == "add_admin":
        user = await message.bot.get_chat(target_id)
        name = user.username or user.first_name or "Без имени"
        add_admin_id(target_id, name)
        await message.answer(f"✅ Админ с ID {target_id} ({name}) добавлен.")

    elif action == "remove_admin":
        if is_super_admin(target_id):
            await message.answer("❌ Нельзя удалить SUPER ADMIN.")
            return
        if target_id in get_user_ids():
            await message.answer("❌ Этот ID принадлежит пользователю, а не админу.")
            return
        if target_id not in get_admin_ids():
            await message.answer("❌ Такого ID нет в списке админов.")
            return
        remove_admin_id(target_id)
        await message.answer(f"🗑️ Админ с ID {target_id} удалён.")
        try:
            await message.bot.send_message(
                target_id,
                "⚠️ Вы больше не являетесь админом этого бота, вам закрыт доступ. По вопросам обратитесь к супер-администратору бота."
            )
        except Exception as e:
            print(f"[❌ Не удалось отправить уведомление админу {target_id}]: {e}")

    router_data.pop(user_id)
