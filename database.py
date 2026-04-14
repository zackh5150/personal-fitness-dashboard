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
        CREATE TABLE IF NOT EXISTS user_equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            equipment_name TEXT NOT NULL,
            experience TEXT NOT NULL,
            suggestion_name TEXT,
            suggestion_instructions TEXT,
            suggestion_safety TEXT
        )
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

    # seed equipment test data (from Christian's original test.db, all accounts)
    c.execute("SELECT COUNT(*) FROM user_equipment")
    if c.fetchone()[0] == 0:
        seed_equipment = [
            ("ab machine", "expert"),
            ("post", "expert"),
            ("exercise mat", "beginner"),
            ("chair", "expert"),
            ("hyperextension bench / roman chair", "expert"),
            ("lat pulldown machine", "intermediate"),
            ("high row machine", "intermediate"),
            ("dip machine", "intermediate"),
            ("leg curl machine", "intermediate"),
            ("lateral raise machine", "intermediate"),
            ("power rack / squat rack", "expert"),
            ("chest press machine", "expert"),
            ("pull-up bar", "intermediate"),
            ("dumbbell", "expert"),
            ("decline bench", "beginner"),
            ("abductor machine", "intermediate"),
            ("glute-ham developer", "intermediate"),
            ("triceps extension machine", "expert"),
            ("assisted pull-up/dip machine", "beginner"),
            ("hack squat machine", "intermediate"),
            ("plyo box", "expert"),
            ("cable machine", "beginner"),
        ]
        for name, exp in seed_equipment:
            c.execute(
                "INSERT INTO user_equipment (user_id, equipment_name, experience) VALUES (1, ?, ?)",
                (name, exp),
            )

    # seed ratings test data (from Christian's original test.db, all accounts)
    c.execute("SELECT COUNT(*) FROM exercise_ratings")
    if c.fetchone()[0] == 0:
        seed_ratings = [
            ("Rickshaw Carry", 8),
            ("Landmine twist", 5),
            ("Single-Leg Press", 3),
            ("T-Bar Row with Handle", 6),
            ("Clean Deadlift", 8),
            ("Power Snatch", 5),
            ("Incline Hammer Curls", 9),
            ("Weighted pull-up", 4),
            ("Hack Squat - Gethin Variation", 6),
            ("Straight-bar wrist roll-up", 3),
            ("Wide-grip barbell curl", 5),
        ]
        for exercise, rating in seed_ratings:
            c.execute(
                "INSERT INTO exercise_ratings (user_id, exercise_name, rating) VALUES (1, ?, ?)",
                (exercise, rating),
            )

    conn.commit()
    conn.close()
