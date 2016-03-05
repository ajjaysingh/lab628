from zoodb import *
from debug import *

import time, auth_client

def setup(username):
    db = bank_setup()
    newacc = Bank()
    newacc.username = username
    db.add(newacc)
    db.commit() 

def transfer(sender, recipient, token, zoobars):
    try:
        if auth_client.check_token(sender, token) is False:
            raise AssertionError()
        else: 
            db = bank_setup()
            senderp = db.query(Bank).get(sender)
            recipientp = db.query(Bank).get(recipient)

            sender_balance = senderp.zoobars - zoobars
            recipient_balance = recipientp.zoobars + zoobars

            if sender_balance < 0 or recipient_balance < 0:
                raise ValueError()

            senderp.zoobars = sender_balance
            recipientp.zoobars = recipient_balance
            db.commit()

            transfer = Transfer()
            transfer.sender = sender
            transfer.recipient = recipient
            transfer.amount = zoobars
            transfer.time = time.asctime()

            transferdb = transfer_setup()
            transferdb.add(transfer)
            transferdb.commit()
            return True

    except (KeyError, ValueError, AttributeError, AssertionError) as e:
        return False 

def balance(username):
    db = bank_setup()
    person = db.query(Bank).get(username)
    return person.zoobars

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

