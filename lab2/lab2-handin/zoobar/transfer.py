from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import bank_client
import traceback

@catch_err
@requirelogin
def transfer():
    warning = None
    if 'recipient' in request.form:
        zoobars = eval(request.form['zoobars'])
        boole = bank_client.transfer(g.user.person.username,
                        request.form['recipient'], g.user.token, zoobars)
        if boole is True:
            warning = "Sent %d zoobars" % zoobars
        else:
            traceback.print_exc()
            warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
