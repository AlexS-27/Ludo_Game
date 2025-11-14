import sqlite3

# Connexion à la base ludo.db
conn = sqlite3.connect("ludo.db")

# Pour exécuter des commandes SQL
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Game (
    game_id   INTEGER PRIMARY KEY,
    Name      TEXT,
    Password  TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Player (
    id_player       INTEGER PRIMARY KEY,
    Name            TEXT,
    game_id         INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
)
""")

conn.commit()
