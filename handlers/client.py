from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from database.user import User_data_class
from other import keyboard

User_data = User_data_class()


async def start(message: Message):
    '''Пользователь нажал старт'''
    user_id = message.from_user.id
    name = message.from_user.first_name
    surname = message.from_user.last_name
    username = message.from_user.username

    User_data.add_user(user_id, name, username, surname)
    User_data.active_user(user_id)
    status = User_data.get_status(user_id) #Статус приема заявок

    if status:
        await message.answer(f'<b>Привет, {name}.</b>\n\n'
                             f'Я бот который поможет тебе найти заказы на продвижение в тг\n\n'
                             f'Статус приема заявок: OK✅', parse_mode='HTML', reply_markup=keyboard.disactive_status())
    else:
        await message.answer(f'<b>Привет, {name}.</b>\n\n'
                             f'Я бот который поможет тебе найти заказы на продвижение в тг\n\n'
                             f'Статус приема заявок: NO❌', parse_mode='HTML', reply_markup=keyboard.active_status())



async def disactive_status(call: CallbackQuery, state: FSMContext):
    '''Устанавливаем статус приема заявок в 0'''
    await state.finish()
    await call.answer()
    user_id = call.from_user.id
    name = call.from_user.first_name

    User_data.change_status0(user_id)
    status = User_data.get_status(user_id) #Статус приема заявок

    if status:
        status_text = f'Статус приема заявок: OK✅'
    else:
        status_text = 'Статус приема заявок: NO❌'
    await call.bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=f'<b>Привет, {name}.</b>\n\n'
                         f'Я бот который поможет тебе найти заказы на продвижение в тг\n\n'
                         f'{status_text}', parse_mode='HTML', reply_markup=keyboard.active_status())


async def activate_status(call: CallbackQuery, state: FSMContext):
    '''Устанавливаем статус приема заявок в 1'''
    await state.finish()
    await call.answer()
    user_id = call.from_user.id
    name = call.from_user.first_name

    User_data.change_status1(user_id)
    status = User_data.get_status(user_id)  # Статус приема заявок

    if status:
        status_text = f'Статус приема заявок: OK✅'
    else:
        status_text = 'Статус приема заявок: NO❌'
    await call.bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=f'<b>Привет, {name}.</b>\n\n'
                                     f'Я бот который поможет тебе найти заказы на продвижение в тг\n\n'
                                     f'{status_text}', parse_mode='HTML', reply_markup=keyboard.disactive_status())


def register_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')

    dp.register_callback_query_handler(disactive_status, lambda call: call.data == 'stop_status', state='*')
    dp.register_callback_query_handler(activate_status, lambda call: call.data == 'start_status', state='*')