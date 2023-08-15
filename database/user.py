import sqlite3
import numpy

class User_data_class:
    '''Класс для управления БД юзеров'''
    def __init__(self):
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            User_ID INTEGER,
            First_Name TEXT,
            Username TEXT,
            Surname TEXT,
            Activ INTEGER DEFAULT 1,
            Status INTEGER DEFAULT 1)''')

    def add_user(self, user_id, first_name, username, surname):
        '''Добавляем юзеров'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT * FROM users WHERE User_ID = ?''', (user_id,))
            checker = cursor.fetchone()
            if not checker:
                cursor.execute('''INSERT INTO users(User_ID, First_Name, Username, Surname) VALUES(?,?,?,?)''',
                               (user_id, first_name, username, surname))

    def disactive_user(self, user_id):
        '''Устанавливаем статус активности юзера в 0'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''UPDATE users SET Activ = 0 WHERE User_ID = ?''', (user_id,))

    def active_user(self, user_id):
        '''Устанавливаем статус активности юзера в 1'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''UPDATE users SET Activ = 1 WHERE User_ID = ?''', (user_id,))

    def change_status1(self, user_id):
        '''Устанавливаем статус приема заявок юзера в 1'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''UPDATE users SET Status = 1 WHERE User_ID = ?''', (user_id,))

    def change_status0(self, user_id):
        '''Устанавливаем статус приема заявок юзера в 0'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''UPDATE users SET Status = 0 WHERE User_ID = ?''', (user_id,))

    def get_status(self, user_id):
        '''Получаем статус приема заявок юзера'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT Status FROM users WHERE User_ID = ?''', (user_id, ))
            status = cursor.fetchone()
            return status[0]

    def get_stat(self):
        '''Получаем статистику'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT count(DISTINCT User_ID) FROM users as count WHERE Activ = 1''')
            active_users = cursor.fetchone()[0]
            cursor.execute('''SELECT count(DISTINCT User_ID) FROM users as count WHERE Activ = 0''')
            disactive_users = cursor.fetchone()[0]
            cursor.execute('''SELECT count(DISTINCT User_ID) FROM users as count''')
            all_users = cursor.fetchone()[0]
            return f'Всего пользователей когда-либо запустивших бота - {all_users}\n' \
                   f'Активных пользователей - {active_users}\n' \
                   f'Неактивных пользователей - {disactive_users}'

    def get_all_user_id(self):
        '''Получаем всех юзеров список'''
        with sqlite3.connect('user.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT User_ID FROM users''')
            all_ids = numpy.array(cursor.fetchall()).flatten()
            users_ids = []
            for user in all_ids:
                users_ids.append(int(user))
            return users_ids

