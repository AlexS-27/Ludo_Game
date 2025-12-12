# src/linkwithdatabase.py
import sqlite3
import traceback
from pathlib import Path

def _default_db_path():

    src_dir = Path(__file__).resolve().parent   # .../project/src
    project_root = src_dir.parent                # .../project
    db_dir = project_root / "docs" / "Database"
    # create folder if missing
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "ludo.db"
    return db_path

def get_connection(db_path=None):
    """Retourne une connexion SQLite. Si db_path None, utilise le chemin par défaut calculé."""
    if db_path is None:
        db_path = _default_db_path()
    else:
        db_path = Path(db_path).resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    return conn

def _ensure_schema(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT UNIQUE NOT NULL,
            Password TEXT
        )
    """)
    conn.commit()

def CreateNewGameDB(newgame_entry_name, newgame_entry_password, db_path=None):
    # ouvre une connexion locale et utilise son curseur, puis commit.
    if not newgame_entry_name:
        print("CreateNewGameDB: nom vide")
        return False

    try:
        conn = get_connection(db_path)
        try:
            _ensure_schema(conn)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Game (Name, Password) VALUES (?, ?)",
                (newgame_entry_name, newgame_entry_password)
            )
            conn.commit()
            print("CreateNewGameDB: inserted id", cur.lastrowid)
            return True
        finally:
            conn.close()
    except sqlite3.IntegrityError as e:
        print("CreateNewGameDB: IntegrityError:", e)
        return False
    except Exception as e:
        print("CreateNewGameDB: Exception:", e)
        traceback.print_exc()
        return False

def LoadGameDB(name_val, pass_val, db_path=None):

    if not name_val:
        print("LoadGameDB: name vide")
        return False

    try:
        conn = get_connection(db_path)
        try:
            _ensure_schema(conn)
            cur = conn.cursor()
            if pass_val is None or pass_val == "":
                cur.execute(
                    "SELECT * FROM Game WHERE Name = ? AND (Password IS NULL OR Password = '')",
                    (name_val,)
                )
            else:
                cur.execute(
                    "SELECT * FROM Game WHERE Name = ? AND Password = ?",
                    (name_val, pass_val)
                )
            row = cur.fetchone()
            if row:
                print("LoadGameDB: found", row)
                return row
            else:
                print("LoadGameDB: not found / wrong password")
                return False
        finally:
            conn.close()
    except Exception as e:
        print("LoadGameDB: Exception:", e)
        traceback.print_exc()
        return False
