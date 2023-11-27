from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.models import Record


async def get_storage_kb(
        records: list[Record]
) -> InlineKeyboardMarkup:
    # async with db.session.begin():
    #     user = await db.user.get(from_user.id, options=[selectinload(User.records)])
    #     records = user.records
    #
    #     records_len = len(user.records)
    #
    #     if pattern:
    #         # TODO: Оптимизировать поиск по URL
    #         records = [record for record in records if pattern in record.url]
    #
    #     if count > 0:
    #         offset = min(records_len, offset + count)
    #     else:
    #         offset = max(0, offset + count)
    #
    #     if records_len > 0:
    #         offset %= records_len

    builder = InlineKeyboardBuilder()

    # TODO: Оптимизировать скроллинг паролей
    for record in records:
        builder.add(InlineKeyboardButton(
            text=record.title,
            callback_data=f'show_record_{record.id}'
        ))

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(text='🔼', callback_data='up'),
        InlineKeyboardButton(text='Назад ◀️', callback_data='back'),
        InlineKeyboardButton(text='🔽', callback_data='down')
    )

    return builder.as_markup(resize_keyboard=True)


RECORD_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить ✏️', callback_data='update_record'),
            InlineKeyboardButton(text='Удалить ❌', callback_data='delete_record')
        ],
        [
            InlineKeyboardButton(text='Назад ◀️', callback_data='back')
        ],
    ]
)

UPDATE_RECORD_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Имя веб-сайта 🌐', callback_data='update_title'),
            InlineKeyboardButton(text='Имя пользователя 👨', callback_data='update_username'),

        ],
        [
            InlineKeyboardButton(text='Пароль 🔑', callback_data='update_password'),
            InlineKeyboardButton(text='Веб-сайт 🔗', callback_data='update_url'),
        ],
        [
            InlineKeyboardButton(text='Комментарий 💬', callback_data='update_comment'),
            InlineKeyboardButton(text='Назад ◀️', callback_data='back')
        ],
    ]
)
