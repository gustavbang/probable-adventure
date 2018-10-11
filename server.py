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
     print("Starter http server på: ", self.host, ":",self.port)
     self.socket.bind((self.host, self.port))
     self._wait_for_connections()

 def _gen_headers(self,  code):

     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
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
         self.socket.listen(5) # maximum number of queued connections

         conn, addr = self.socket.accept()
         print("Får connection fra::", addr)

         data = conn.recv(1024) #receive data from client
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

             #Kigger efter URL arguments
             file_requested = file_requested.split('?')[0]  # disregard anything after '?'

             if (file_requested == '/test'):  # in case no file is specified by the browser
                 file_requested = 'test.html' # load index.html by default

             if (file_requested == '/'):  # in case no file is specified by the browser
                 file_requested = 'index.html' # load index.html by default


             file_requested = file_requested
             print ("Serving web page [",file_requested,"]")

             ## Load file content
             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'GET'):  #only read the file when GET
                     response_content = file_handler.read() # read file content
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

             except Exception as e: #in case file was not found, generate 404 page
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self._gen_headers( 404)

                 if (request_method == 'GET'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'GET'):
                 server_response +=  response_content  # return additional conten for GET only

             conn.send(server_response)
             print ("Closing connection with client")
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)


print ("Starter webserver")
s = Server(80)
s.activate_server()