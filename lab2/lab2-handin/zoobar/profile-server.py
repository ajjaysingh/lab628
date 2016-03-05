#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import hashlib
import socket
import bank
import bank_client
import zoodb
import time

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor, token):
        self.user = user
        self.visitor = visitor
        self.token = token
        if os.geteuid() is 0:
            os.setresgid(61015, 61015, 61015)
            os.setresuid(61020, 61020, 61020)

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank.get_log(username):
            xfers.append({ 'sender': xfer.sender,
                           'recipient': xfer.recipient,
                           'amount': xfer.amount,
                           'time': xfer.time,
                         })
        return xfers

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': p.profile,
                 'zoobars': bank_client.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank_client.transfer(self.user, target, self.token, zoobars)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, pcode, user, visitor):
        uid = 61018
        
       # localtime = time.asctime(time.localtime(time.time()))
       # userdir = '/tmp/' + (localtime[8]+localtime[17]+localtime[18]+localtime[14]+localtime[15])
        userdir = '/tmp' + '/' + user.replace("/","9")
        if not os.path.exists(userdir):
            os.mkdir(userdir)
            os.chmod(userdir,0770)       
       # print "Directory created " + userdir        
 
        db = zoodb.cred_setup()
        person = db.query(zoodb.Cred).get(user)
        if not person:
            return None
        token = person.token

        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor, token).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)        

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
