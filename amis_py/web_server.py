import re
import sys
import time
import json
import socket
import hashlib
import threading
from urllib import parse


class HttpRequest:

    def __init__(self, request):
        self._request = request

    @property
    def method(self):
        return self._request.splitlines()[0].split()[0]

    @property
    def http(self):
        return self._request.splitlines()[0].split()[2]

    @property
    def path(self):
        data = self._request.splitlines()[0].split()[1]
        data = data.split('?')[0]
        if data != '/':
            return data.rstrip('/')
        return data

    @property
    def paths(self):
        return self.path.split('/')

    @property
    def headers(self):
        return dict(
            x.split(': ') for x in self._request.split(
                '\r\n\r\n')[0].strip().splitlines()[1:])

    @property
    def data_get(self):
        path = self._request.splitlines()[0].split()[1]
        data = path.split('?')
        try:
            return dict(
                parse.unquote_plus(y).split('=') for y in data[1].split('&'))
        except Exception:
            return {}

    @property
    def data_post(self):
        data = self._request.splitlines()[-1]
        try:
            return dict(
                parse.unquote_plus(y).split('=') for y in data.split('&'))
        except Exception:
            return {}

    @property
    def data_json(self):
        data = self._request.splitlines()[-1]
        try:
            return json.loads(data)
        except Exception:
            return {}


class Response:

    def __init__(self):
        self.data = []
        self.raw = []

    def not_found(self):
        self.send('404 Not Found', options={
            'code': '404',
            'status': 'Not Found'
        })

    def bad_request(self):
        self.send('400 Bad Request', options={
            'code': '400',
            'status': 'Bad Request'
        })

    def not_implemented(self):
        self.send('501 Not Implemented', options={
            'code': '501',
            'status': 'Not Implemented'
        })

    def _build_header(self, body, options=None):
        builder = Response.HeaderBuilder(body)
        if options is not None:
            builder.parse(options)
        self.data.extend(builder.build())

    def send(self, body, options={}):
        self._build_header(body, options)
        self.data.append(body)

    def send_json(self, body, options={}):
        body = json.dumps(body)
        options['content-type'] = 'application/json'
        self._build_header(body, options)
        self.data.append(body)

    def send_raw(self, body, options={}):
        self._build_header(body, options)
        self.raw.append(body)

    class HeaderBuilder:
        def __init__(
                self,
                body,
                code='200',
                status='OK',
                content_type='text/plain'):
            self.body = body
            self.code = code
            self.status = status
            self.content_type = content_type
            self.content_length = len(body)
            self.headers = {}

            md5 = hashlib.md5()
            if isinstance(body, str):
                md5.update(body.encode())
            else:
                md5.update(body)
            self.etag = md5.hexdigest()

        def parse(self, data):
            if 'code' in data:
                self.code = data['code']
            if 'status' in data:
                self.status = data['status']
            if 'content-type' in data:
                self.content_type = data['content-type']
            if 'headers' in data:
                self.headers = data['headers']

        def build(self):
            data = []
            data.append('HTTP/1.1 {} {}'.format(self.code, self.status))
            data.append('\nContent-Type: {}'.format(self.content_type))
            data.append('\nContent-Length: {}'.format(self.content_length))
            data.append('\nETag: {}'.format(self.etag))
            for header in self.headers:
                data.append('\n{}: {}'.format(header, self.headers[header]))
            data.append('\nConnection: close\n\n')
            return data


class App:
    def __init__(
            self,
            module=__name__,
            host="0.0.0.0",
            port=8000,
            thread=5):
        self.response = Response()
        self.routes = {}
        self.module = module
        self.port = port
        self.host = host
        self.thread = thread
        self._stopped = False
        self._threads = []

    def _listen(self, socket):
        try:
            while not self._stopped:
                req_conn, req_addr = socket.accept()
                request = req_conn.recv(1024).decode('utf-8')
                self.recv_request(request)
                for res in self.responses:
                    req_conn.send(res)
                req_conn.close()
        except Exception as e:
            print(e)
            req_conn.close()

    def run(self):
        self._stopped = False
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        _socket.bind((self.host, self.port))
        print('server run at {}:{}...'.format(self.host, self.port))
        _socket.listen(10)
        for _ in range(self.thread):
            t = threading.Thread(
                target=self._listen,
                args=(_socket,),
                daemon=True
            )
            self._threads.append(t)
            t.start()
        while True:
            if self._stopped:
                print("stop server")
                break
            for index, _ in enumerate(self._threads):
                if not t.is_alive():
                    print("have dead thread, recreate one")
                    t = threading.Thread(
                        target=self._listen,
                        args=(socket),
                        daemon=True
                    )
                    self._threads[index] = t
                    t.start()
            time.sleep(1)
        print("stop server")
        _socket.shutdown(2)
        _socket.close()

    def recv_request(self, request):
        self.request = HttpRequest(request)

    @property
    def responses(self):
        path = None
        for route in self.routes:
            splited_routes = route.split("/")
            params_keys = []
            params = {}
            for i, r in enumerate(splited_routes):
                if re.match("<(.*)>", r):
                    params_keys.append(r.strip("<").strip(">"))
                    splited_routes[i] = "(.*)"
            if len(splited_routes) != len(self.request.path.split("/")):
                continue
            re_route = "/".join(splited_routes)
            match = re.match(re_route, self.request.path)
            if match:
                path = route
                for index, key in enumerate(params_keys):
                    params[key] = match.groups()[index]
                break

        if path is not None:
            res = self.routes[path](**params)
            if isinstance(res, dict):
                self.response.send_json(res)
            elif isinstance(res, bytes):
                self.response.send_raw(res)
            else:
                self.response.send(str(res))
        else:
            self.response.not_found()

        data = [x.encode() for x in self.response.data]
        data.extend(self.response.raw)

        self.response = Response()
        return data

    def add_route(self, endpoint, view_func):
        self.routes[endpoint] = view_func

    def add_url_rule(
            self,
            rule,
            endpoint=None,
            view_func=None,
            provid_automatic_options=None,
            **options):
        if endpoint is None:
            endpoint = view_func.__name__
        self.add_route(endpoint, view_func)

    def route(self, endpoint):
        def decorate(view_func):
            self.add_route(endpoint, view_func)
            return view_func
        return decorate

    def stop(self):
        self._stopped = True
