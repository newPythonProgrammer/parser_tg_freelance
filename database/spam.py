import sqlite3 as sq
import ast


class Spam_data_class:
    '''Класс для БД рассылки'''

    def __init__(self):
        with sq.connect('smap.db') as con:
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS spam(
                   id INTEGER PRIMARY KEY,
                   text TEXT,
                   keyboard STRING,
                   media STRING)''')

    def make_spam(self, text, keyboard, media):
        '''Запись рассылки в базу данных'''
        with sq.connect('smap.db') as con:
            cur = con.cursor()

            ins = '''INSERT INTO spam(text, keyboard, media) VALUES(?,?,?)'''
            data = (text, keyboard, media)
            cur.execute(ins, data)


    def select_text(self, spam_id):
        '''Получаем текст рассылки'''
        with sq.connect('smap.db') as con:
            cur = con.cursor()
            cur.execute(f'''SELECT text FROM spam WHERE id = {spam_id}''')
            text = cur.fetchone()
        return text[0]

    def select_keyboard(self, spam_id):
        '''Получаем клавиатуру'''
        with sq.connect('smap.db') as con:
            cur = con.cursor()
            cur.execute(f'''SELECT keyboard FROM spam WHERE id = {spam_id}''')
            keyboard = cur.fetchone()
        try:
            return ast.literal_eval(keyboard[0])
        except:
            return None

    def select_media(self, spam_id):
        '''Получаем медиа'''
        with sq.connect('smap.db') as con:
            cur = con.cursor()
            cur.execute(f'''SELECT media FROM spam WHERE id = {spam_id}''')
            media = cur.fetchone()
        try:
            return ast.literal_eval(media[0])
        except:
            return None

    def select_id(self):
        '''Получаем последний id'''
        with sq.connect('smap.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT id FROM spam''')
        return cur.fetchall()[-1][0]