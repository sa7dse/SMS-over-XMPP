#! /usr/bin/env python
# -*- coding: utf-8 -*-
#xmpp2sms.py
'''
This is a little cli tool to send sms via the aspsms.ch XMPP gateway.
To get this program running you need to download and install XMPPPY from:
http://xmpppy.sourceforge.net/ (best with *nix)

To get to use the service you need  to register
at http://aspsms.ch/registration.asp
Then you need an JID and you need to rigister the service with your JID

author: SlaverIQ
requires: xmpppy
contact:
XMPP: slaveriq@jabber.ccc.de 
version: 1.1
change: Real password input
'''

import xmpp, cPickle

def dbwrite():
    '''
   This function makes sure that the JID(user) and the JID's password(pw) 
   are stored in a binary pickle file. So it's NOT encrypted
    '''
    from os import path
    from os import curdir
    from getpass import getpass
    if not path.isfile(path.join(curdir,'user.db')):
        user= raw_input('Please enter full JID:')
        pw= getpass()
        userpw=(user,
                pw)
        db=file('user.db', 'wb') 
        cPickle.dump(userpw, db, 2)
        db.close()
        return True
    else:
        return True
def dbread():
    '''
    A function that reads the pickled file and then returns username and password in an array.
    '''
    db = file('user.db', 'rb', 2)
    userpw = cPickle.load(db)
    return userpw 
def main():
    '''
    The main function calls the dbwrite and the dbread functions, then makes sure that
    the mobilphone number has the correct syntax and then sends the sms.
    '''
    dprefix= '+45'
    from sys import argv
    args=argv
    if args[1][0] is not '+':
        mbfn= '+' + args[1] +'@aspsms.swissjabber.ch'
    else:
        mbfn=args[1] + '@aspsms.swissjabber.ch'
    msg = ''
    for i in range(len(args)):
        if i is 1:
            pass
        elif i is 0:
            pass
        else:
            msg= msg + args[i] + ' '
    print msg
    print mbfn
    
    if dbwrite():
        userpw = dbread()
        smssend(userpw, mbfn, msg)
def smssend(userpw,mbfn,msg):
    '''
    Sends the SMS. userpw is an array:
    userpw[0] is the JID
    userpw[1] is the password
    mbfn is the mobilphone number with country prefix e.g. +45 for denmark
    msg is the sms content
    '''
    cl=xmppconnect(userpw[0], userpw[1])
    cl.send(xmpp.protocol.Message(mbfn,msg))
    
def xmppconnect(user,pw):
    '''
    Connects to the XMPP server.User has to be your JID and password the JID's password.
    '''
    jid=xmpp.protocol.JID(user)
    cl=xmpp.Client(jid.getDomain(),debug=[])
    cl.connect()
    cl.auth(jid.getNode(),pw)
    return cl
if __name__ == "__main__":
    main() 