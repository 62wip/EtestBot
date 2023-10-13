import pymysql

def checking_first_use(db, user_id):
    # with db.cursor() as cursor:
    #     select_user_by_user_id = f'SELECT * FROM `users` WHERE user_id = {user_id}'
    #     cursor.execute(select_user_by_user_id)
    #     result = cursor.fetchall()
    #     return len(result) == 0
    return True