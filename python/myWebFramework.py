import re
import traceback


class MyWebFramework:
    status_202 = "200 OK"
    status_404 = "404 Not Found"
    status_505 = "505 Internal Error"
    response_header = [("Content-Type", "text/html;charset=UTF-8")]

    def __init__(self, environ, start_response):
        self.status = self.status_202
        self.environ = environ
        self.start_response = start_response
        self.request = self.get_response_body()
        self.ip = self.environ['REMOTE_ADDR']


    def __iter__(self):
        try:
            delegate = self.delegate()
            self.start_response(self.status, self.response_header)
        except:
            # self.start_response(self.status, self.response_header)
            # print (self.response_header)
            self.start_response(self.status_505, self.response_header)
            delegate = "Internal Error: \n\n" + traceback.format_exc()

        if isinstance(delegate, str):
            return iter([delegate])
        else:
            return iter(delegate)

    def header(self, name, value):
        self.response_header.clear()
        self.response_header.append((name, value))

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.paths:
            match = re.match('^' + pattern + '$', path)
            if match:
                args = match.groups()
                match_name = re.match('^' + 'static/(.*)' + '$', name)
                if match_name:
                    name = match_name.groups()[0]

                func_name = method.lower() + '_' + name
                if hasattr(self, func_name):
                    func = getattr(self, func_name)
                    return func(*args)

        return self.notfound()


    def get_response_body(self):

        try:
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        request_body = self.environ['wsgi.input'].read(request_body_size)
        self.request_body = request_body

        try:
            return str(request_body, encoding='utf-8')
        except:
            return request_body
