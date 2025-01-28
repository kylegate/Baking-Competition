"""
Name:(Kyle Webb)
Date:(12/5/24)
Assignment:(Assignment #14)
Due Date:(12/4/24)
About this project:(Flask Website, connects to sqlite database where entries can be added encryption and decryption
added vote feature that also encrypts data with HMAC key and decrypts)
Assumptions:(run DDL/DML for BakingContestEntry and DDL/DML for BakingContestPeople prior to executing main)
All work below was performed by (Kyle Webb)
"""
from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3 as sql
import os
import Encryption
import pandas as pd
import socket
import hmac, hashlib

app = Flask(__name__)

# Query BakingContestEntry DB Entry Table check if ENTRYID exists
def ID_Exists(EntryID):
    con = sql.connect("BakingContestEntry.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Entry WHERE EntryID = ?", (EntryID,))
    result = cur.fetchone() # fetch any matches for EntryID
    con.close()
    if result is not None:
        return None
    else:
        return "Invalid EntryID - EntryID does not exist"


# validate the Name is not empty and does not only contain spaces
def valid_Name(name):
    if name and name.strip():
        return None
    else:
        return "Invalid Name - Name must not be empty and must not contain only spaces.\n"

# validate the LoginPassword is not empty and does not only contain spaces
def valid_Password(password):
    if password and password.strip():
        return None
    else:
        return "Invalid Password - Password must not be empty and must not contain only spaces.\n"


# validate vote number greater than 0
def ValidNum(num):
    if num == "":
        return "Invalid Vote - Vote must not be empty.\n"
    if num.isdigit():
        if (int(num) >= 0):
            return None
    return "Invalid Vote - Vote must be greater than 0.\n"


# validate the Age is a whole number greater than 0 and less than 121
def valid_Age(age):
    if age == "":
        return "Invalid Age - Age must not be empty.\n"
    if age.isdigit():
        if (int(age) > 0) and (int(age) < 121):
            return None
    return "Invalid Age - Age must not be empty and must be between 1 and 3.\n"


# validate the PhoneNumber is not empty and does not only contain spaces
def valid_PhoneNumber(phoneNumber):
    if phoneNumber == "":
        return "Invalid Phone Number - Phone Number must not be empty and must not contain only spaces.\n"
    if phoneNumber.isdigit():
        if (int(phoneNumber) >= 0) and (int(phoneNumber) <= 10000000000):
            return None
    return "Invalid Phone Number - Phone Number must be between 0 and 10 characters.\n"


# validate The SecurityRoleLevel must be a numeric between 1 and 3
def valid_SecurityLevel(securityLevel):
    if securityLevel == "":
        return "Invalid Security Level - Security Level must not be empty and must be between 1 and 3.\n"
    if securityLevel.isdigit():
        if (int(securityLevel) >= 1) and (int(securityLevel) <= 3):
            return None
    return "Invalid Security Level - Security Level must not be empty and must be between 1 and 3.\n"


# homepage
@app.route('/')
def Home():
    if not session.get("logged_in"):
        return render_template('Login.html')
    else:
        nm = Encryption.cipher.decrypt(bytes(session['name'], 'utf-8'))
        return render_template('Home.html', name=nm)


# Add Baking Contestant
@app.route('/Add-Contestant')
def Add_Contestant():
    # Verify login
    if not session.get("logged_in"):
        return render_template('Login.html')
    else:
        return render_template('Add-Contestant.html')


# List all Contestants
@app.route('/Contestants')
def Display_Contestants():
    if not session.get("logged_in"):
        return render_template('Login.html')
    # Display All Contestants
    else:
        con = sql.connect("BakingContestPeople.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from Person")

        df = pd.DataFrame(cur.fetchall(), columns=['Name', 'Age', 'Phone_Number', 'Security_Level', 'Password'])
        print(df.head(10))
        # convert to an array
        index = 0
        for nm in df['Name']:
            nm = str(Encryption.cipher.decrypt(nm))
            df._set_value(index, 'Name', nm)
            index += 1
        index=0
        for phnum in df['Phone_Number']:
            phnum = str(Encryption.cipher.decrypt(phnum))
            df._set_value(index, 'Phone_Number', phnum)
            index += 1
        index = 0
        for psswrd in df['Password']:
            psswrd = str(Encryption.cipher.decrypt(psswrd))
            df._set_value(index, 'Password', psswrd)
            index += 1

        con.close()
        print(df.head(10))
        return render_template("Display_Contestants.html", rows=df)

