import dbus

from . import dbus_namespace, dbus_path

def get_notify():
    bus = dbus.SessionBus()
    notification_service = bus.get_object(dbus_namespace,dbus_path)
    notify = notification_service.get_dbus_method("notify",dbus_namespace)
    return notify
