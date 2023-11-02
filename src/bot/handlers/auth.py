from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import RegisterGroup, LoginGroup
from src.bot.structures.keyboards import LOGIN_KB
from src.cache import Cache
from src.db import Database
from .additional import edit_last_msg, update_last_msg, delete_last_msg
from .main import show_main_menu

auth_router = Router(name='auth')
auth_router.message.middleware(DatabaseMd())


@auth_router.message(F.text == 'Регистрация ✔️', RegisterGroup.waiting_for_click)
async def reg_button_step(msg: types.Message, state: FSMContext) -> None:
    sent_msg = await msg.answer('<b>Регистрация. Шаг 1</b>\n\nПридумай надежный пароль ⬇️')
    await state.set_state(RegisterGroup.entering_password)
    await update_last_msg(sent_msg, state)


@auth_router.message(RegisterGroup.entering_password)
async def reg_entering_password(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(password=msg.text)
    await msg.delete()

    user_data = await state.get_data()
    await edit_last_msg(bot, user_data, state,
                        '<b>Регистрация. Шаг 2</b>\n\nПридумай надежный мастер-пароль ⬇️\n\n<b><i>Мастер-пароль '
                        'даёт доступ ко всем вашим паролям. Держите его в секрете ❗️</i></b>')
    await state.set_state(RegisterGroup.entering_master)


@auth_router.message(RegisterGroup.entering_master)
async def reg_entering_master(
        msg: types.Message,
        state: FSMContext,
        db: Database,
        bot: Bot,
        cache: Cache
) -> None:
    user_data = await state.get_data()
    user = msg.from_user

    if user is None:
        return

    async with db.session.begin():
        await db.user.register(
            db=db,
            cache=cache,
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
            password=user_data['password'],
            master=msg.text,
        )

    await msg.delete()
    await delete_last_msg(bot, user_data)

    await msg.answer('Регистрация успешно завершена! Ты можешь начать пользование менеджером 😊\n\n'
                     'Нажми на кнопку ниже, чтобы авторизоваться 👇',
                     reply_markup=LOGIN_KB)
    await state.clear()
    await state.set_state(LoginGroup.waiting_for_click)


@auth_router.message(F.text == 'Авторизация 😇', LoginGroup.waiting_for_click)
async def login_button_step(msg: types.Message, state: FSMContext) -> None:
    sent_msg = await msg.answer('Введи пароль ⬇️')
    await state.set_state(LoginGroup.entering_password)
    await update_last_msg(sent_msg, state)


@auth_router.message(LoginGroup.entering_password)
async def login_entering_password(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    await msg.delete()

    user_data = await state.get_data()

    async with db.session.begin():
        if await db.user.login(msg.from_user, msg.text):
            await delete_last_msg(bot, user_data)
            await state.clear()
            await msg.answer('Успешная авторизация ✅')

            await show_main_menu(msg, state)
        else:
            await edit_last_msg(bot, user_data, state, 'Неверный пароль. Попробуй ещё раз ⬇️')
