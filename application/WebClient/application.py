#Application entry point for client.
from settings import settings
from url import urls
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado import httpserver
from tornado import options

def main():
    app = Application(urls, **settings)
    options.parse_command_line() #cli logging
    server = httpserver.HTTPServer(app, xheaders=True)
    server.bind(9000)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

if __name__ == "__main__":
    main()