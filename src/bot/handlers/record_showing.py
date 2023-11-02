from datetime import timedelta
from html import escape

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.encryption import decrypt_data
from src.bot.filters import RegisterFilter
from src.bot.handlers.confirmation import confirm_master
from src.bot.handlers.forwarding import redirects
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup
from src.bot.structures.keyboards import RECORD_KB
from src.db import Database
from src.db.models import Record

router = Router(name='record_showing')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.callback_query(F.data.startswith('show_record'), MainGroup.viewing_storage)
@router.callback_query(F.data.startswith('show_record'), MainGroup.viewing_record)
async def show_record_confirmation(callback: types.CallbackQuery, state: FSMContext) -> None:
    args = callback.data.split('_')
    try:
        record_id = int(args[2])
    except (IndexError, ValueError):
        pass
    else:
        await state.update_data(record_id=record_id)
        await confirm_master(callback.message, state, show_record, True)
    finally:
        await callback.answer()


@redirects.register_redirect
async def show_record(msg: types.Message, state: FSMContext, db: Database, arq_redis: ArqRedis) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record: Record = await db.record.get(user_data['record_id'])
        title = escape(record.title)
        url = escape(record.url) if record.url is not None else ''
        username = escape(decrypt_data(record.username, user_data['master'], record.salt))
        password = escape(decrypt_data(record.password_, user_data['master'], record.salt))
        comment = escape(record.comment.text) if record.comment is not None else ''

    record_msg = await msg.answer(
        f'<b>{title}</b>\n\n'
        f'👨 Имя пользователя: <code>{username}</code>\n'
        f'🔑 Пароль: <code>{password}</code>\n'
        f'🔗 Веб-сайт: {url}\n'
        f'💬 Комментарий: <tg-spoiler>{comment}</tg-spoiler>\n\n'
    )

    cp_msg = await msg.answer(
        'Ты в меню управления записью. Выбери действие 🔽',
        reply_markup=RECORD_KB
    )

    await arq_redis.enqueue_job(
        'delete_record_message',
        _defer_by=timedelta(minutes=2),
        chat_id=msg.from_user.id,
        record_msg_id=record_msg.message_id,
        cp_msg_id=cp_msg.message_id
    )

    await state.clear()

    await state.set_state(MainGroup.viewing_record)
    await state.update_data(record_id=user_data['record_id'])
    await state.update_data(record_msg_id=record_msg.message_id)
