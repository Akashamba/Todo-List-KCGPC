import sqlite3
from passlib.hash import sha256_crypt


def encrypt(text):
    return sha256_crypt.encrypt(text)


def verify(encrypted, entry):
    return sha256_crypt.verify(entry, encrypted)

3
db = sqlite3.connect('flaskdb', check_same_thread=False)
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Accounts(Name TEXT, Username TEXT PRIMARY KEY,Password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS todo(Task TEXT, Username TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS done(Task TEXT, Username TEXT)''')
db.commit()


def write(username, task):
    c.execute('''INSERT into todo (Task, Username) VALUES(?,?) ''', (task,  username))
    db.commit()


def readtask(username):
    c = db.cursor()
    c.execute('''select Task from todo where Username like (?)''',  (username,))
    data = c.fetchall()
    db.commit()
    return data


def cleartable(username):
    c.execute('''delete from todo where Username like (?)''',  (username,))
    db.commit()


def delete(username, x):
    c.execute('''delete from todo where Username like (?) and Task=?''', (username, x))
    db.commit()


def readcompleted(username):
    c = db.cursor()
    c.execute('''select Task from done where Username like (?) order by Task''',  (username,))
    data = c.fetchall()
    db.commit()
    return data


def deletecompleted(username, x):
    c.execute('''delete from done where Username like (?) and Task=?''', (username, x))
    db.commit()


def deleteallcompleted(username):
    c.execute('''delete from done where Username like (?)''',  (username,))
    db.commit()


def complete(username, x):
    c.execute('''INSERT into done (Username, Task) VALUES(?,?) ''', (username, x))
    c.execute('''delete from todo where Username like (?) and Task=? ''', (username, x))
    db.commit()


def create_acc(name, username, password):
    try:
        c.execute('''INSERT into Accounts(Name, Username, Password) VALUES(?,?,?) ''', (name,  username, encrypt(password)))
        db.commit()
        return True
    except:
        return False


def getusernames():
    c.execute('''SELECT Username from Accounts''')
    return c.fetchall()


def check(name, username, password, cpassword):
    if name is None:
        return False
    if username in getusernames():
        return False
    if password != cpassword:
        return False
    if len(password) <= 8:
        return False
    return True


def clean(list):
    return list[0][0]


def authenticate(username, password):
    try:
        c.execute('''select Username from Accounts where Username=?''', (username,))
        x = clean(c.fetchall())
        c.execute('''select Password from Accounts where Username=?''', (username,))
        y = clean(c.fetchall())
        db.commit()
        if username == x and verify(y, password):
            return True
    except:
        return False
