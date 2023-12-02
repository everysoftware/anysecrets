from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.fsm import MainGroup
from bot.keyboards.main import MAIN_MENU_KB
from bot.middlewares import DatabaseMd

router = Router()

router.message.middleware(DatabaseMd())


async def show_main_menu(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Вы в главном меню. Выберите действие 🔽", reply_markup=MAIN_MENU_KB
    )
    await state.set_state(MainGroup.view_main_menu)
