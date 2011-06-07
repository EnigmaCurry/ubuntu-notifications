import gtk
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from . import dbus_namespace, dbus_path
from .notify import Message

class DBUSService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(
            dbus_namespace,
            bus=dbus.SessionBus())
        dbus.service.Object.__init__(
            self,bus_name,
            dbus_path)

    @dbus.service.method(dbus_interface=dbus_namespace)
    def notify(self, summary, message, category):
        Message(summary,message,category)
        return 1
    
def run():
    DBusGMainLoop(set_as_default=True)
    service = DBUSService()
    gtk.main()

