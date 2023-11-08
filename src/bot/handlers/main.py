from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.fsm import RecordGroup
from src.bot.filters import RegisterFilter
from src.bot.fsm import MainGroup
from src.bot.handlers.start import generate
from src.bot.keyboards.main import MAIN_MENU_KB
from src.bot.keyboards.user import PROFILE_KB
from src.bot.middlewares import DatabaseMd

router = Router(name='main')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.message(MainGroup.viewing_profile, F.text == 'Назад ◀️')
async def show_main_menu(message: types.Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        'Ты в главном меню. Используй кнопки для навигации 🔽',
        reply_markup=MAIN_MENU_KB
    )

    await state.set_state(MainGroup.viewing_main_menu)


@router.message(MainGroup.viewing_main_menu, F.text == 'Сгенерировать 🔑')
@router.message(MainGroup.viewing_all_records, F.text == 'Сгенерировать 🔑')
@router.message(RecordGroup.viewing_record, F.text == 'Сгенерировать 🔑')
async def generate_password(message: types.Message, arq_redis: ArqRedis) -> None:
    await generate(message, arq_redis)


@router.message(MainGroup.viewing_main_menu, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_all_records, F.text == 'Мой профиль 👨')
@router.message(RecordGroup.viewing_record, F.text == 'Мой профиль 👨')
async def show_profile(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text='Ты в меню профиля. Используй кнопки для навигации 🔽',
        reply_markup=PROFILE_KB
    )
    await state.set_state(MainGroup.viewing_profile)
