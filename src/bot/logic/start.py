from html import escape as e

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.commands import BOT_COMMANDS_STR
from src.bot.fsm import LoginGroup, RegisterGroup
from src.bot.keyboards.auth import REG_KB
from src.db import Database
from src.db.enums import UserRole
from src.db.models import User
from ..middlewares import DatabaseMd

router = Router()

router.message.middleware(DatabaseMd())


@router.message(Command('start'))
async def start(
        message: types.Message,
        state: FSMContext,
        db: Database
) -> Message:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id)

        if user is None:
            user = db.user.new(User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
            ))

    match user.role:
        case UserRole.GUEST:
            message = await message.answer(
                'Добро пожаловать! Я бот, который помогает быстро и безопасно управлять паролями! 😊 '
                'Давайте создадим аккаунт, для этого нажмите на кнопку 👇',
                reply_markup=REG_KB)
            await state.set_state(RegisterGroup.in_lobby)
        case UserRole.USER:
            message = await message.answer(
                f'Добро пожаловать, {e(user.first_name)} {e(user.last_name)}! 😊 '
                f'Чтобы войти в аккаунт, введите пароль ⬇️',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(LoginGroup.type_password)
        case UserRole.ADMIN:
            message = await message.answer(
                f'Добро пожаловать, супер-кот {e(user.first_name)} {e(user.last_name)}! 😊'
                f'Чтобы войти в аккаунт, введите пароль ⬇️',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(LoginGroup.type_password)
        case _:
            raise ValueError(f'Unknown user role: {user.role}')

    return message


@router.message(Command('help'))
async def help_(message: types.Message) -> Message:
    return await message.answer('<b>Что может бот?</b>\n\n' + BOT_COMMANDS_STR)


@router.message(Command('about'))
async def author(message: types.Message) -> Message:
    return await message.answer(
        '<b>Менеджер паролей Secrets</b>\n\n 👨‍💻 '
        'Разработчик: @ivanstasevich'
    )
