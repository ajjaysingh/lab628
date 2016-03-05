#!/usr/bin/python
#
# Insert bank server code here.

import rpclib
import sys
import bank
from debug import *

class BankRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_transfer(self, zsender, zrecepient, ztoken, czoobars):
        return bank.transfer(zsender, zrecepient, ztoken, czoobars)

    def rpc_balance(self, uname):
        return bank.balance(uname)

#    def rpc_get_log(self, uname):
 #       return bank.get_log(uname)
    
    def rpc_setup(self, uname):
        bank.setup(uname)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
