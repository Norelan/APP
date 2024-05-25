import sqlite3 as sl

class DB:
    def __init__(self, db_file):
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
    
    def get_wish(self, wish_id):
        result = self.cursor.execute("SELECT * FROM wishes WHERE id = ?", (wish_id,))
        return result.fetchall()
    
    def wish_owner(self, wish_id):
        result = self.cursor.execute("SELECT users_id FROM wishes WHERE id = ?", (wish_id,))
        return result.fetchall()[0]
    
    def update_wish_text(self, new_text, wish_id):
        self.cursor.execute("UPDATE wishes SET wish_text = ? WHERE id = ? ", (new_text, wish_id))
        return self.conn.commit()
    def update_wish_url(self, new_url, wish_id):
        self.cursor.execute("UPDATE wishes SET wish_url = ? WHERE id = ?", (new_url, wish_id))
        return self.conn.commit()

    def delete_wish(self, wish_id):
        self.cursor.execute("DELETE FROM wishes WHERE id = ?", (wish_id,))
        return self.conn.commit()
    
    def close(self):
        self.conn.close()

