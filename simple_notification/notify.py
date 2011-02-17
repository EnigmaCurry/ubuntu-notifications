import pynotify
import gtk, gtk.gdk

from indicator import Indicator

categories = {} #category name -> Category object
app_indicator = Indicator()

class Category(object):
    def __init__(self, name, icon_path=None):
        self.name = name
        self.set_icon_path(icon_path)
        categories[name] = self
    def set_icon_path(self, path):
        self.icon = None
        if path:
            self.icon = gtk.gdk.pixbuf_new_from_file(icon_path)
    
class Message(object):
    def __init__(self, summary, message, category_name=None, notify=True):
        self.summary = summary
        self.message = message
        if category_name == None:
            category_name = "General"
        try:
            self.category = categories[category_name]
        except KeyError:
            self.category = Category(category_name)

        if notify:
            self.notify()
    
    def notify(self):
        note = pynotify.Notification(self.summary, self.message)
        
        if self.category.icon:
            note.set_icon_from_pixbuf(self.category.icon)
        note.show()
        app_indicator.record_message(self)
        
if __name__ == '__main__':
    msg = Message("Summary","This is the message","Ryan")
    msg = Message("Summary","This is another message")
    raw_input("Press Enter to quit")
