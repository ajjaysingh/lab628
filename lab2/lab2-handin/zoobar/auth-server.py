#!/usr/bin/python

import rpclib
import sys
import auth
from debug import *

class AuthRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_register(self, uname, pword):
        return auth.register(uname, pword)

    def rpc_login(self, uname, pword):
        return auth.login(uname, pword)

    def rpc_check_token(self, uname, token):
        return auth.check_token(uname, token) 

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