# Display baking items - queries BakingContestEntry DB
@app.route('/Baking-Items')
def Display_Baking_Entry():
    if not session.get("logged_in"):
        return render_template('Login.html')
    else:
        con = sql.connect("BakingContestEntry.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes from Entry")
        rows = cur.fetchall();
        return render_template("baking-contest-entry.html", rows=rows)


# GET and POST Baking Contest Vote edit and encrypt vote information
@app.route("/Baking-Contest-Vote", methods=['POST', 'GET'])
def Submit_Vote():
    errors = []
    msg = ""
    if request.method == 'POST':
        try:
            Excellent_Votes = request.form['Excellent_Votes']
            Ok_Votes = request.form['Ok_Votes']
            Bad_Votes = request.form['Bad_Votes']
            Entry_ID = request.form['Entry_ID']

            # find any error messages
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

            # Check if there are any error messages
            if errors:
                return render_template("query_result.html", msg=msg, errors=errors)

            Excellent_Votes = int(Excellent_Votes)
            Ok_Votes = int(Ok_Votes)
            Bad_Votes = int(Bad_Votes)
            entry_id = int(Entry_ID)

            # Create and encrypt the message
            message = f"{entry_id}.{Excellent_Votes}.{Ok_Votes}.{Bad_Votes}"
            encrypted_message = Encryption.cipher.encrypt(message.encode('utf-8'))
            HOST, PORT = "localhost", 9999
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT)) # Connect to server and send data
            sock.sendall(encrypted_message)
            sock.close()
            msg = "Vote successfully sent"
        except:
            msg = "Error - Vote NOT sent"

    return render_template("query_result.html", msg=msg, errors=errors)  # Render the result page


# List all Baking Entries
@app.route("/Baking-Entry-Results")
def Display_Entry_Results():
    if not session.get("logged_in") or session.get('Security_Level') < 1:
        return render_template('Login.html')
    else:
        con = sql.connect("BakingContestEntry.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from Entry")
        rows = cur.fetchall();
        return render_template("Baking-Entry.html", rows=rows)


# Add new baking entry
@app.route('/add-baking-entry')
def addBakingEntry():
    if not session.get("logged_in"):
        return render_template('Login.html')
    else:
        return render_template('BakingItem.html')


# Delete Baking Contest Entry using HMAC
@app.route('/delete-baking-entry-hmac')
def deleteBakingEntry():
    if not session.get("logged_in"):
        return render_template('Login.html')
    else:
        return render_template('Delete-Entry-Message.html')


# Edit Baking Entry
@app.route('/edit-baking-entry')
def editBakingEntryVote():
    if not session.get("logged_in"):
        return render_template('Login.html')
    else:
        return render_template('SubmitBakingVote.html')


@app.route('/logout')
def logout():
    session['name'] = ""
    session['logged_in'] = False
    return Home()


