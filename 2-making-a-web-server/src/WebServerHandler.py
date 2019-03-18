from http.server import BaseHTTPRequestHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi
import re

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # response setup
            self.send_response(200)
            self.send_header("Content-type", "text/html;charset=utf-8")
            self.end_headers()

            # DB setup
            session = DBSession()
            
            # response setup
            output = "<html><body>"

            if self.path.endswith("/restaurants"):
                # retrieve and format the response
                output += "<h1>Restaurant List</h1>"
                items = session.query(Restaurant).all()
                for item in items:
                    output += "<h2>{}</h2>".format(item.name)

            elif self.path.endswith("/restaurants/new"):
                output += "<h1>New restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new'>'''
                output += '''<label for="message">Name:</label>'''
                output += '''<input name="message" type="text">'''
                output += '''<input type="submit" value="Submit">'''
                output += '''</form>'''

            elif re.search(r"^/restaurant/\d+/edit$", self.path):
                id = re.findall(r"\d+", self.path)[0]
                output += "<h1>Edit restaurant {}</h1>".format(id)

            else:
                self.send_error(404, "File not found {}".format(self.path))
                return

            output += "</body></html>"
            self.wfile.write(output.encode())

        except:
            raise

        finally:
            if session:
                session.close()

    def do_POST(self):
        try:
            # DB setup
            session = DBSession()

            if self.path.endswith("/new"):
                pass

            elif re.search(r"^/restaurant/\d+/edit$", self.path):
                pass

            

        except:
            raise

        finally:
            if session:
                session.close()