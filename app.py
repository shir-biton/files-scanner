import os
import json
import cgi
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from config import UPLOAD_FOLDER
from utils import scan_file

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST",
                     "CONTENT_TYPE": self.headers["Content-Type"],
                    })

        if "file" not in form.keys():
            self.make_response(json.dumps({"error": "No file received"}), 400)
            return
        
        try:
            input_file = form['file']
            file_name = input_file.filename

            with open(os.path.join(UPLOAD_FOLDER, file_name), "wb") as f:
                f.write(input_file.file.read())

            self.make_response(json.dumps(scan_file(file_name)), 200)            
        except Exception as e:
            self.make_response(json.dumps({"error": "Bad Request"}), 400)
        return

    def make_response(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))  

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True
