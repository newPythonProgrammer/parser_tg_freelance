import ast
import asyncio
from typing import List, Union

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import pyrogram


import config
from database.spam import Spam_data_class
from database.user import User_data_class
from database.chats import Chat_data_class
from other import keyboard
from other.func import check_text
from state.states import *
from bot import bot

User_data = User_data_class()
Spam_data = Spam_data_class()
Chat_data = Chat_data_class()

client_pyrogram = pyrogram.Client("my_account", config.API_ID, config.API_HASH)


@client_pyrogram.on_message(pyrogram.filters.chat(Chat_data.get_chat_id()))
async def my_handler(client:pyrogram.Client, message:pyrogram.types.Message):
    chat_id = message.chat.id
    message_id = message.id
    username = message.chat.username
    link = f't.me/{username}/{message_id}'
    await asyncio.sleep(10)

    check_msg = await client.get_messages(chat_id, message_id)
    message_text_full = check_msg.text

    if message_text_full == None:
        print('return')
        return

    if check_text(message_text_full):
        if len(message_text_full) >200:
            message_text = message_text_full[0:198]
        else:
            message_text = message_text_full

        for user_id in User_data.get_all_user_id():
            if User_data.get_status(user_id):
                try:
                    await bot.send_message(user_id, f'Я нашел новую работу\n\n'
                                                    f'Ссылка: {link}\n\n'
                                                    f'От: {check_msg.from_user.first_name} - @{check_msg.from_user.username}\n\n'
                                                    f'Текст: {message_text}', disable_web_page_preview=True)
                except:
                    User_data.disactive_user(user_id)


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


async def show_panel(message: Message, state:FSMContext):
    '''Показываем админ панель'''
    await state.finish()
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        await message.answer('Вот твоя админ панель', reply_markup=keyboard.admin_panel())


async def statistic(call: CallbackQuery, state: FSMContext):
    '''Статистика'''
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer(User_data.get_stat())


async def change_key_word(call: CallbackQuery, state: FSMContext):
    '''Меняем ключевые слова'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли txt файл содержащий ключевые слова\n\n'
                                  'Слова должны быть перечислены через запятую.')
        await FSM_KEY_WORD.file.set()


async def change_key_word2(message: Message, state: FSMContext):
    '''Меняем ключевые слова (Загружаем файл с ключевыми словами)'''
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.content_type == 'document':
            await message.document.download('key_word.txt')
            await message.answer('Новые ключевые слова сохранены')
            await state.finish()
        else:
            await message.answer('Ты должен отправить файл')


async def add_chat(call: CallbackQuery, state: FSMContext):
    '''Добавляем чат'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли мне ссылку на чат или канал')
        await FSM_ADD_CHAT.chat.set()


async def add_chat2(message: Message, state: FSMContext):
    '''Добавялем чат (записываем в бд и подписываемся)'''
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        try:
            chat = await client_pyrogram.get_chat(message.text)
            await client_pyrogram.join_chat(chat.id)#присоединение к чату
            Chat_data.add_chat(chat.id, message.text)
            await message.answer(f'Канал {chat.title} добавлен')
            await state.finish()
        except Exception as e:
            await message.answer(f'Не получилось добавить канал {e}')
            await state.finish()


async def del_chat(call: CallbackQuery, state: FSMContext):
    '''Удаляем чат'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли мне ссылку канала/чата который надо удалить')
        await FSM_DELETE_CHAT.chat.set()


async def del_chat2(message: Message, state: FSMContext):
    '''Удаляем чат (убираем из бд и отписываемся)'''
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        try:
            chat = await client_pyrogram.get_chat(message.text)
            await client_pyrogram.leave_chat(chat.id)#удаляем чат
            Chat_data.del_chat(chat.id)
            await message.answer(f'Канал {chat.title} удален')
            await state.finish()
        except Exception as e:
            await message.answer(f'Не получилось удалить канал {e}')
            await state.finish()


async def get_chats(call: CallbackQuery, state: FSMContext):
    '''Получаем список ссылок всех чатов'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        data = Chat_data.get_chat()
        text = 'Все чаты\n\n'
        for link in data:
            text += f'{link}\n'
        await call.message.answer(text)


async def spam1(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли пост')
        await FSM_ADMIN_SPAM.text.set()


async def spam2_media_group(message: types.Message, album: List[types.Message], state: FSMContext):
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type, "caption": obj.caption,
                                "caption_entities": obj.caption_entities})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
    media_group = ast.literal_eval(str(media_group))
    async with state.proxy() as data:
        try:
            data['text'] = media_group[0]['caption']
        except:
            data['text'] = 'None'
        data['media'] = media_group
        Spam_data.make_spam(data['text'], 'None', str(media_group))

    await message.answer_media_group(media_group)
    await message.answer(f'Пришли команду /sendspam_{Spam_data.select_id()} чтоб начать рассылку')
    await state.finish()


