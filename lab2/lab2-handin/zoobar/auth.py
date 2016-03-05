from zoodb import *
from debug import *

import hashlib
import random
import pbkdf2
import os, binascii

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if not person:
        return None
    salt = person.hash_string
    hashed_password = pbkdf2.PBKDF2(password, salt).hexread(32)
    if person.password == hashed_password:
        return newtoken(db, person)
    else:
        return None
'''
def credentials(username, password):
    db_cred = cred_setup()
    newcred = Cred()
    newcred.username = username
    newcred.password = password
    db_cred.add(newcred)
    db_cred.commit()
    return newtoken(db_cred, newcred)
'''

def register(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if person:
        return None
    newperson = Cred()
    newperson.username = username
    salt = binascii.b2a_hex(os.urandom(8))   # 64-bit salt
    newperson.password = pbkdf2.PBKDF2(password, salt).hexread(32) 
    newperson.hash_string = salt
    db.add(newperson)
    db.commit()
    #token = newtoken(db, newperson)
    #add password to cred and return token
    token = newtoken(db, newperson)
    return token

def check_token(username, token):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if person and person.token == token:
        return True
    else:
        return False

'''
def newtoken(db, person):
    hashinput = "%s%.10f" % (person.password, random.random())
    person.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return person.token

def login(username, password):
    db = person_setup()
    person = db.query(Person).get(username)
    if not person:
        return None
    if person.password == password:
        return newtoken(db, person)
    else:
        return None

def register(username, password):
    db = person_setup()
    person = db.query(Person).get(username)
    if person:
        return None
    newperson = Person()
    newperson.username = username
    newperson.password = password
    db.add(newperson)
    db.commit()
    return newtoken(db, newperson)

def check_token(username, token):
    db = person_setup()
    person = db.query(Person).get(username)
    if person and person.token == token:
        return True
    else:
        return False
'''
