# -*- coding: utf-8 -*-
import pycurl
import urllib

# auth data
USERS = {'test': 'test'}

# new data to save
data = {'artist': 'Ее глаза', 'title': 'Bi2'}

curl = pycurl.Curl()
curl.setopt(pycurl.URL, "https://0.0.0.0:8888/admin")
curl.setopt(pycurl.VERBOSE, 1)
curl.setopt(pycurl.POST, 1)
curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
# curl.setopt(pycurl.USERPWD, '%s:%s' % ('test', 'test'))
curl.setopt(pycurl.USERPWD, 'test:test')
curl.setopt(pycurl.SSL_VERIFYPEER, 0)
curl.setopt(pycurl.SSL_VERIFYHOST, 0)
curl.setopt(pycurl.CAINFO, "/etc/cert1.pem")
curl.perform()


# cat pycurl_create_empty_shared_list.py
# !/bin/env python

# import pycurl
# import json

# url = 'http://127.0.0.1:8080/list'
# headers = {'Content-Type': 'application/json'}
# payload = {'name':'hi'}
# post = json.dumps(payload)

# def createList():
#      c = pycurl.Curl()
#        c.setopt(pycurl.URL, '%s' % url)
#        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json'])
#        c.setopt(pycurl.VERBOSE, 0)
#        c.setopt(pycurl.USERPWD, 'admin:admin')
#        c.setopt(pycurl.POST, 1)
#        c.setopt(pycurl.POSTFIELDS, post)
#        c.perform()