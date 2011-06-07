import os
import indicate
import logging

logging.basicConfig()
logger = logging.getLogger("simple_notification.indicator")

default_desktop_file = os.path.join(os.path.split(__file__)[0],"app.desktop")

app_indicator = None
def get_indicator():
    global app_indicator
    if app_indicator:
        return app_indicator
    app_indicator = Indicator()
    return app_indicator


class Indicator(object):
    def __init__(self, desktop_file = default_desktop_file):
        logger.warn("Starting Ubuntu message indicator..")
        server = indicate.indicate_server_ref_default()
        server.connect("server-display", self.__server_click_event)
        server.set_type("message.im")
        server.set_desktop_file(desktop_file)
        server.show()
        self.sources = {} #category name -> indate.Indicator

    def __server_click_event(self, server, some_number_dont_care):
        pass
        
    def __dismiss_event(self, source, some_number_dont_care):
        source.set_property("count","0")
        source.hide()

    def create_source(self,source_name):
        source = indicate.Indicator()
        source.set_property("subtype", "im")
        source.set_property("sender", source_name)
        source.connect("user-display", self.__dismiss_event)
        source.set_property("draw-attention", "true")
        source.set_property("count", "0")
        self.sources[source_name] = source
        return source

    def get_source_for_category(self,category):
        try:
            return self.sources[category.name]
        except KeyError:
            source = self.create_source(category.name)
            return source
    
    def record_message(self, message):
        #Increment the message count for the source
        source = self.get_source_for_category(message.category)
        current_count = int(source.get_property("count"))
        source.set_property("count",str(current_count+1))
        source.show()
