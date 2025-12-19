"""
Ludo Game - Database Connectivity Module
Description: Handles SQLite database interactions, including schema initialization,
             saving new game sessions, and retrieving existing ones.
Authors: Alexandre Ramirez, Kilian Testard, Niels Delafontaine et Alex Kamano with help of IA
Date: 2025
"""

import sqlite3
import traceback
from pathlib import Path


def _default_db_path():
    """
    Calculates the absolute path to the database file within the project structure.
    Ensures the directory exists before returning the path.
    """
    src_dir = Path(__file__).resolve().parent  # Path: .../project/src
    project_root = src_dir.parent  # Path: .../project
    db_dir = project_root / "docs" / "Database"

    # Create the directory if it does not exist
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "ludo.db"


def get_connection(db_path=None):
    """
    Establishes a connection to the SQLite database.

    Args:
        db_path (str, optional): Custom path to the .db file. Defaults to calculated path.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    if db_path is None:
        db_path = _default_db_path()
    else:
        db_path = Path(db_path).resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)

    # check_same_thread=False allows sharing the connection across Pygame events if needed
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    return conn


def _ensure_schema(conn):
    """
    Checks for the existence of required tables and creates them if missing.
    """
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Game
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    Name
                    TEXT
                    UNIQUE
                    NOT
                    NULL,
                    Password
                    TEXT
                )
                """)
    conn.commit()


def CreateNewGameDB(name, password, db_path=None):
    """
    Attempts to insert a new game entry into the database.

    Args:
        name (str): The unique name for the game session.
        password (str): The password associated with the session.
        db_path (str, optional): Custom database path.

    Returns:
        bool: True if insertion was successful, False otherwise.
    """
    if not name:
        print("CreateNewGameDB: Error - Empty name provided.")
        return False

    try:
        conn = get_connection(db_path)
        try:
            _ensure_schema(conn)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Game (Name, Password) VALUES (?, ?)",
                (name, password)
            )
            conn.commit()
            print(f"CreateNewGameDB: Successfully inserted ID {cur.lastrowid}")
            return True
        finally:
            conn.close()
    except sqlite3.IntegrityError as e:
        print(f"CreateNewGameDB: Integrity Error (likely duplicate name): {e}")
        return False
    except Exception as e:
        print(f"CreateNewGameDB: Unexpected error: {e}")
        traceback.print_exc()
        return False


def LoadGameDB(name, password, db_path=None):
    """
    Retrieves a game session from the database based on name and password.

    Args:
        name (str): The name of the game to load.
        password (str): The password to verify.
        db_path (str, optional): Custom database path.

    Returns:
        tuple/bool: The database row if found, False otherwise.
    """
    if not name:
        print("LoadGameDB: Error - Empty name provided.")
        return False

    try:
        conn = get_connection(db_path)
        try:
            _ensure_schema(conn)
            cur = conn.cursor()

            # Handle cases where the password might be null or an empty string
            if not password:
                cur.execute(
                    "SELECT * FROM Game WHERE Name = ? AND (Password IS NULL OR Password = '')",
                    (name,)
                )
            else:
                cur.execute(
                    "SELECT * FROM Game WHERE Name = ? AND Password = ?",
                    (name, password)
                )

            row = cur.fetchone()
            if row:
                print(f"LoadGameDB: Session found for '{name}'")
                return row
            else:
                print("LoadGameDB: No match found or invalid credentials.")
                return False
        finally:
            conn.close()
    except Exception as e:
        print(f"LoadGameDB: Unexpected error: {e}")
        traceback.print_exc()
        return False