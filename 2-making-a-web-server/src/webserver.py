# Note that the packages imported were moved from BaseHTTPServer to http.server in Python 3
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("Content-type", "text/html;charset=utf-8")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                
            elif self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header("Content-type", "text/html;charset=utf-8")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
        
        except IOError:
            self.send_error(404, "File not found {}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html;charset=utf-8')
            self.end_headers()

            # getheaders() does not exist in Python3
            ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
            # needed to add this line to fix "can't concat bytes to str" error
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h1> Okay, how about this: </h1>"
            # use decode to clean up the message for display
            output += "<h2>{}</h2>".format(messagecontent[0].decode())
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)

        except BaseException as err:
            print(err.args)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping server")
        server.socket.close()

if __name__ == '__main__':
    main()