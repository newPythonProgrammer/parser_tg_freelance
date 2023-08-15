from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def disactive_status():
    menu = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text='Остановить прием заявок', callback_data='stop_status')
    menu.add(btn)
    return menu

def active_status():
    menu = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text='Возобновить прием заявок', callback_data='start_status')
    menu.add(btn)
    return menu


def admin_panel():
    menu = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='Установить новые ключевые слова', callback_data='set_key_words')
    btn2 = InlineKeyboardButton(text='Статистика', callback_data='stat')
    btn3 = InlineKeyboardButton(text='Добавить чат/канал', callback_data='add_chat')
    btn4 = InlineKeyboardButton(text='Получить все чаты', callback_data='get_chat')
    btn5 = InlineKeyboardButton(text='Удалить чат', callback_data='del_chat')
    menu.add(btn1, btn2, btn3, btn4, btn5)
    return menu

