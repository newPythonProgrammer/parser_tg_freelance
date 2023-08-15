from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM_ADMIN_SPAM(StatesGroup):
    '''Рассылка'''
    text = State()
    btns = State()

class FSM_KEY_WORD(StatesGroup):
    '''Ключевые слова'''
    file = State()

class FSM_ADD_CHAT(StatesGroup):
    '''Добавялем чат'''
    chat = State()

class FSM_DELETE_CHAT(StatesGroup):
    '''Удаляем чат'''
    chat = State()