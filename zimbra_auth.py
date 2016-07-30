#!/usr/bin/python

import sys
from struct import *
import urllib2, base64
from urllib2 import Request

global debug_mode
debug_mode = True

if (debug_mode):
    global log
    log = open('/var/log/ejabberd/zimbra_auth', 'a')

def log_file(chain):
   #WARNING : do not use the print/sdout system to log, it breaks ejjaberd link
   if (debug_mode):
        log.write(str(chain)+'\n')

log_file("LOADING SCRIPT")

def from_ejabberd():
    log_file("FROM EJABBERD")
    input_length = sys.stdin.read(2)
    (size,) = unpack('>h', input_length)
    res = sys.stdin.read(size).split(':')
    return res

def to_ejabberd(bool):
    log_file("TO EJABBERD")
    answer = 0
    if bool:
        answer = 1
    token = pack('>hh', 2, answer)
    sys.stdout.write(token)
    sys.stdout.flush()
    log_file("END")

def auth(username, server, password):
    log_file(username+" "+server)
    zimbra_token_mode = "zimbra_auth_token++"
    user_login = username+'@fontaine-consultants.fr'
    if password[:len(zimbra_token_mode)] == zimbra_token_mode :
        #TODO : use GetInfoRequest service to check the token (or the password) instead of downloading the whole calendar.atom
               # we verify the user associated to the token
               # http://community.zimbra.com/collaboration/f/1893/t/1120561
        token = password[len(zimbra_token_mode):]
        url = "https://mail.fontaine-consultants.fr/home/"+user_login+"/calendar.atom?start=0days&end=0days&auth=qp&zauthtoken="+token
        log_file("token "+url)
        response = urllib2.urlopen(url)
        if response.getcode() != 200 :
            return False
    else :
        #TODO : use Zimbra login service to check the user/pass couple instead of downloading the whole inbox.rss
        url = "https://mail.fontaine-consultants.fr/home/"+user_login+"/calendar.atom?start=0days&end=0days"
        log_file("password : "+url)
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (user_login, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try :
           response = urllib2.urlopen(request)
        except Exception as e:
            log_file(e.code)
            return False
    log_file("zimbra OK")
    return True

def isuser(username, server):
    log_file("issuer")
    return True

def setpass(username, server, password):
    log_file("setpass")
    return False

def tryregister(username, server, password):
    log_file("tryregister")
    return False

def removeuser(username, server):
    log_file("remove user")
    return False

def removeuser3(username, server, password):
    log_file("remove user 3")
    return False


def ejabberd_hook():
        log_file("Ready to enter endless ejabberd listening loop")
        while 1==1:
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
                if (debug_mode):
                        log.close()
                        log = open('/var/log/ejabberd/zimbra_auth', 'a')

def test_mode() :
    log_file(auth('adumaine', 'fontaine-consultants.fr','true-password'))
    log_file( auth('admin-adumaine', 'fontaineconsultants.biz','fake-password'))
    log_file("===============================================")
    log_file(auth('zimbra_auth_token++admin-adumaine', 'fontaineconsultants.biz','true-token'))
    log_file(auth('zimbra_auth_token++admin-adumaine', 'fontaineconsultants.biz','fake-token'))

#test_mode()
ejabberd_hook()

log.close()
