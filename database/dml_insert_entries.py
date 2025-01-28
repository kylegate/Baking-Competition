import sqlite3


def insert_entry_data():
    with sqlite3.connect('BakingContestEntry.db') as conn:
        cursor = conn.cursor()

        entries = ((1001, 9001, 'Strawberry Pie', 6, 3, 4),
                   (1002, 9002, 'Banana Pudding', 4, 2, 7),
                   (1003, 9003, 'Ice Cream Cake', 3, 7, 3),
                   (1004, 9004, 'Rice Pudding', 8, 3, 2))

        try:
            cursor.executemany(
                '''INSERT INTO Entry (UserID, EntryID, NameOfBakingItem, 
                NumExcellentVotes, NumOkVotes, NumBadVotes) VALUES (?,?,?,?,?,?)''', entries
            )
            conn.commit()
            print("Data inserted into Entry Table")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data into Entry table: {e}")