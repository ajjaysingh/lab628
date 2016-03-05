from debug import *
from zoodb import *
import rpclib

def transfer(sender, recepient, token,zoobars):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('transfer', zsender = sender, zrecepient = recepient, ztoken = token, czoobars = zoobars)

def balance(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', uname = username)
        return ret
'''
def get_log(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('get_log', uname = username)
        return ret
'''
def setup(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        c.call('setup', uname = username)
