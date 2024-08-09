import sqlite3
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO',
                    format='#%(levelname)-8s [%(asctime)s] %(filename)s: %(lineno)d - %(name)s - %(message)s',
                    filename='logs.log',
                    filemode='w')


class Database:
    def __init__(self, user_id: int = None) -> None:
        self.user_id = user_id

    @staticmethod
    def create_table_users() -> None:
        logger.info('Connecting to db')
        with sqlite3.connect('SETA.db') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT NOT NULL PRIMARY KEY,'
                           'name VARCHAR(255), age INT)')
            logger.info('Query executed')

    def insert_user(self, user_name: str, age: int) -> None:
        logger.info('Connecting to db')
        with sqlite3.connect('SETA.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f'INSERT INTO users (id, name, age)'
                           f'VALUES (?,?,?)', (self.user_id, user_name, age))
            logger.info('Query executed')

    @staticmethod
    def select_all_users() -> str:
        logger.info('Connecting to db')
        with sqlite3.connect('SETA.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            result = ''
            for row in cursor.fetchall():
                result += f'<b>id</b>: {row['id']} <b>name</b>: {row['name']} <b>age</b>: {row['age']}\n'
            logger.info('Query executed')
            return result

    @staticmethod
    def get_ids() -> list:
        logger.info('Connecting to db')
        with sqlite3.connect('SETA.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users')
            result = []
            for row in cursor.fetchall():
                result.append(row[0])
            return result
