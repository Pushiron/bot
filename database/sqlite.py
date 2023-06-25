import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('data.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "user_id INT PRIMARY KEY,"
                "name TEXT,"
                "isAdmin BOOL NOT NULL DEFAULT '0'"
                ")")
    cur.execute("CREATE TABLE IF NOT EXISTS suggested_wallpapers("
                "id INT NOT NULL PRIMARY KEY,"
                "from_user INT,"
                "wallpaper TEXT"
                ")")


async def create_user(user_id, user_name):
    user = cur.execute("SElECT 1 FROM users WHERE user_id == '{uid}'".format(uid=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?,?,?)", (user_id, user_name, 0))
        db.commit()  # Завершение транзакции


async def get_users():
    users = cur.execute("SElECT * FROM users")
    return users


async def get_user_status(user_id):
    user = cur.execute("SElECT isAdmin FROM users WHERE user_id == '{uid}'".format(uid=user_id)).fetchone()
    if user[0] == 1:
        return True
    else:
        return False


async def save_wallpaper(user_id, wallpaper):
    cur.execute("INSERT INTO suggested_wallpapers (from_user, wallpaper) VAlUES(?,?)", (user_id, wallpaper))
    db.commit()
    return cur.execute("SELECT "
                       "from_user, wallpaper "
                       "FROM suggested_wallpapers "
                       "WHERE wallpaper == '{wallpaper_id}'".format(wallpaper_id=wallpaper)).fetchone()


async def setRole(user_id, role):
    if role == 1 or role == 0:
        query = """UPDATE `users` SET `isAdmin` = ?  WHERE `user_id` = ?"""
        params = (role, user_id)
        cur.execute(query, params)
