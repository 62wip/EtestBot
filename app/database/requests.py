import pymysql

from config import *
from app.database.models import *

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
                    'CREATE TABLE IF NOT EXISTS `users` (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, username TEXT, fio TEXT, status CHAR(1), `group` TEXT)',
                    'CREATE TABLE IF NOT EXISTS `test` (id INT AUTO_INCREMENT PRIMARY KEY, creator_user_id INT, creation_time DATETIME, test_key TEXT,test_name TEXT, subject_name TEXT, all_questions TEXT, all_answers TEXT, right_answer TEXT, visible_result BIT)'
                    # 'CREATE TABLE IF NOT EXISTS `test_result` (id INT AUTO_INCREMENT PRIMARY KEY, maker_user_id INT, making_time DATETIME, test_id INT, count_right INT, mistake_place TEXT)'

                    ]
                for execute_create_table in execute_create_all_tables:
                    cursor.execute(execute_create_table)
                self.db.commit()
                # print("Tables created successfully.")
            except pymysql.Error as e:
                print(f"Error creating table: {e}")

    def insert_new_user_id(self, user: User) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_insert_new_user_id = f'INSERT INTO `users` (user_id, username, fio, status, `group`) VALUES ({user.user_id}, {user.username}, {user.fio}, {chr(user.status)}, {user.group})'
                values = (user.user_id, user.username, user.fio, user.status, user.group)
                cursor.execute(execute_insert_new_user_id, values)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in insert into table: {e}")


    def checking_first_use(self, user_id: int) -> bool:
        with self.db.cursor() as cursor:
            try:
                execute_insert_new_user_id = f'SELECT * FROM `users` WHERE user_id = {user_id}'
                cursor.execute(execute_insert_new_user_id)
                result = cursor.fetchall()
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")
        return len(result) == 0
    
    def select_for_my_profile(self, user_id: int) -> User:
        with self.db.cursor() as cursor:
            try:
                execute_select_for_my_profile = f'SELECT * FROM `users` WHERE user_id = {user_id}'
                cursor.execute(execute_select_for_my_profile)
                result = cursor.fetchall()[0]
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")

        return User(result['user_id'], result['username'], result['fio'], result['status'], result['group'])
    
    def update_fio_for_my_profile(self, user_id: int, fio: str) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_update_fio_for_my_profile = f'UPDATE `users` SET fio = "{fio}" WHERE user_id = {user_id}'
                cursor.execute(execute_update_fio_for_my_profile)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")

    def update_status_for_my_profile(self, user_id: int, status: str) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_update_status_for_my_profile = f'UPDATE `users` SET status = "{status}", `group` = NULL WHERE user_id = {user_id}'
                cursor.execute(execute_update_status_for_my_profile)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")

    def update_group_for_my_profile(self, user_id: int, group: str) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_update_group_for_my_profile = f'UPDATE `users` SET `group` = "{group}" WHERE user_id = {user_id}'
                cursor.execute(execute_update_group_for_my_profile)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")