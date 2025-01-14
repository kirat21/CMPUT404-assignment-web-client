#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Abram Hindle, https://github.com/tywtyw2002, https://github.com/treedust and Gurkirat Singh
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
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('latin1')

    def GET(self, url, args=None):
        # print("New test case !!: ", url)
        o = urllib.parse.urlparse(url)
        # print(o)
        host = o.hostname
        if o.port == None:
            port = 80
        else:
            port = o.port

        request = 'GET /'+o.path+' HTTP/1.1\r\nHost: '+o.hostname+'\r\n\r\nConnection: close\r\n\r\n'

        self.connect(host, port)
        self.sendall(request)

        ret = self.recvall(self.socket)
        self.close()

        elements = str(ret.strip('\r\n')).split('\r\n')
        body = elements[len(elements)-1]
        code = elements[0].split()[1]
        # print(code)

        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        #making form data
        form_data = ''
        if args != None:
            # form_data = ""
            # keys = list(args)
            # # print(keys[0])
            # for key_in in range(len(keys)):
            # # for key in keys:
            #     key_split = keys[key_in].split()
            #     #store field name
            #     for i in range(len(key_split)):
            #         if i == len(key_split) - 1:
            #             form_data += key_split[i]+"="
            #         else:
            #             form_data += key_split[i]+"+"

            #     #store value entry
            #     value = args.get(keys[key_in])
            #     value_split = value.split()
            #     for i in range(len(value_split)):
            #         if (i == len(value_split)-1 ) and (key_in == len(keys)-1 ):
            #             form_data += value_split[i]
            #         elif (i != len(value_split)-1 ):
            #             form_data += value_split[i]+"+"
            #         else:#i == len(value_split)-1
            #             form_data += value_split[i]+"&"
            
            # # print(form_data)
            # length = str(len(form_data))
            # print(form_data)

            keys = list(args)
            for key in keys:
                form_data+=key+'='
                value = args.get(key)
                form_data+=value+'&'
            form_data.strip('&')
            length = str(len(form_data))


        else:   # if args == None
            form_data = ''
            length = '0'

        o = urllib.parse.urlparse(url)
        host = o.hostname
        if o.port == None:
            port = 80
        else:
            port = o.port
        
        self.connect(host, port)

        request = "POST /test HTTP/1.1\r\nHost: "+o.hostname+"\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: "+length+"\r\n\r\n"+form_data+"\r\n\r\n"

        self.sendall(request)
        ret = self.recvall(self.socket)
        self.close()

        elements = str(ret.strip('\r\n')).split('\r\n')
        body = elements[len(elements)-1]
        code = elements[0].split()[1]
        # body = ""
        return HTTPResponse(int(code), body)

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
        print(client.command( sys.argv[2], sys.argv[1]))
    else:
        print(client.command( sys.argv[1] ))
