import logging
import tornado.web
import tornado.escape
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import tornado.web
import os.path

define("port", default=8889, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout",AuthLogoutHandler),
            (r"/api/notification/updates",NotificationUpdatesHandler),
            (r"/api/notification/new",NotificationHandler)
            ]
        settings = dict(
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url = "/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape="xhtml_escape",
            )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("user")
        print "USER: ",user
        return user
        
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")

class AuthLoginHandler(BaseHandler):
    def get(self):
        self.write("Need to login")
        #Force the generation of the auth token:
        self.xsrf_token
    def post(self):
        #TODO : authenticate on a stored password HMAC
        #For now, just use whatever name they give us:
        self.set_secure_cookie("user", self.get_argument("name"))
        self.write("Logged in")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("Logged out")

class NotificationMixin(object):
    waiters = []
    
    def new_notifications(self, notifications):
        cls = NotificationMixin
        for callback in cls.waiters:
            try:
                callback(notifications)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.waiters = []

    def wait_for_notifications(self, callback):
        cls = NotificationMixin
        cls.waiters.append(callback)
    
class NotificationHandler(BaseHandler, NotificationMixin):
    @tornado.web.authenticated
    def post(self):
        note = tornado.escape.json_decode(self.get_argument("body"))
        self.new_notifications([note])

class NotificationUpdatesHandler(BaseHandler, NotificationMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        self.wait_for_notifications(self.async_callback(self.on_new_notifications))

    def on_new_notifications(self, notifications):
        if self.request.connection.stream.closed():
            return
        self.finish(dict(notifications=notifications))
        
def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
