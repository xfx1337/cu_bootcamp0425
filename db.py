from sqlite3 import connect


# Подключение к базе данных
def get_db_connection():
    conn = connect('main.db')
    conn.row_factory = dict_factory  # Используем dict_factory для удобства
    return conn


def dict_factory(cursor, row):
    """Преобразует строку результата запроса в словарь."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Инициализация базы данных
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        userid INT,
        first_name TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        userid INT,
        subject TEXT
    );
    ''')

    conn.commit()
    conn.close()

def user_exists(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE userid = ?",
        [(userid)]
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def register_user(userid, first_name):
    if not user_exists(userid):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (userid, first_name) VALUES (?,?)",
            (userid, first_name)
        )
        conn.commit()
        conn.close()

def register_subjects(userid, subjects):
    if user_exists(userid):
        conn = get_db_connection()
        for s in subjects:
            conn.execute(
                "INSERT INTO subjects (userid, subject) VALUES (?,?)",
            (userid, str(s)))
        conn.commit()
        conn.close()