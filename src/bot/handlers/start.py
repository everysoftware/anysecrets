from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.fsm import LoginGroup, RegisterGroup
from src.bot.keyboards import LOGIN_KB, REG_KB
from src.bot.middlewares import RegisterCheck
from src.cache import Cache
from .commands import BOT_COMMANDS_STR

router = Router(name='start')

router.message.middleware(RegisterCheck())


@router.message(Command('start'))
async def start(
        message: types.Message,
        state: FSMContext,
        cache: Cache,
) -> Message:
    if await cache.get(f'user_exists:{message.from_user.id}', int):
        message = await message.answer(
            'Привет, {first_name} {last_name}, мы тебя помним! 😊 '
            'Нажми на кнопку, чтобы войти в аккаунт 👇'.format(
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name),
            reply_markup=LOGIN_KB)
        await state.set_state(LoginGroup.waiting_for_click)
    else:
        message = await message.answer(
            'Привет, я бот Secrets — твой быстрый и безопасный менеджер паролей 😊 '
            'Нажми на кнопку, чтобы создать аккаунт 👇',
            reply_markup=REG_KB)
        await state.set_state(RegisterGroup.waiting_for_click)

    return message


@router.message(Command('help'))
async def help_(message: types.Message) -> Message:
    return await message.answer('<b>Команды бота:</b>\n\n' + BOT_COMMANDS_STR)


@router.message(Command('author'))
async def author(message: types.Message) -> Message:
    return await message.answer('Автор бота: @ivanstasevich 👨‍💻')
