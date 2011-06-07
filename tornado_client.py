import logging
from urlparse import urljoin
from urllib import urlencode
from Cookie import SimpleCookie
import tornado.httpclient
import json

from simple_notification import notify

class HTTPClient(object):
    def __init__(self, http_client=None):
        self.http_client = http_client if http_client else \
            tornado.httpclient.HTTPClient()
        self.cookies = SimpleCookie()

    def get(self, url, data=None, headers={}): 
        if data is not None: 
            if isinstance(data, dict): 
                data = urlencode(data) 
            if '?' in url: 
                url += '&%s' % data 
            else: 
                url += '?%s' % data 
        return self.__fetch(url, 'GET', headers=headers)
    
    def post(self, url, data, headers={}): 
        if data is not None: 
            if isinstance(data, dict): 
                data = urlencode(data) 
        return self.__fetch(url, 'POST', data, headers)
    
    def __fetch(self, url, method, data=None, headers={}):
        #Send the cookies that have been previously set
        if len(self.cookies) > 0:
            headers["Cookie"] = self.cookies.output(attrs=[],
                header="",sep=";").strip()

        response = self.http_client.fetch(url, method=method,
                                          body=data, headers=headers)
        try:
            #Record any new cookies set
            self.cookies.update(SimpleCookie(response.headers["Set-Cookie"]))
        except KeyError:
            pass

        return response

class NotificationClient(HTTPClient):
    def __init__(self,url):
        HTTPClient.__init__(self)
        self.url = url

    def post(self, url, data, headers={}):
        if self.xsrf_token:
            data["_xsrf"] = self.xsrf_token
        return super(NotificationClient, self).post(url, data, headers)
    
    def login(self, username, password):
        if not self.xsrf_token:
            self.get(urljoin(self.url, "/auth/login"))
        return self.post(urljoin(self.url,"/auth/login"), {"name":username})
    
    def get_notifications(self):
        while True:
            try:
                #TODO: pass in a cursor of the last update seen
                #Otherwise, we might miss notifications
                resp = self.post(urljoin(self.url, "/api/notification/updates"), {})
                print resp.body
                notes = json.loads(resp.body)
                for note in notes["notifications"]:
                    notify.Message(note["summary"],note["message"],note["category"])
            except tornado.httpclient.HTTPError, e:
                if e.code != 599:
                    logging.error("Bad response from server",exc_info=True)

    def new_notification(self, notification):
        resp = self.post(urljoin(self.url, "/api/notification/new"), {"body":notification})
        return resp
        
    @property
    def xsrf_token(self):
        try:
            return self.cookies["_xsrf"].value
        except KeyError:
            return None
        
def main():
    client = NotificationClient("http://localhost:8889")
    client.login("asdf","asdf")
    client.get_notifications()

if __name__ == "__main__":
    main()