async def spam2(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.content_type in ('photo', 'video', 'animation'):
            async with state.proxy() as data:
                try:
                    data['text'] = message.html_text
                except:
                    data['text'] = None
                if message.content_type == 'photo':
                    data['media'] = ('photo', message.photo[-1].file_id)
                else:
                    data['media'] = (message.content_type, message[message.content_type].file_id)
        else:
            async with state.proxy() as data:
                data['text'] = message.html_text
                data['media'] = 'None'
        await message.answer('Теперь пришли кнопки например\n'
                             'text - url1\n'
                             'text2 - url2 && text3 - url3\n\n'
                             'text - надпись кнопки url - ссылка'
                             '"-" - разделитель\n'
                             '"&&" - склеить в строку\n'
                             'ЕСЛИ НЕ НУЖНЫ КНОПКИ ОТПРАВЬ 0')
        await FSM_ADMIN_SPAM.next()


async def spam3(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.text != '0':
            # конструктор кнопок
            try:
                buttons = []
                for char in message.text.split('\n'):
                    if '&&' in char:
                        tmpl = []
                        for i in char.split('&&'):
                            tmpl.append(dict([i.split('-', maxsplit=1)]))
                        buttons.append(tmpl)
                    else:
                        buttons.append(dict([char.split('-', maxsplit=1)]))
                menu = InlineKeyboardMarkup()
                btns_list = []
                items = []
                for row in buttons:
                    if type(row) == dict:
                        url1 = str(list(row.items())[0][1]).strip()
                        text1 = list(row.items())[0][0]
                        menu.add(InlineKeyboardButton(text=text1, url=url1))
                    else:
                        items.clear()
                        btns_list.clear()
                        for d in row:
                            items.append(list(d.items())[0])
                        for text, url in items:
                            url = url.strip()
                            btns_list.append(InlineKeyboardButton(text=text, url=url))
                        menu.add(*btns_list)
                ###########$##############
                async with state.proxy() as data:
                    data['btns'] = str(menu)
                    media = data['media']
                    text = data['text']
                    Spam_data.make_spam(text, str(menu), str(media))
                    if media != 'None':
                        content_type = media[0]
                        if content_type == 'photo':
                            await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'video':
                            await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=menu)
                    else:
                        await message.answer(text, reply_markup=menu, parse_mode='HTML', disable_web_page_preview=True)

            except Exception as e:
                await message.reply(f'Похоже что непрвильно введена клавиатура')
        else:
            async with state.proxy() as data:
                data['btns'] = 'None'
                media = data['media']
                text = data['text']
                Spam_data.make_spam(text, 'None', str(media))

                if media != 'None':
                    content_type = media[0]
                    if content_type == 'photo':
                        await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'video':
                        await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'animation':
                        await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML')
                else:
                    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
        await message.answer(f'Пришли команду /sendspam_{Spam_data.select_id()} чтоб начать рассылку')
        await state.finish()


async def start_spam(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        spam_id = int(message.text.replace('/sendspam_', ''))
        text = Spam_data.select_text(spam_id)
        keyboard = Spam_data.select_keyboard(spam_id)
        media = Spam_data.select_media(spam_id)
        if text == 'None':
            text = None
        if keyboard == 'None':
            keyboard = None
        all_user = User_data.get_all_user_id()
        await message.answer(f'Считанно {len(all_user)} пользователей запускаю рассылку')
        no_send = 0
        send = 0
        for user in all_user:
            user = int(user)
            try:
                if media != 'None' and media != None:  # Есть медиа
                    if type(media) is list:
                        await message.bot.send_media_group(user, media)
                    else:
                        content_type = media[0]

                        if content_type == 'photo':
                            await message.bot.send_photo(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'video':
                            await message.bot.send_video(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=keyboard)

                else:  # Нету медиа
                    if keyboard != 'None' and keyboard != None:  # Есть кнопки
                        await message.bot.send_message(chat_id=user, text=text, reply_markup=keyboard,
                                                       parse_mode='HTML', disable_web_page_preview=True)
                    else:
                        await message.bot.send_message(chat_id=user, text=text, parse_mode='HTML',
                                                       disable_web_page_preview=True)
                send += 1
                User_data.active_user(user)

            except:
                no_send += 1
                User_data.disactive_user(user_id)
        await message.answer(f'Рассылка окончена.\n'
                             f'Отправленно: {send} пользователям\n'
                             f'Не отправленно: {no_send} пользователям')

client_pyrogram.start()
def register_admin(dp: Dispatcher):
    dp.register_message_handler(show_panel, commands='panel', state='*')
    dp.register_callback_query_handler(statistic, lambda call: call.data == 'stat', state='*')

    dp.register_callback_query_handler(spam1, lambda call: call.data == 'spam', state='*')
    dp.register_message_handler(spam2_media_group, is_media_group=True, content_types=types.ContentType.ANY,
                                state=FSM_ADMIN_SPAM.text)
    dp.register_message_handler(spam2, content_types=['photo', 'video', 'animation', 'text'], state=FSM_ADMIN_SPAM.text)
    dp.register_message_handler(spam3, state=FSM_ADMIN_SPAM.btns, content_types=['text'])
    dp.register_message_handler(start_spam, lambda message: str(message.text).startswith('/sendspam_'), state='*')

    dp.register_callback_query_handler(change_key_word, lambda call: call.data == 'set_key_words', state='*')
    dp.register_message_handler(change_key_word2, content_types=['document', 'text'], state=FSM_KEY_WORD.file)

    dp.register_callback_query_handler(add_chat, lambda call: call.data == 'add_chat', state='*')
    dp.register_message_handler(add_chat2, state=FSM_ADD_CHAT.chat)

    dp.register_callback_query_handler(del_chat, lambda call: call.data == 'del_chat', state='*')
    dp.register_message_handler(del_chat2, state=FSM_DELETE_CHAT.chat)

    dp.register_callback_query_handler(get_chats, lambda call: call.data == 'get_chat', state='*')