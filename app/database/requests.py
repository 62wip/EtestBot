import pymysql
from config import *

try:
    db_con = pymysql.connect(
        host=HOST,
        port=3306,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connected to the database.")
except pymysql.Error as e:
    print(f"Error connecting to the database: {e}")

class Connection():
    def __init__(self) -> None:
        self.db = db_con

    def create_all_tables(self) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_create_all_tables = [
                    'CREATE TABLE IF NOT EXISTS `only_users` (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT)'
                    ]
                for execute_create_table in execute_create_all_tables:
                    cursor.execute(execute_create_table)
                self.db.commit()
                # print("Tables created successfully.")
            except pymysql.Error as e:
                print(f"Error creating table: {e}")

    def insert_or_update_user_id(self, user_id):
        with self.db.cursor() as cursor:
            try:
                execute_insertall_users_id = f'INSERT INTO `only_users_` (user_id) VALUES ({user_id}) ON DUPLICATE KEY UPDATE user_id = {user_id}'
                cursor.execute(execute_insertall_users_id)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error creating table: {e}")


    def checking_first_use(self, user_id) -> None:
        # with db.cursor() as cursor:
        #     execute_select_user_by_user_id = f'SELECT * FROM `users` WHERE user_id = {user_id}'
        #     await cursor.execute(execute_select_user_by_user_id)
        #     await result = cursor.fetchall()
        #     return len(result) == 0
        return True