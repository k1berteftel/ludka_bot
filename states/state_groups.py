from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class startSG(StatesGroup):
    start = State()


class adminSG(StatesGroup):
    start = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()
