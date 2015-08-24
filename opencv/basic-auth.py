from cherrypy.lib import auth_basic
import cherrypy

USERS = {'jon': 'secret'}

class RootServer:
    @cherrypy.expose
    def index(self):
        return """This is a private page!"""

def validate_password(username, password):
    if username in USERS and USERS[username] == password:
       return True
    return False

conf = {
   '/': {
       'tools.auth_basic.on': True,
       'tools.auth_basic.realm': 'localhost',
       'tools.auth_basic.checkpassword': validate_password
    }
}

cherrypy.quickstart(RootServer, '/', conf)