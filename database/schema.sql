CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exe_name TEXT NOT NULL,
    game_name TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration REAL
);

CREATE TABLE IF NOT EXISTS game_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name TEXT NOT NULL UNIQUE,
    progress_percentage REAL DEFAULT 0,
    achievements_unlocked INTEGER DEFAULT 0,
    total_achievements INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
