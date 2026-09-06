import sqlite3

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    con = sqlite3.connect('clinic.db')
    cursor = con.cursor()

    # Create the xrays table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xrays (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            gender TEXT NOT NULL, 
            age INTEGER NOT NULL, 
            date TEXT NOT NULL, 
            state TEXT NOT NULL, 
            price REAL NOT NULL, 
            contact TEXT NOT NULL, 
            address TEXT NOT NULL
        )
    """)
    
    # Create the dental table if it doesn't exist (added price column to match the UI)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dental (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            gender TEXT NOT NULL, 
            age INTEGER NOT NULL, 
            date TEXT NOT NULL, 
            state TEXT NOT NULL, 
            price REAL NOT NULL, 
            contact TEXT NOT NULL, 
            address TEXT NOT NULL
        )
    """)
    
    # Create the implant table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS implant (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            gender TEXT NOT NULL, 
            age INTEGER NOT NULL, 
            date TEXT NOT NULL, 
            state TEXT NOT NULL, 
            price REAL NOT NULL, 
            contact TEXT NOT NULL, 
            address TEXT NOT NULL
        )
    """)
    
    # Create the fillings table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fillings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            gender TEXT NOT NULL, 
            age INTEGER NOT NULL, 
            date TEXT NOT NULL, 
            state TEXT NOT NULL, 
            price REAL NOT NULL, 
            contact TEXT NOT NULL, 
            address TEXT NOT NULL
        )
    """)
    
    con.commit()
    con.close()
    print("Database and all four section tables have been successfully created and set up!")

if __name__ == "__main__":
    create_database()