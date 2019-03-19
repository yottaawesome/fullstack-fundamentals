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
            response = 200

            # DB setup
            session = DBSession()
            
            # response setup
            output = "<html><body>"

            if self.path.endswith("/restaurants"):
                # retrieve and format the response
                output += "<h1>Restaurant List</h1>"
                output += '''<p><a href="restaurant/new">Add new restaurant</a></p>'''
                items = session.query(Restaurant).all()
                for item in items:
                    output += "<h2>{}</h2>".format(item.name)
                    output += '''<p><a href="/restaurant/{}/edit">edit</a></p>'''.format(item.id)
                    output += '''<p><a href="/restaurant/{}/delete">delete</a></p>'''.format(item.id)

            elif self.path.endswith("/restaurant/new"):
                output += "<h1>New restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>'''
                output += '''<label for="name">Name:</label>'''
                output += '''<input name="name" type="text">'''
                output += '''<input type="submit" value="Submit"><a href="/restaurants">Cancel</a>'''
                output += '''</form>'''

            elif re.search(r"^/restaurant/\d+/edit$", self.path):
                id = re.findall(r"\d+", self.path)[0]
                restaurant = session.query(Restaurant).filter_by(id = id).one()

                if restaurant:
                    output += "<h1>Edit restaurant {}</h1>".format(restaurant.name)
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/{}/edit'>'''.format(id)
                    output += '''<label for="name">Name:</label>'''
                    output += '''<input name="name" value="{}" type="text">'''.format(restaurant.name)
                    output += '''<input type="submit" value="Submit"><a href="/restaurants">Cancel</a>'''
                    output += '''</form>'''
                else:
                    response = 404
                    output += "<h1>404: restaurant {} does not exist</h1>".format(id)

            elif re.search(r"^/restaurant/\d+/delete$", self.path):
                id = re.findall(r"\d+", self.path)[0]
                restaurant = session.query(Restaurant).filter_by(id = id).one()
                if restaurant:
                    output += '''<h1>Delete restaurant {}?</h1>'''.format(restaurant.name)
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/{}/delete'>'''.format(id)
                    output += '''<p>Are you sure you wish to delete this restaurant?</p>'''
                    output += '''<input type="submit" value="Delete"><a href="/restaurants>Cancel</a>"'''
                    output += '''</form>'''
                else:
                    response = 404
                    output += "<h1>404: restaurant {} does not exist</h1>".format(id)

            else:
                response = 404
                output += "<h1>404: File {} not found</h1>".format(self.path)

            self.send_response(response)
            self.send_header("Content-type", "text/html;charset=utf-8")
            self.end_headers()

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

            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')

                if name and name[0].decode():
                    newRestaurant = Restaurant(name = name[0].decode())
                    session.add(newRestaurant)
                    session.commit()

            elif re.search(r"^/restaurant/\d+/edit$", self.path):
                id = re.findall(r"\d+", self.path)[0]
                restaurant = session.query(Restaurant).filter_by(id = id).one()

                if restaurant:
                    ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
                    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                    
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        name = fields.get('name')

                        if name and name[0].decode():
                            restaurant.name = name[0].decode()
                            session.add(restaurant)
                            session.commit()

            elif re.search(r"^/restaurant/\d+/delete$", self.path):
                id = re.findall(r"\d+", self.path)[0]
                restaurant = session.query(Restaurant).filter_by(id = id).one()
                if restaurant:
                    session.delete(restaurant)
                    session.commit()

            self.send_response(303)
            self.send_header("Location", "http://127.0.0.1:8080/restaurants")
            self.send_header('Content-type', 'text/html;charset=utf-8')
            self.end_headers()

        except:
            raise

        finally:
            if session:
                session.close()