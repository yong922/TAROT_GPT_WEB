from app.models import get_db_connection, User

def authenticate_user(user_id, password):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, password, nickname FROM user_tb WHERE id = %s AND password = %s", (user_id, password))
    user_data = cursor.fetchone()
    connection.close()

    if user_data:
        return User(user_data["id"], user_data["password"], user_data["nickname"])
    return None
