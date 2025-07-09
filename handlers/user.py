import os
from aiogram import Router, types
from services.excel_writer import save_avr_to_excel
from aiogram.types import FSInputFile  
from middlewares.restricted import is_allowed_user


router  = Router()
user_router = router



@user_router.callback_query(lambda call: call.data == "get_file")
async def handle_get_file_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # 🔒 Проверка доступа
    if not is_allowed_user(user_id):
        await callback.message.answer("❌ У вас больше нет доступа к получению файлов.")
        await callback.answer()
        return

    file_path = f"temp_output_{user_id}.xlsx"
    print(f"📥 Получен запрос от пользователя {user_id}")

    await save_avr_to_excel(file_path)

    if os.path.exists(file_path):
        print(f"📤 Отправляем файл: {file_path}")
        await callback.message.answer_document(FSInputFile(file_path), caption="✅ Вот ваш файл.")
        os.remove(file_path)
        print("🗑️ Файл удалён после отправки.")
    else:
        print("❌ Файл не найден после генерации.")
        await callback.message.answer("❌ Не удалось создать файл.")

    await callback.answer() 

 