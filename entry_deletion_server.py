import sqlite3 as sql
import socketserver
import Encryption
import hmac, hashlib

def ValidNum(num):
    if num == "":
        return "Invalid Vote - Vote must not be empty.\n"
    if num.isdigit():
        if (int(num) >= 0):
            return None
    return "Invalid Vote - Vote must be greater than 0.\n"


def ID_Exists(Entry_ID):
    con = sql.connect("BakingContestEntry.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Entry WHERE EntryID = ?", (Entry_ID,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return None
    else:
        return "Invalid EntryID - EntryID does not exist"

# fetch message, validate, then if valid edit BakingContestEntry DB
class	MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            print("{}	sent message:	".format(self.client_address[0]))
            print(self.data)

            # get HMAC
            hmac_received = self.data[-64:]
            encrypted_message = self.data[:-64]
            # check HMAC
            secret = b'1234'
            hmac_check = hmac.new(secret, encrypted_message, hashlib.sha3_512).digest()
            if hmac_received != hmac_check:
                print("Unauthenticated Delete Baking Contest Entry message received!"
                      " Be on alert! Watch out for bad guys !!!")
                return

            print("Received data:", self.data)
            self.data = str(Encryption.cipher.decrypt(self.data))
            Entry_ID = self.data
            print(f"Entry ID: {Entry_ID}")

            # Validate Entry_ID
            errors = []
            entry_id_error = ValidNum(Entry_ID)
            entry_id_exists = ID_Exists(Entry_ID)
            if entry_id_error:
                errors.append(entry_id_error)
            if entry_id_exists:
                errors.append(entry_id_exists)
            # If there are validation errors, print them
            if errors:
                for error in errors:
                    print(f"Validation error: {error}")
                return

            # If validation passes, delete from the database
            con = sql.connect("BakingContestEntry.db")
            cur = con.cursor()
            cur.execute("DELETE FROM Entry WHERE EntryID = ?", (Entry_ID,))
            con.commit()
            con.close()

            print(f"Entry with Entry_ID {Entry_ID} deleted successfully.")

        except Exception as e:
            print(f"Error processing request: {e}")

if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 8888
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
        exit(1)
    finally:
        server.shutdown()
        server.server_close()
