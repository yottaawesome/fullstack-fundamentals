# Note that the packages imported were moved from BaseHTTPServer to http.server in Python 3
from http.server import BaseHTTPRequestHandler, HTTPServer
from WebServerHandler import WebServerHandler

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping server")
        server.socket.close()

if __name__ == '__main__':
    main()