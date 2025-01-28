import sqlite3
import Encryption

def create_person_table():
    # Working with the BakingContestPeople.db
    with sqlite3.connect('BakingContestPeople.db') as conn:
        cursor = conn.cursor()

        try:
            conn.execute("""DROP TABLE Person""")
            conn.commit()
            print("Person Table Dropped")
        except sqlite3.OperationalError:
            print("Person Table does not exist")

        # Create Person table
        cursor.execute('''CREATE TABLE Person(
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Phone_Number TEXT PRIMARY KEY NOT NULL,
            Security_Level INTEGER NOT NULL,
            Password TEXT NOT NULL
        );
        ''')
        conn.commit()
        print('Person Table created.')



def create_entry_table():
    with sqlite3.connect('BakingContestEntry.db') as con:
        cursor = con.cursor()
        try:
            con.execute("""DROP TABLE Entry""")
            con.commit()
            print("Entry Table Dropped")
        except:
            print("Entry Table does not exist")
        # create table in database
        cursor.execute('''CREATE TABLE Entry(
        UserID INTEGER PRIMARY KEY,
        EntryID INTEGER NOT NULL,
        NameOfBakingItem TEXT NOT NULL,
        NumExcellentVotes INTEGER NOT NULL,
        NumOkVotes INTEGER NOT NULL,
        NumBadVotes INTEGER NOT NULL
        );
        ''')
        con.commit()
        print('Entry Table created.')
        # close database connection
        con.close()
        print('Connection closed.')