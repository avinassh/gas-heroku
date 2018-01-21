import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default=5000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('https://avi.im/gg-flip')


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        number = self.get_argument('num', None)
        if not number:
            self.clear()
            self.set_status(400)
            self.write('Invalid Request')
            return
        return self.flip(number)

    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            request = data['num']
        except (ValueError, TypeError, KeyError):
            self.clear()
            self.set_status(400)
            self.write('Invalid Request')
            return
        return self.flip(request=request)

    def options(self):
        self.set_status(204)
        self.finish()

    def flip(self, request):
        if request == '0':
            self.clear()
            self.write('-0')
            return
        if request == '-0':
            self.clear()
            self.write('0')
            return
        try:
            number = int(request)
        except (ValueError, TypeError):
            self.clear()
            self.set_status(400)
            self.write('Invalid Request')
            return
        if number > 9007199254740991:
            self.clear()
            self.set_status(400)
            self.write('Javascript Number Overflow')
            return
        response = {'flipped': -number, 'flippedStr': str(-number)}
        print(response)
        self.write(response)


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/api/v1/flip', MainHandler),
        (r'/api/v1/flip/', MainHandler),
    ])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
