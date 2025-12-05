import sqlite3
conn = sqlite3.connect("ludo.db")
cursor = conn.cursor()


def CreateNewGameDB(newgame_entry_name, newgame_entry_password):
    conn = sqlite3.connect("ludo.db")
    query = "INSERT INTO Game (Name, Password) VALUES (?, ?)"
    cursor.execute(query,(newgame_entry_name, newgame_entry_password))
    conn.commit()

def LoadGameDB(name_val, pass_val):
    # On utilise ? pour remplacer les variables
    query = "SELECT * FROM Game WHERE Name = ? AND Password = ?"

    # On exécute la recherche avec les valeurs reçues
    cursor.execute(query, (name_val, pass_val))

    result = cursor.fetchall()

    if result:
        print(f"Partie trouvée ! ID: {result[0][0]}")
        return result  # Renvoie les données trouvées
    else:
        print("Aucune partie trouvée avec ce nom/mot de passe.")
        return None