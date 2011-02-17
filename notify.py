import indicate
import os
import pynotify
import gtk, gtk.gdk

def click(*args):
    pass

def create_notification_server():
    server = indicate.indicate_server_ref_default()
    server.connect("server-display", click)
    server.set_type("message.im")
    server.set_desktop_file(os.path.abspath("app.desktop"))
    server.show()
    return server
    
def visual(summary, message, icon_path=None):
    note = pynotify.Notification(summary, message)

    if icon_path:
        note.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file(icon_path))
    note.show()


if __name__ == '__main__':
    server = create_notification_server()
    raw_input("Press Enter to quit")
