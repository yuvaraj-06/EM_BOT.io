# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import os
import RPi.GPIO as GPIO
PAGE="""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<img src="stream.mjpg" width="640" height="480">
<br><br>
<br>
<button style="height: 75px; width: 120px" ><a href="/forward"><img style="height: 65px "src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqr4Fvs3wGNhXjMQ8cV_z9AjEOGU-a8zSNKiWNssZd0EXseribaw&s"></a></button>
<img hspace="900" vspace="60" style="padding-left: 5px">
<br>
<button style="height: 75px; width: 120px" <a href="/left"><img style="height: 65px"src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqhLLAg-aZAGnWAifSuTROl4lA6GwlSaeg7F6xvGIjdAJqhjNG2Q&s"></button>
<img hspace="800" vspace="60" style="padding-left: 5px">
<button style="height: 75px; width: 120px" <a href="/stop"><img style="height: 65px"src="data:image/jpeg;base64,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"></button>
<button style="height: 75px; width: 120px" <a href="/right"><img style="height: 65px"src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOcAAADaCAMAAABqzqVhAAAAeFBMVEX///8AAABNTU1CQkI8PDyGhob39/f09PRISEj19fX5+fnW1tYiIiKLi4vQ0NCXl5fCwsIXFxeQkJAPDw8cHBxVVVUmJiaamppiYmJpaWkjIyPLy8sTExOAgIApKSkZGRk0NDTh4eHd3d13d3fq6upTU1NoaGhxcXH6kISsAAAEgUlEQVR4nO3d63LaMBAFYJMLhFwITZqSW2nI9f3fsAYyBNmSLC8L1jnrM/3HjOtvdmUcI8lF0VWmp53914fMdDD42/U5HCAl0wJ0xeSHfjPZoRsmN3SLORjwXnUdJi+0wmRt3RqTE+phMraul8kHDTDZoC7zhRXqMi+KOSe0yizO/zBCa0xOqIdZQula18vkgwaYJfSRCRpkckEjTKbWfYoxea66DUyW1m1kckATmAytm8TEh07SmOitm8wsoZe40It0JnLrtmLiQl/bMVFbtzWzCr3a9xmqZNGeiXjVFTHxoO8yJlrrjqRMLOjoVswsiiEMdPhvBybQGJ3vxIRp3ZPts3ySHAGjdY+2T/JMdAgMqFPQE9EhMFr3ZXcoREXdvzyIocNbBehvAKh7Q0RcUfcG91h0DEAoceuqVBQPSjxGF1bG6KsGFKF19aE3ymeoFDMVveih6YFo3R7aIkZbN1PoRAPqPETMtHU1oGOEMaoCtVJRiKtuP0ZbxEzrjn/BQYVP6vEqKoMCtm4PjWZkZYwCVvRIdAzAq64MCti6ZqAfomOYgUKMUXc2+Z3oGKNnAOhEA4pQUfeZ0b3oGK0qetRN7uYHhg7yiAb0GsA5+NwztCtXLV8K0EjrdsWq522v0K5Unsj2OXEn+wZbtyuUL7K5tmljtCuTN7Iv+6SKdkXyJ/rVsBN08/Hl2bFqzrazvDX4uCtzX/4r8/lQ5uvr7e3vMqdlrq5ubmaz2XBf0M2nmf7WlpbmMbr5MOMJ9wlprCiJsxHK4myC0jgboDzOOJTIGYUyOWNQKmcEyuUMQ8mcQSibMwSlcwagfE4/lNDphTI6fVBKZwU6K1iddSipsxjNXWjvhI6RvjVyHaozKZ3uqukVk9HpqSaj08vkc/qZdM4Ak80ZYpI5g0wuZ5hJ5TTynDpSTSZnlMnjNPK7oJHfedN/t7cyD+Py+EQjobk1q0m3PxNr7n0Ta64PMa8mixxgnlQOMTLvzcg8RiPzUjXmGYfHd1eqWoTzxtOqmY/zQcZEWwew93UdPOt0ZN+9e47+uqssmRMbTP11kVkyVVZFojFp1y3rMwGqqbHcnpYJsAa9ZyYH7hIk3K4m/11cVDarsVFNgD15jOyx1FczOUO0atLuO2myaWn3nDSyh6iRnbg1mABNq8K0Uc1+bOYSIy/s0GACjE0j1VzYYBp54ZU+00g1eZmX2TNH6swsx+b4VoGZf9O67zmlZbrvraVtWvc9xLxMjfdK5397oPKecARmUTjvpxe89x2haZcZP+8ExXhH+DLuXUJLKEo1l3mXQ5GYO0BxmnadhQx6/ojFFELRqrnMa3soIlMAxWRWn1E3Qt2/cnCYLaF4l6CfTNKhqE27TjIUm1mdIR6EumMTccltEhSfmQRFb9p1GqEczEYoQ9OuM41BeZhRqHt7gM2MQLmYQej5nIsZgPIxvVCmS9BPalBOZh1K2LTruNAXVmYVSssMQtmYASgf0wtlZHqgnMwalJVZgfIyHSgzcwvKzdxA2ZnfUH7mCirbDwwt04NW8z/kFFuW/TSJUgAAAABJRU5ErkJggg=="></button>
<br>
<button style="height: 75px; width: 120px" <a href="/back"><img style="height: 65px"src="data:image/png;base64,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"></button>
<img hspace="800" vspace="60" style="padding-left: 5px">

</body>
</html>
"""
red ="""\
<html>
<head>
<meta http-equiv="refresh" content="0;url='\index.html'"/>
</head>
</html>
"""
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == '/forward':
            os.system("/var/www/cgi-bin/forward.cgi")
            content = red.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stop':
            os.system("/var/www/cgi-bin/stop.cgi")
            content = red.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/back':
            os.system("/var/www/cgi-bin/reverse.cgi")
            content = red.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/left':
            os.system("/var/www/cgi-bin/left.cgi")
            content = red.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/right':
            os.system("/var/www/cgi-bin/right.cgi")
            content = red.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(6969)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='320x240', framerate=100) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

