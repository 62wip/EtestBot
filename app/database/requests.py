import pymysql
from config import *

try:
    db = pymysql.connect(
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

def create_all_tables() -> None:
    with db.cursor() as cursor:
        try:
            execute_create_all_tables = 'CREATE TABLE IF NOT EXISTS `users` (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT)'
            cursor.execute(execute_create_all_tables)
            db.commit()
            print("Table 'users' created successfully.")
        except pymysql.Error as e:
            print(f"Error creating table: {e}")


def checking_first_use(user_id) -> None:
    # with db.cursor() as cursor:
    #     execute_select_user_by_user_id = f'SELECT * FROM `users` WHERE user_id = {user_id}'
    #     cursor.execute(execute_select_user_by_user_id)
    #     result = cursor.fetchall()
    #     return len(result) == 0
    return True