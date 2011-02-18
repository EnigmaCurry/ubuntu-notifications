import sys
import argparse
import shlex
import logging

from . import __version__
from . import dbus_service, dbus_client
from . import server

def do_serve(args):
    dbus_starter = dbus_service.Starter()
    http_server = server.FlaskApp()
    http_server.start()
    dbus_starter.run()
    
def do_notify(args):
    notify = dbus_client.get_notify()
    notify(args.SUMMARY,args.MESSAGE,args.CATEGORY)

def main():
    parser_template = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser(parents=[parser_template])
    parser.version = "Simple Notification -- {0} -- http://www.enigmacurry.com".format(__version__)
    subparsers = parser.add_subparsers()

    ### Serve
    p_serve = subparsers.add_parser(
        "serve", help="Run the confiugured services [dbus, http]",
        parents=[parser_template])
    p_serve.add_argument("PORT", nargs="?", default="8080",
                         help="TCP port to use")
    p_serve.add_argument(
        "IP_ADDR", nargs="?", default="127.0.0.1",
        help="IP address to bind to. Defaults to loopback only "
        "(127.0.0.1). 0.0.0.0 binds to all network interfaces, "
        "please be careful!")
    p_serve.set_defaults(func=do_serve)

    ### Notify
    p_notify = subparsers.add_parser(
        "notify", help="Send a notification to the local server",
        parents=[parser_template])
    p_notify.add_argument("SUMMARY", nargs="?",
                         help="The message summary")
    p_notify.add_argument("MESSAGE", nargs="?",
                         help="The message contents")
    p_notify.add_argument("CATEGORY", nargs="?",
                         help="The name of the category")
    p_notify.set_defaults(func=do_notify)
    
    if len(sys.argv) <= 1:
        parser.print_help()
        parser.exit(1)
    else:
        args = parser.parse_args()
    args.func(args)
