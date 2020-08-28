CREATE TABLE herfst (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    naam TEXT,
    score REAL,
    UNIQUE (date, naam))
