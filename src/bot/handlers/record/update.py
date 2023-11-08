from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.encryption import Encryption
from src.bot.fsm import RecordGroup, UpdateRecordGroup
from src.bot.handlers.activities import UpdateRecordActivity, TypeNewDataActivity, ShowRecordControlActivity
from src.bot.handlers.record.show import show_record_cp
from src.bot.keyboards.record import UPDATE_RECORD_KB
from src.db import Database
from src.db.models import Comment

router = Router(name='update_record')


@router.callback_query(F.data == 'update_record', RecordGroup.viewing_record)
async def update_record(call: types.CallbackQuery, state: FSMContext) -> None:
    await ShowRecordControlActivity.finish_callback(
        call, state
    )
    await UpdateRecordActivity.start_callback(
        call, state,
        RecordGroup.editing_record,
        text='Выбери элемент, который хочешь изменить в записи 🔽',
        reply_markup=UPDATE_RECORD_KB
    )


@router.callback_query(F.data == 'update_title', RecordGroup.editing_record)
async def type_title(call: types.CallbackQuery, state: FSMContext) -> None:
    await TypeNewDataActivity.start_callback(
        call, state,
        new_state=UpdateRecordGroup.updating_title,
        text='Введи новое имя сайта ⬇️'
    )


@router.message(UpdateRecordGroup.updating_title)
async def update_title(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await TypeNewDataActivity.switch(
            message, state,
            user_data=user_data,
            text='Имя веб-сайта не может быть длиннее 64 символов. Введи новое имя сайта ⬇️',
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.title = text
        await db.record.merge(record)

    await TypeNewDataActivity.finish(
        message, state,
        user_data=user_data,
        new_state=RecordGroup.editing_record,
        text='Запись успешно изменена ✅'
    )


@router.callback_query(F.data == 'update_username', RecordGroup.editing_record)
async def type_username(call: types.CallbackQuery, state: FSMContext) -> None:
    await TypeNewDataActivity.start_callback(
        call, state,
        new_state=UpdateRecordGroup.updating_username,
        text='Введи новое имя пользователя ⬇️'
    )


@router.message(UpdateRecordGroup.updating_username)
async def update_username(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await TypeNewDataActivity.switch(
            message, state,
            user_data=user_data,
            text='Имя пользователя не может быть длиннее 64 символов. Введи новое имя пользователя ⬇️',
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.username = Encryption.encrypt(text, user_data['master'], record.salt)
        await db.record.merge(record)

    await TypeNewDataActivity.finish(
        message, state,
        user_data=user_data,
        new_state=RecordGroup.editing_record,
        text='Запись успешно изменена ✅'
    )


@router.callback_query(F.data == 'update_password', RecordGroup.editing_record)
async def type_password(call: types.CallbackQuery, state: FSMContext) -> None:
    await TypeNewDataActivity.start_callback(
        call, state,
        new_state=UpdateRecordGroup.updating_password,
        text='Введи новый пароль ⬇️'
    )


@router.message(UpdateRecordGroup.updating_password)
async def update_password(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await TypeNewDataActivity.switch(
            message, state,
            user_data=user_data,
            text='Пароль не может быть длиннее 64 символов. Введи новый пароль ⬇️',
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.password_ = Encryption.encrypt(text, user_data['master'], record.salt)
        await db.record.merge(record)

    await TypeNewDataActivity.finish(
        message, state,
        user_data=user_data,
        new_state=RecordGroup.editing_record,
        text='Запись успешно изменена ✅',
    )


@router.callback_query(F.data == 'update_url', RecordGroup.editing_record)
async def type_url(call: types.CallbackQuery, state: FSMContext) -> None:
    await TypeNewDataActivity.start_callback(
        call, state,
        new_state=UpdateRecordGroup.updating_url,
        text='Введи новый веб-сайт ⬇️'
    )


@router.message(UpdateRecordGroup.updating_url)
async def update_url(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await TypeNewDataActivity.switch(
            message, state,
            user_data=user_data,
            text='Веб-сайт не может быть длиннее 64 символов. Введи новый веб-сайт ⬇️'
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.url = text
        await db.record.merge(record)

    await TypeNewDataActivity.finish(
        message, state,
        user_data=user_data,
        new_state=RecordGroup.editing_record,
        text='Запись успешно изменена ✅',
    )


@router.callback_query(F.data == 'update_comment', RecordGroup.editing_record)
async def type_comment(call: types.CallbackQuery, state: FSMContext) -> None:
    await TypeNewDataActivity.start(
        call.message, state,
        new_state=UpdateRecordGroup.updating_comment,
        text='Введи новый комментарий ⬇️'
    )

    await call.answer()


@router.message(UpdateRecordGroup.updating_comment)
async def update_comment(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 256:
        return await TypeNewDataActivity.switch(
            message, state,
            user_data=user_data,
            text='Комментарий не может быть длиннее 256 символов. Введи новый комментарий ⬇️'
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])

        if record.comment is None:
            record.comment = db.comment.new(text=text)
            await db.record.merge(record)
        else:
            comment: Comment = record.comment
            comment.text = text
            await db.comment.merge(comment)

    await TypeNewDataActivity.finish(
        message, state,
        user_data=user_data,
        new_state=RecordGroup.editing_record,
        text='Запись успешно изменена ✅',
    )


@router.callback_query(F.data == 'back', RecordGroup.editing_record)
async def back(call: types.CallbackQuery, state: FSMContext, arq_redis: ArqRedis) -> None:
    await UpdateRecordActivity.finish_callback(
        call, state,
    )

    await show_record_cp(call.message, state, arq_redis)
