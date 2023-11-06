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
                    'CREATE TABLE IF NOT EXISTS `users` (id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT, username TEXT, fio TEXT, status CHAR(1), `group` TEXT)',
                    'CREATE TABLE IF NOT EXISTS `test` (id INT AUTO_INCREMENT PRIMARY KEY, creator_user_id INT, creation_time DATETIME, `test_key` TEXT,test_name TEXT, subject_name TEXT, all_questions TEXT, all_answers TEXT, right_answers TEXT, visible_result BIT)'
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
                if user.status == 'T':
                    group = 'NULL'
                else:
                    group = f'"{user.group}"'
                execute_insert_new_user_id = f'''INSERT INTO `users` (user_id, username, fio, status, `group`) 
                VALUES 
                ({user.user_id}, "{user.username}", "{user.fio}", "{user.status}", {group})'''
                cursor.execute(execute_insert_new_user_id)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in insert into table: {e}")

    def checking_first_use(self, user_id: int) -> bool:
        with self.db.cursor() as cursor:
            try:
                execute_insert_new_user_id = f'''SELECT * FROM `users` 
                WHERE user_id = {user_id}'''
                cursor.execute(execute_insert_new_user_id)
                result = cursor.fetchall()
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")
        return len(result) == 0
    
    def select_for_user_class(self, user_id: int) -> User:
        with self.db.cursor() as cursor:
            try:
                execute_select_for_my_profile = f'''SELECT * FROM `users` 
                WHERE user_id = {user_id}'''
                cursor.execute(execute_select_for_my_profile)
                result = cursor.fetchall()[0]
            except pymysql.Error as e:
                print(f"Error in select from table: {e}")

        return User(result['user_id'], result['username'], result['fio'], result['status'], result['group'])
    
    def update_fio_for_my_profile(self, user_id: int, fio: str) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_update_fio_for_my_profile = f'''UPDATE `users` 
                SET fio = "{fio}" 
                WHERE user_id = {user_id}'''
                cursor.execute(execute_update_fio_for_my_profile)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in update from table: {e}")

    def update_status_for_my_profile(self, user_id: int, status: str) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_update_status_for_my_profile = f'''UPDATE `users` 
                SET 
                status = "{status}", `group` = NULL 
                WHERE 
                user_id = {user_id}'''
                cursor.execute(execute_update_status_for_my_profile)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in update from table: {e}")

    def update_group_for_my_profile(self, user_id: int, group: str) -> None:
        with self.db.cursor() as cursor:
            try:
                execute_update_group_for_my_profile = f'''UPDATE `users` 
                SET `group` = "{group}" 
                WHERE user_id = {user_id}'''
                cursor.execute(execute_update_group_for_my_profile)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in update from table: {e}")

    def insert_new_test(self, test: Test) -> None:
        with self.db.cursor() as cursor:
            try:
                if test.subject_name == None:
                    subject_name = 'NULL'
                else:
                    subject_name = f'"{test.subject_name}"'
                execute_insert_new_test = f'''INSERT INTO `test` (creator_user_id, creation_time, test_key, test_name, subject_name, all_questions, all_answers, right_answers, visible_result) 
                VALUES 
                ({test.creator_user_id}, "{test.creation_time}", "{str(test.test_key)}", "{test.test_name}", {subject_name}, "{'-_-'.join(test.all_questions)}", "{'-_-'.join(['-=-'.join(sublist) for sublist in test.all_answers])}", "{'-_-'.join(list(map(str, test.right_answers)))}", {test.visible_result})'''
                cursor.execute(execute_insert_new_test)
                self.db.commit()
            except pymysql.Error as e:
                print(f"Error in insert from table: {e}")

    def select_for_test_class_by_uuid(self, key: UUID) -> Test:
        with self.db.cursor() as cursor:
            try:
                execute_insert_new_test = f'''SELECT * FROM `test` 
                where test_key = "{str(key)}"'''
                cursor.execute(execute_insert_new_test)
                result = cursor.fetchall()[0]
            except pymysql.Error as e:
                print(f"Error in insert from table: {e}")

        return Test(result['creator_user_id'], result['test_key'], result['test_name'], result['subject_name'], result['all_questions'].split('-_-'), [i.split('-=-') for i in result['all_answers'].split('-_-')], list(map(int, result['right_answers'].split('-_-'))), result['visible_result'])