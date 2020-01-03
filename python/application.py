import json
import os
import re
from urllib.parse import unquote

from myWebFramework import MyWebFramework
from resolution import resolution
from connect import SSHConnect
from session import Session

HOME_DIR = '/home'
class Application(MyWebFramework):

    # routes
    paths = (
        ("/getlist", "getlist"),
        ("/download", "download"),
        ("/upload(.*)", "upload"),
        ("/signup", "signup"),
        ("/login(.*)", "login"),
        ("/logout", "logout"),

        ("/home/(.*)", "home"),

        ("/static/js/(.*)", "static/js"),
        ("/static/css/(.*)", "static/css"),
        ("/(.*)", "index")
    )

    def get_index(self, name):
        self.header('Content-type', 'text/html')
        sess = Session()
        user = sess.get_session(self.ip)
        if user is None:
            yield self.redict('/login').encode('utf-8')

        else:
            if user == 'None':
                yield self.redict('/login').encode('utf-8')
            user = str(user, encoding='utf-8')
            # print (user)
            if name != user:
                yield self.redict('/' + user).encode('utf-8')
            else:
                params = name.split('?', 1)
                username = params[0]
                location = ''
                if len(params) > 1:
                    location = params[1]

                response_body = ''
                for line in open('html/index.html', 'r'):
                    line = resolution.resolute(self, line)
                    response_body = response_body + line
                yield response_body.encode('utf-8')

    def get_js(self, name):
        # print(name)
        self.header('Content-type', 'application/javascript')
        with open("static/js/" + name, 'r') as f:
            response_body = f.read()
        yield response_body.encode('utf-8')

    def get_css(self, name):
        self.header('Content-type', 'text/css')
        with open("static/css/" + name, 'r') as f:
            response_body = f.read()
        yield response_body.encode('utf-8')

    def get_login(self, status):
        self.header('Content-type', 'text/html')
        response_body = ''
        for line in open('html/login.html', 'r'):
            line = resolution.resolute(self, line, {'status': status})
            response_body = response_body + line
        yield response_body.encode('utf-8')

    def post_login(self, status):
        params = self.request.split('&')
        username = params[0].split('=')[1]
        password = params[1].split('=')[1]
        conn = SSHConnect()
        check_login = conn.check_login(username, password)

        if check_login == "OK":
            print('login success')
            sess = Session()
            sess.set_sessoion(self.ip, username)
            yield self.redict('/'+username).encode('utf-8')
        else:
            yield self.redict('login' + check_login).encode('utf-8')

    def get_signup(self, status):
        self.header('Content-type', 'text/html')
        response_body = ''
        for line in open('html/sign.html', 'r'):
            line = resolution.resolute(self, line, {'status': status})
            response_body = response_body + line
        yield response_body.encode('utf-8')

    def post_signup(self):
        params = self.request.split('&')
        username = params[0].split('=')[1]
        password = params[1].split('=')[1]
        conn = SSHConnect()
        status = conn.signup(username, password)

        if status == "OK":
            print ('sign success')
            yield self.redict('/login').encode('utf-8')
        else:
            yield self.redict('/login' + status).encode('utf-8')

    def get_logout(self):
        self.header('Content-type', 'text/html')
        sess = Session()
        sess.delete_session(self.ip)
        yield self.redict('/login').encode('utf-8')

    def get_home(self, name):
        name = name.split('/')[-1]
        self.header("content-disposition", "attachment; filename={}".format(name))
        return ''.encode('utf-8')

    def post_upload(self, params):
        self.header('Content-type', 'text/html')
        n, dir, filename = params.split('&')
        requst = re.sub(b'--.*--', b'', self.request_body)
        open(dir + filename, 'wb+').write(requst)
        sess = Session()
        user = sess.get_session(self.ip)

        yield self.redict('/' + str(user, encoding='utf-8')).encode('utf-8')

    def post_getlist(self):
        params = unquote(self.request)
        dir = params.split('=')[1]

        sshc = SSHConnect()
        json = sshc.read_dir(dir)
        print (json)
        yield json.encode('utf-8')

    def notfound(self):
        status = self.status_404
        yield "Not Found".encode('utf-8')

    def redict(self, url):
        red = '<script language="javascript" type="text/javascript"> window.location.href=\'' + url + '\' </script>'
        return red
