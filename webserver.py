from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import cgi
import json
from sqlite_utils import *

myport = 80
msgfile = open("messages.txt","w")
msgfile.write("")
msgfile.close()


class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):        
        self._set_headers()
        data = parse_qs(self.path[2:])
        user = data["user"][0]
        # query = "SELECT sender, receiver, message FROM messages"
        # cursor.execute(query)
        print(f"Retrieving messages for {user}...")
        # Retrieves messages from database
        cur.execute(f"SELECT sender, message FROM messages WHERE receiver = '{user}'")
        results = cur.fetchall()
        
        cursor.execute(f"DELETE FROM messages WHERE receiver = '{user}'")
        con.commit()
        # get it in JSON format
        if results:
            response = json.dumps(
                {'user': user, 'messages': [{'sender': msgInfo[0], 'value': msgInfo[1]} for msgInfo in results]}
            )
        else:
            response = json.dumps({})

        # Returns messages to client
        self.wfile.write(bytes(response,"utf-8"))
    
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

        add_message = "INSERT INTO messages (sender, receiver, message) VALUES ('{0}','{1}','{2}')".format(sender, receiver, message)
        cur.execute(add_message)
        con.commit()

        self.wfile.write(bytes(f"Message from {sender} to {receiver} sent!\n","utf-8"))

def run(server_class=HTTPServer, handler_class=GP, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server running at localhost:80...')
    httpd.serve_forever()

#db is the name of the database, defined in sqlite_utils.py
con = sqlite3.connect(db)
cur = con.cursor()

run(port=myport)
