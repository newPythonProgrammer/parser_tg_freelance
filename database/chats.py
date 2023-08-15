import sqlite3
import numpy

class Chat_data_class:
    '''Класс для управления бд чатов'''
    def __init__(self):
        with sqlite3.connect('chats.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS chat(
            Chat_ID INTEGER,
            Link TEXT)''')

    def add_chat(self, chat_id, link):
        with sqlite3.connect('chats.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''INSERT INTO chat(Chat_ID, Link) VALUES(?,?)''', (chat_id, link))

    def del_chat(self, chat_id):
        with sqlite3.connect('chats.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''DELETE FROM chat WHERE Chat_ID = ?''', (chat_id,))

    def get_chat(self):
        '''Получаем список ссылок чатов'''
        with sqlite3.connect('chats.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT Link FROM chat''')
            result = numpy.array(cursor.fetchall()).flatten()
            return result

    def get_chat_id(self):
        '''получаем список id чатов'''
        with sqlite3.connect('chats.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT Chat_ID FROM chat''')
            result = numpy.array(cursor.fetchall()).flatten()
            list_ids = []
            for chat_id in result:
                list_ids.append(int(chat_id))
            return list_ids
