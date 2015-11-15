#!/usr/bin/python

import sys
from struct import *
import urllib2, base64
from urllib2 import Request

#global bak
#bak = sys.stdout
#log = open('/tmp/log2', 'w')
#sys.stdout = log
#print "DEBUT"

def from_ejabberd():
#    print "RECEPTION"
    input_length = sys.stdin.read(2)
    (size,) = unpack('>h', input_length)
    res = sys.stdin.read(size).split(':')
#    print res
    return res

def to_ejabberd(bool):
#    print "RETOUR"
    answer = 0
    if bool:
        answer = 1
    token = pack('>hh', 2, answer)
#    print token
    sys.stdout.write(token)
    sys.stdout.flush()
#    print "FIN"

def auth(username, server, password):
#    print username, server, password
    zimbra_token_mode = "zimbra_auth_token++"
    user_login = username+'@'+server
    if password[:len(zimbra_token_mode)] == zimbra_token_mode :
	#TODO : use GetInfoRequest service to check the token instead of downloading the whole inbox.rss
               # we verify the user asscoiated to the token
               # http://community.zimbra.com/collaboration/f/1893/t/1120561
#	print "login", user_login
        password = password[len(zimbra_token_mode):]
        url = "https://localhost/home/"+user_login+"/inbox.rss?auth=qp&zauthtoken="+password
        response = urllib2.urlopen(url)
        if response.getcode() != 200 :
            return False
    else :	
	#TODO : use Zimbra login service to check the user/pass couple instead of downloading the whole inbox.rss
        url = "https://localhost/home/"+user_login+"/inbox.rss"
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (user_login, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        response = urllib2.urlopen(request)
        if response.getcode() != 200:
            return False
#    print "zimbra OK"
    return True

def isuser(username, server):
    return True

def setpass(username, server, password):
    return False

def tryregister(username, server, password):
    return False

def removeuser(username, server):
    return False

def removeuser3(username, server, password):
    return False


#https://www.ejabberd.im/files/doc/dev.html#htoc8
#while 1==2:
while True:
    data = from_ejabberd()
    success = False
    if data[0] == "auth":
        success = auth(data[1], data[2], data[3])
    elif data[0] == "isuser":
        success = isuser(data[1], data[2])
    elif data[0] == "setpass":
        success = setpass(data[1], data[2], data[3])
    elif data[0] == "tryregister":
        success = tryregister(data[1], data[2], data[3])
    elif data[0] == "removeuser":
        success = removeuser(data[1], data[2])
    elif data[0] == "removeuser3":
        success = removeuser3(data[1], data[2], data[3])
    to_ejabberd(success)

#print "resultat : ", auth('admin-adumaine', 'fontaineconsultants.biz','admin-adumaine')
#print "resultat : ", auth('admin-adumaine', 'fontaineconsultants.biz','fake-password')
#print "==============================================="
#print "resultat : ", auth('zimbra_auth_token++admin-adumaine', 'fontaineconsultants.biz','0_456417b1824fb22a72f3266dd29d45348527a651_69643d33363a62383262646263612d646261632d343935642d393436302d3637616236646138353761613b6578703d31333a313434373639333033383030393b76763d313a303b747970653d363a7a696d6272613b7469643d31303a313131303236333538373b76657273696f6e3d31333a382e362e305f47415f313135333b637372663d313a313b')
#print "resultat : ", auth('zimbra_auth_token++admin-adumaine', 'fontaineconsultants.biz','fake-tocken')

sys.stdout = bak
log.close()
