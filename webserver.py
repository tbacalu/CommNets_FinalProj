from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import cgi
import json

myport = 80
msgfile = open("messages.txt","w")
msgfile.write("")
msgfile.close()


class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        print(self.path)
        print(parse_qs(self.path[2:]))

        query = "SELECT sender, receiver, message FROM messages"
        # cursor.execute(query)
        with open("messages.txt",'r') as msgfile:
            self.wfile.write(str(json.load(msgfile)))
        
        # self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        sender =  form.getvalue("sender")
        receiver =  form.getvalue("receiver")
        message = form.getvalue("message")

        # add_message = "INSERT INTO messages (sender, receiver, message) VALUES ('{0}','{1}','{2}')\n".format(sender, receiver, message)
        message_dict = {'sender': sender, 'receiver': receiver, 'message': message}
        # cursor.execute(add_message)
        with open("messages.json","a") as msgfile:
            json.dump(msgfile, message_dict)
        #db.commit()

        self.wfile.write("message from {0} to {1} received!".format(sender, receiver))

def run(server_class=HTTPServer, handler_class=GP, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server running at localhost:80...')
    httpd.serve_forever()

# db = sql.connect(
#     host = "localhost",
#     user = "root",
#     password = "commNets",
#     database = "Messages",
#     port = myport
# )

# cursor = db.cursor()

run(port=myport)
