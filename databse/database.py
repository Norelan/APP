import sqlite3 as sl

# conn = sl.connect('wish.db')
# cursor = conn.cursor()

# # Создание пользователя с user_id = 1000
# cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES(?)", (1000,))
# # считываю всех пользователей
# users = cursor.execute("SELECT * FROM 'users'")
# print(users.fetchall())

# # подтверждаем изменения
# conn.commit()

class DB:

    def __init__(self, db_file):
        """ Инициализация соединений с БД"""
        self.conn = sl.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return len(result.fetchall()) > 0
    
    def get_id(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return result.fetchall()[0]
    
    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO users (user_id) VALUES(?)", (user_id,))
        return self.conn.commit()
    
    def add_wish(self, user_id, wish_text, wish_url):
        self.cursor.execute("INSERT INTO wishes (users_id, wish_text, wish_url) VALUES(?, ?, ?)",
                (self.get_id(user_id)[0],
                 wish_text,
                 wish_url,))
        return self.conn.commit()
    
    def get_wishlist(self, user_id):
        result = self.cursor.execute("SELECT * FROM wishes WHERE users_id = ?", (self.get_id(user_id)))
        return result.fetchall()

    def close(self):
        self.conn.close()

BotDB = DB('wish.db')