DROP TABLE IF EXISTS expenses;

CREATE TABLE expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT
);