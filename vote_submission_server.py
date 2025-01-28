import sqlite3 as sql
import socketserver
import Encryption

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

# fetch vote information, validate, then if valid edit BakingContestEntry DB
class	MyTCPHandler(socketserver.BaseRequestHandler):
    def	handle(self):

        # the message received is authenticated using HMAC with Encryption
        #
        # if the message received is authenticated:

        self.data=self.request.recv(1024).strip()

        print("{}	sent message:	".format(self.client_address[0]))
        print(self.data)

        print("Received data:", self.data)

        self.data = str(Encryption.cipher.decrypt(self.data))

        Entry_ID, Excellent_Votes, Ok_Votes, Bad_Votes = self.data.split(".")

        print(f"Entry ID: {Entry_ID}")

        errors = []
        excellent_error = ValidNum(Excellent_Votes)
        ok_error = ValidNum(Ok_Votes)
        bad_error = ValidNum(Bad_Votes)
        entry_id_error = ValidNum(Entry_ID)
        entry_id_exists = ID_Exists(Entry_ID)

        if excellent_error:
            errors.append(excellent_error)
        if ok_error:
            errors.append(ok_error)
        if bad_error:
            errors.append(bad_error)
        if entry_id_error:
            errors.append(entry_id_error)
        if entry_id_exists:
            errors.append(entry_id_exists)
        try:
            con = sql.connect('BakingContestEntry.db')
            cur = con.cursor()
            cur.execute("""
                UPDATE Entry
                SET NumExcellentVotes = NumExcellentVotes + ?,
                    NumOkVotes = NumOkVotes + ?,
                    NumBadVotes = NumBadVotes + ?
                WHERE EntryID = ?""", (Excellent_Votes, Ok_Votes, Bad_Votes, Entry_ID))
            con.commit()
            con.close()
            print(f"Record successfully updated.")
        except:
            print(f"Record could not be updated." + str(errors))



if __name__  ==	"__main__":
    try:
        HOST,	PORT	=	"localhost",	9999
        server	=	socketserver.TCPServer((HOST,	PORT),	MyTCPHandler)
        server.serve_forever()
    except Exception as e:
        print("Error:",e)
        exit(1)
    finally:
        server.shutdown()
        server.server_close()