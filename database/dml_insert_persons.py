import sqlite3
import Encryption

def insert_person_data():
    with sqlite3.connect('BakingContestPeople.db') as conn:
        cursor = conn.cursor()

        nm1 = str(Encryption.cipher.encrypt(b'Josh').decode("utf-8"))
        Pwd1 = str(Encryption.cipher.encrypt(b'abc789').decode("utf-8"))
        phnm1 = str(Encryption.cipher.encrypt(b'1000000000').decode("utf-8"))

        nm2 = str(Encryption.cipher.encrypt(b'Darla').decode("utf-8"))
        Pwd2 = str(Encryption.cipher.encrypt(b'abc456').decode("utf-8"))
        phnm2 = str(Encryption.cipher.encrypt(b'1000000001').decode("utf-8"))

        nm3 = str(Encryption.cipher.encrypt(b'Kevin').decode("utf-8"))
        Pwd3 = str(Encryption.cipher.encrypt(b'abc123').decode("utf-8"))
        phnm3 = str(Encryption.cipher.encrypt(b'1000000002').decode("utf-8"))

        nm4 = str(Encryption.cipher.encrypt(b'Hunter').decode("utf-8"))
        Pwd4 = str(Encryption.cipher.encrypt(b'abc123').decode("utf-8"))
        phnm4 = str(Encryption.cipher.encrypt(b'1000000003').decode("utf-8"))

        nm5 = str(Encryption.cipher.encrypt(b'Cameron').decode("utf-8"))
        Pwd5 = str(Encryption.cipher.encrypt(b'abc456').decode("utf-8"))
        phnm5 = str(Encryption.cipher.encrypt(b'1000000004').decode("utf-8"))

        nm6 = str(Encryption.cipher.encrypt(b'Susan').decode("utf-8"))
        Pwd6 = str(Encryption.cipher.encrypt(b'abc789').decode("utf-8"))
        phnm6 = str(Encryption.cipher.encrypt(b'1000000005').decode("utf-8"))

        persons = [[nm1, 23, phnm1, 1, Pwd1], [nm2, 25, phnm2, 2, Pwd2],
                   [nm3, 55, phnm3, 3, Pwd3], [nm4, 22, phnm4, 1, Pwd4],
                   [nm5, 26, phnm5, 1, Pwd5], [nm6, 35, phnm6, 2, Pwd6]]

        try:
            cursor.executemany("INSERT INTO Person VALUES (?,?,?,?,?)", persons)
            conn.commit()
            print("Data inserted into Person Table")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data into Person table: {e}")