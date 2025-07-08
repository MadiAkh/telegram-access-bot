from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Постоянная reply-кнопка "Главное меню"
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏡 Главное меню")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие..."
)

# Универсальный выбор inline-кнопок в зависимости от роли
def get_keyboard_for_role(user_id, super_admin_id, get_admin_ids, get_user_ids):
    if user_id == super_admin_id:
        return (
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👀 Посмотреть всех", callback_data="view_all")],
                [InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="add_user")],
                [InlineKeyboardButton(text="🗑️ Удалить пользователя", callback_data="remove_user")],
                [InlineKeyboardButton(text="➕ Добавить админа", callback_data="add_admin")],
                [InlineKeyboardButton(text="🗑️ Удалить админа", callback_data="remove_admin")]
            ]),
            "🔧 SUPER ADMIN-панель"
        )

    elif user_id in get_admin_ids():
        return (
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👥 Посмотреть пользователей", callback_data="admin_view_users")],
                [InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="add_user")],
                [InlineKeyboardButton(text="➖ Удалить пользователя", callback_data="remove_user")]
            ]),
            "🔧 Админ-панель"
        )

    elif user_id in get_user_ids():
        return (
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📄 Получить файл", callback_data="get_file")]
            ]),
            "👤 Вы вошли как пользователь. Добро пожаловать!"
        )

    return None, None
