import sqlite3
import bcrypt
from schemes import User
from utils import process_user

class DBWorker:
    def __init__(self, db_path: str = 'matrix_db.db'):
        # check_same_thread=False нужен, чтобы Qt мог обращаться к БД из разных потоков
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    passwd TEXT NOT NULL, 
                    operations_cnt INTEGER DEFAULT 0,
                    energy INTEGER DEFAULT 0
                );
            ''')

    def add_user(self, user: User) -> bool:
        user = process_user(user)
        with self.conn:
            try:
                self.conn.execute(
                    '''INSERT INTO users (name, email, passwd) VALUES (?, ?, ?);''',
                    (user.name, user.email, user.passwd)
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def check_cred(self, username: str, passwd: str) -> int:
        # Возвращает ID пользователя, если пароль верный, иначе кидает ошибку
        curs = self.conn.execute(
            'SELECT id, passwd FROM users WHERE name = ?', (username,)
        )
        row = curs.fetchone()
        if row is None:
            raise ValueError('Пользователь не найден.')
        
        uid, hashed_passwd = row
        if not bcrypt.checkpw(passwd.encode('utf-8'), hashed_passwd.encode('utf-8')):
            raise ValueError('Неверный пароль.')
        
        return uid

    def add_energy(self, uid: int, amount: int = 10):
        # Начисляет энергию и увеличивает счетчик операций
        with self.conn:
            self.conn.execute(
                'UPDATE users SET energy = energy + ?, operations_cnt = operations_cnt + 1 WHERE id = ?',
                (amount, uid)
            )

    def get_stats(self, uid: int) -> tuple:
        # Возвращает (энергию, количество операций)
        curs = self.conn.execute('SELECT energy, operations_cnt FROM users WHERE id = ?', (uid,))
        row = curs.fetchone()
        return row if row else (0, 0)