@app.route('/login', methods=['POST'])
def Login():
    try:
        name = request.form['username']
        nm = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
        pwd = request.form['password']
        pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

        with sql.connect("BakingContestPeople.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            print(f"username: {nm}, password: {pwd}")

            sql_select_query = """select * from Person where Name = ? and Password = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone();

            if (row != None):
                session['logged_in'] = True
                session['name'] = nm
                session['user_id'] = row[2]
                if int(row['Security_Level']) == 1:
                    session['Security_Level'] = 1
                    print('1')
                elif int(row['Security_Level']) == 2:
                    print('2')
                    session['Security_Level'] = 2
                elif int(row['Security_Level']) == 3:
                    print('3')
                    session['Security_Level'] = 3
                else:
                    session['Security_Level'] = 3
            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return Home()

# delete entryID message
@app.route('/delete-message', methods=['POST'])
def deleteMessage():
    errors = []
    msg = ""
    if request.method == 'POST':
        try:
            # Get form data
            Entry_ID = request.form['Entry_ID']
            # find any error messages
            entry_id_error = ValidNum(Entry_ID)
            entry_id_exists = ID_Exists(Entry_ID)

            if entry_id_error:
                errors.append(entry_id_error)
            if entry_id_exists:
                errors.append(entry_id_exists)
            # Check if there are any error messages
            if errors:
                return render_template("query_result.html", msg=msg, errors=errors)

            # Create and encrypt the message
            encrypted_message = str(Encryption.cipher.encrypt(bytes(Entry_ID, 'utf-8')).decode("utf-8"))

            # HMAC to message
            secret = b'1234'
            hmac_tag = hmac.new(secret, encrypted_message.encode('utf-8'), hashlib.sha3_512).digest()
            message = encrypted_message.encode('utf-8') + hmac_tag

            # connect to localhost at port 8888 and send message
            HOST, PORT = "localhost", 8888
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))  # Connect to server and send data
            sock.sendall(message)
            sock.close()
            msg = "Message to Delete Baking Contest Entry successfully sent"

        except Exception as e:
            print(f"Error: {e}")
            msg = "Error - Message to Delete Baking Contest Entry NOT sent "

        return render_template("query_result.html", msg=msg, errors=errors)  # Render the result page


@app.route('/add-entry', methods=['POST'])
def add_entry():
    errors = []
    msg = ""
    if request.method == 'POST':
        try:

            # Get form data
            name = request.form['Name']
            Excellent_Votes = request.form['Excellent_Votes']
            Ok_Votes = request.form['Ok_Votes']
            Bad_Votes = request.form['Bad_Votes']
            Entry_ID = request.form['Entry_ID']

            # find any error messages
            name_error = valid_Name(name)
            excellent_error = ValidNum(Excellent_Votes)
            ok_error = ValidNum(Ok_Votes)
            bad_error = ValidNum(Bad_Votes)
            entry_id_error = ValidNum(Entry_ID)
            entry_id_exists = ID_Exists(Entry_ID)

            if name_error:
                errors.append(name_error)
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

            # Check if there are any error messages
            if errors:
                return render_template("query_result.html", msg=msg, errors=errors)

            Excellent_Votes = int(Excellent_Votes)
            Ok_Votes = int(Ok_Votes)
            Bad_Votes = int(Bad_Votes)
            entry_id = int(Entry_ID)
            user_id = int(Encryption.cipher.decrypt(bytes(session.get('user_id'), 'utf-8')))

            # If no errors, insert into the database
            with sql.connect("BakingContestEntry.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Entry(EntryID, UserID, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes) VALUES (?,?,?,?,?,?)",
                            (entry_id, user_id, name, Excellent_Votes, Ok_Votes, Bad_Votes))

                con.commit()
                msg = "Record successfully added"
            return render_template("query_result.html", msg=msg, errors=errors)

        except Exception as e:
            error_msg = f"Error in insert operation: {e}"
            errors.append(error_msg)
        return render_template("query_result.html", msg=msg, errors=errors)  # Render the result page


# Validate Input until added to Person Table
@app.route('/addrec', methods=['POST'])
def addrec():
    errors = []
    msg = ""
    if request.method == 'POST':
        try:
            # Get form data
            nm = request.form['Name']
            age = request.form['Age']
            phone_number = request.form['Phone_Number']
            pwd = request.form['Login_Password']
            level = request.form['Security_Level']

            # find any error messages
            name_error = valid_Name(nm)
            age_error = valid_Age(age)
            phone_error = valid_PhoneNumber(phone_number)
            password_error = valid_Password(pwd)
            level_error = valid_SecurityLevel(level)

            if name_error:
                errors.append(name_error)
            if age_error:
                errors.append(age_error)
            if phone_error:
                errors.append(phone_error)
            if level_error:
                errors.append(level_error)
            if password_error:
                errors.append(password_error)

            # Check if there are any error messages
            if errors:
                return render_template("query_result.html", msg=msg, errors=errors)

            name = str(Encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
            password = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))
            age = int(age)
            phone_number = str(Encryption.cipher.encrypt(bytes(phone_number, 'utf-8')).decode("utf-8"))
            level = int(level)

            # If no errors, insert into the database
            with sql.connect("BakingContestPeople.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Person(Name, Age, Phone_Number, Security_Level, Password) VALUES (?,?,?,?,?)",
                            (name, age, phone_number, level, password))
                con.commit()
                msg = "Record successfully added"
            return render_template("query_result.html", msg=msg, errors=errors)

        except Exception as e:
            error_msg = f"Error in insert operation: {e}"
            errors.append(error_msg)

        return render_template("query_result.html", msg=msg, errors=errors)  # Render the result page


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
