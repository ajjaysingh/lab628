from debug import *
from zoodb import *
import rpclib

def login(username, password):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('login', uname = username, pword = password)
        return ret

def register(username, password):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('register', uname = username, pword = password)
        return ret

def check_token(username, token):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('check_token', uname = username, token = token)
        return ret
