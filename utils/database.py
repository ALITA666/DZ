import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def commit(self):
        self.connection.commit()

    def get_user_or_none(self, uid: int):
        query = 'SELECT * FROM users WHERE uid = ?'
        self.execute(query, (uid,))

        result = self.fetch_one()

        return result

    def register(self, uid: int, sex: int, age: int, city: int):
        query = 'INSERT INTO users VALUES(?, ?, ?, ?)'
        self.execute(query, (uid, sex, age, city))
        self.commit()

    def get_seen(self, uid: int, person: int):
        query = "SELECT * FROM seen WHERE uid = ? AND person = ?"
        self.execute(query, (uid, person))
        data = self.fetch_one()

        return data

    def add_seen(self, uid: int, person: int):
        query = 'INSERT INTO seen VALUES(?, ?)'
        self.execute(query, (uid, person))
        self.commit()




