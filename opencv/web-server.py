#! /usr/bin/env python
import random
import cherrypy
import os
import string
from cherrypy.lib import auth_basic

# auth data
USERS = {'jon': 'secret'}

songs = {
    '1': {
        'title': 'Lumberjack Song',
        'artist': 'Canadian Guard Choir'
    },

    '2': {
        'title': 'Always Look On the Bright Side of Life',
        'artist': 'Eric Idle'
    },

    '3': {
        'title': 'Spam Spam Spam',
        'artist': 'Monty Python'
    }
}

def validate_password(username, password):
    if username in USERS and USERS[username] == password:
       return True
    return False

class RootServer:
    @cherrypy.expose
    def index(self, **keywords):
        return """<!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Full Page Background Image | Progressive</title>
            <style> * { margin: 0; padding: 0; }
                html {
                background: url(/static/img/bg.jpg) no-repeat center center fixed;
                -webkit-background-size: cover;
                -moz-background-size: cover;
                -o-background-size: cover;
                background-size: cover;
                }

                #page-wrap { width: 400px; margin: 50px auto; padding: 20px; background: white; -moz-box-shadow: 0 0 20px black; -webkit-box-shadow: 0 0 20px black; box-shadow: 0 0 20px black; }
                H1 { font: 30px/2 Georgia, Serif; margin: 0 0 30px 0; text-indent: 40px; color: white;}
                p { font: 15px/2 Georgia, Serif; margin: 0 0 30px 0; text-indent: 40px; }
                </style>
        </head>

        <body>

        <h1>Hello! This is landing plane counting page!</h1>
        <style type="text/css" style="display: none !important;">
        * {
            margin: 0;
            padding: 0;
        }
        body {
        overflow-x: hidden;
        }
        #demo-top-bar {
            text-align: left;
            background: #222;
            position: relative;
            zoom: 1;
            width: 100% !important;
            z-index: 6000;
            padding: 20px 0 20px;
        }
        #demo-bar-inside {
            width: 960px;
            margin: 0 auto;
            position: relative;
            overflow: hidden;
        }
        #demo-bar-buttons {
        padding-top: 10px;
        float: right;
        }
        #demo-bar-buttons a {
            font-size: 12px;
            margin-left: 20px;
            color: white;
            margin: 2px 0;
            text-decoration: none;
            font: 14px "Lucida Grande", Sans-Serif !important;
        }
        #demo-bar-buttons a:hover,
        #demo-bar-buttons a:focus {
        text-decoration: underline;
        }
        #demo-bar-badge {
            display: inline-block;
            width: 302px;
            padding: 0 !important;
            margin: 0 !important;
            background-color: transparent !important;
        }
        #demo-bar-badge a {
            display: block;
            width: 100%;
            height: 38px;
            border-radius: 0;
            bottom: auto;
            margin: 0;
            background: url(/images/examples-logo.png) no-repeat;
            background-size: 100%;
            overflow: hidden;
            text-indent: -9999px;
        }
        #demo-bar-badge:before, #demo-bar-badge:after {
            display: none !important;
        }
        </style>
        </body>
        </html>"""

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))

    def POST(self, title, artist):
        id = str(max([int(_) for _ in songs.keys()]) + 1)
        songs[id] = {
            'title': title,
            'artist': artist
        }

        return ('Create a new song with the ID: %s' % id)

class Songs:

    exposed = True

    def GET(self, id=None):

        if id is None:
            return('Here are all the songs we have: %s' % songs)
        elif id in songs:
            song = songs[id]

            return(
                'Song with the ID %s is called %s, and the artist is %s' % (
                    id, song['title'], song['artist']))
        else:
            return('No song with the ID %s :-(' % id)

    def POST(self, title, artist):

        id = str(max([int(_) for _ in songs.keys()]) + 1)

        songs[id] = {
            'title': title,
            'artist': artist
        }

        return ('Create a new song with the ID: %s' % id)

    def PUT(self, id, title=None, artist=None):
        if id in songs:
            song = songs[id]

            song['title'] = title or song['title']
            song['artist'] = artist or song['artist']

            return(
                'Song with the ID %s is now called %s, '
                'and the artist is now %s' % (
                    id, song['title'], song['artist'])
            )
        else:
            return('No song with the ID %s :-(' % id)

    def DELETE(self, id):
        if id in songs:
            songs.pop(id)

            return('Song with the ID %s has been deleted.' % id)
        else:
            return('No song with the ID %s :-(' % id)

if __name__ == '__main__':
    server_config={
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8888,

        'server.ssl_module': 'pyopenssl',
        'server.ssl_certificate': '/etc/cert.pem',
        'server.ssl_private_key': '/etc/privkey.pem'
    }

    conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.tree.mount(
        Songs(), '/api/songs',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )

    cherrypy.tree.mount(RootServer(), '/', conf)
    cherrypy.config.update(server_config)
    cherrypy.quickstart(RootServer(), '/', conf)
    # cherrypy.quickstart(RootServer())

# import cherrypy
# import MySQLdb
# from md5 import md5

# class RootServer:
#    @cherrypy.expose
#    def index(self):
#        return """This is a public page!"""

# class SecureServer:
#     @cherrypy.expose
#     def index(self):
#     return "This is a secure section"

# def get_users():
#     db = MySQLdb.connect(host='localhost',
#                         user='db_name',
#                         passwd='db_pass',
#                         db='db_name')
#    curs = db.cursor()
#    curs.execute('select username,password from users')
#    return dict(curs.fetchall())

# def encrypt_pw(pw):
#    return md5(pw).hexdigest()

# if __name__ == '__main__':
#    users = get_users()

#    conf = {'/secure': {'tools.basic_auth.on': True,
#                        'tools.basic_auth.realm': 'Some site2',
#                        'tools.basic_auth.users': users,
#                        'tools.basic_auth.encrypt': encrypt_pw}}
#    root = RootServer()
#    root.secure = SecureServer()
#    cherrypy.quickstart(root, '/', config=conf)