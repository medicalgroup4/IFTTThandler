from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import sys
from MQTT import *
from Message import *


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
        print("body: ",body)
        mqtt = MQTT(ip="51.83.42.157", port=1883, qos=2, mode=Message_mode.NON_BLOCKING)
        mqtt.connect()
        mes = body.decode("utf-8")
        print("decoded:", mes)
        
        if Message.is_str_message(mes):
            m = Message.from_string(mes)
            mqtt.publish_message("database/message", m)
            print("sent message to broker")
        else:
            mqtt.publish_string("basestation/startmeasurement", mes)
            print("sent measurement start command to broker")
        mqtt.disconnect()


httpd = HTTPServer(('51.83.42.157', 8081), SimpleHTTPRequestHandler)

httpd.serve_forever()
