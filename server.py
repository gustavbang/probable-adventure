#!/usr/bin/python

import socket  # Networking support
import time    # Current time

class Server:

#Konstruktør
 def __init__(self, port = 80):
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     self.host = ''
     self.port = port

#Aktivererer server
 def activate_server(self):
     self.interpretHtml()
     print("Starter http server på: ", self.host, ":",self.port)
     self.socket.bind((self.host, self.port))
     self._wait_for_connections()

 def _gen_headers(self,  code):

     h = ''
     if code == 200:
        h = 'HTTP/1.1 200 OK\n'
     elif code == 404:
        h = 'HTTP/1.1 404 Not Found\n'

     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

     return h

 def _wait_for_connections(self):
     """ Main loop awaiting connections """
     while True:
         print ("Venter på forbindelse..")
         self.socket.listen(5)

         conn, addr = self.socket.accept()
         print("Får connection fra::", addr)

         #får data fra client
         data = conn.recv(1024)
         print("Data: ", data)
         #string indeholder alt det spændende
         string = bytes.decode(data)

         request_method = string.split(' ')[0]
         print ("Metode:: ", request_method)
         print ("REQ BODY<< ", string + " >>REQ BODY")

         #if string[0:3] == 'GET':
         if (request_method == 'GET') | (request_method == 'HEAD'):

             file_requested = string.split(' ')
             file_requested = file_requested[1]

             #Kigger efter URL arguments, fjerner alt efter ?
             file_requested = file_requested.split('?')[0]

             if file_requested == '/test':
                 file_requested = 'test.html'

             if file_requested == '/':
                 file_requested = 'index.html'

             file_requested = file_requested
             print ("Serving web page [", file_requested, "]")

             try:
                 file_handler = open(file_requested,'rb')
                 if request_method == 'GET':
                     response_content = file_handler.read()
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

                #Hvis fil ikke findes, smides error 404
             except Exception as e:
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self._gen_headers( 404)

                 if request_method == 'GET':
                    response_content = b"<html><body><p>Error 404: File not found</p><p>HTTP server</p></body></html>"

             server_response = response_headers.encode()
             if request_method == 'GET':
                 server_response += response_content

             conn.send(server_response)
             print("Closing connection with client")
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)


 def interpretHtml(self):
     file = open("index.html")
     loop = None
     tmp = file.read().split("\n")
     print(tmp)
     if "(start-python-lang)" in tmp:
         loop = True
         while(loop):
             if "(end-python-lang)" in tmp:
                 loop = False

             if ""






print("Starter webserver")
s = Server(80)
s.activate_server()
