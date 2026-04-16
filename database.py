import sqlite3

DB_NAME = "fitness.db"


def get_db():
    """Connect to the database and return the connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create all the tables if they don't exist yet."""
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            display_name TEXT,
            height REAL,
            weight REAL,
            age INTEGER,
            goal TEXT,
            fitness_level TEXT DEFAULT 'beginner'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            exercise_name TEXT NOT NULL,
            muscle_group TEXT,
            equipment TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            duration_minutes INTEGER,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS exercise_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exercise_name TEXT NOT NULL,
            rating INTEGER
        )
    """)

    c.execute("""
            CREATE TABLE IF NOT EXISTS Equipment(
            EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            Equipment TEXT NOT NULL,
            Experience TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE);
    """)

    c.execute("""
         CREATE TABLE IF NOT EXISTS workout_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            scheduled_date TEXT,
            duration_minutes INTEGER DEFAULT 60,
            notes TEXT DEFAULT '',
            completed INTEGER DEFAULT 0
        )
    """)

    # create a default user if the table is empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username) VALUES (?)", ("local",))

    conn.commit()
    conn.close()
