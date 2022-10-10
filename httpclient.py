#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2022 Mateo Paez
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split()[1])
        return code
    
    def get_headers(self, data):
        return None

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body
    
    def get_parsed_url(self, url):
        ''' This method parses through the given url to give us the url's host, path, and port. '''
        parsedURL = urllib.parse.urlparse(url)
        self.host = parsedURL.hostname
        # Checking if path is given:
        if parsedURL.path == None or parsedURL.path == '':
            self.path = '/'
        else:
            self.path = parsedURL.path
        # Checking if port is given:
        if parsedURL.port == None:
            self.port = 80
        else:
            self.port = parsedURL.port

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        # Note: This method is for reading the server's reply in response to the client's message
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # Parsing URL:
        self.get_parsed_url(url)

        # Creating the request message to be sent to server:
        request = f"GET {self.path} HTTP/1.1\r\n" \
                  f"Host: {self.host}\r\n" \
                   "Connection: close\r\n" \
                   "Accept: */*\r\n\r\n"

        # Connecting and communicating with the server:
        self.connect(self.host, self.port)
        self.sendall(request)
        response = self.recvall(self.socket)

        # Getting code and body:
        code = self.get_code(response)
        body = self.get_body(response)

        # Printing result of GET and closing connection with server:
        print(body)
        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # Parsing URL and args:
        self.get_parsed_url(url)
        if args == None:
            formData = ""
            contentLength = 0
        else:
            formData = urllib.parse.urlencode(args)
            contentLength = len(formData)

        # Creating request message to be sent to server:
        request = f"POST {self.path} HTTP/1.1\r\n" \
                  f"Host: {self.host}\r\n" \
                   "Content-Type: application/x-www-form-urlencoded\r\n" \
                   "Content-Length: " + str(contentLength) + "\r\n" \
                   "Connection: close\r\n" \
                   "Accept: */*\r\n\r\n" + formData + "\n"

        # Connecting and communicating with the server:
        self.connect(self.host, self.port)
        self.sendall(request)
        response = self.recvall(self.socket)

        # Getting code and body:
        code = self.get_code(response)
        body = self.get_body(response)

        # Printing result of POST and closing connection with server:
        print(body)
        self.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
