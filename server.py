#!/usr/bin/python

import socket  # Networking support
import time    # Current time
import threading
import datetime

import re

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
        self.socket.listen(5)
        self.accept_connections()

    def accept_connections(self):
        while True:
            print("Venter på forbindelse..")
            conn, addr = self.socket.accept()
            print("Forbindelse oprettet fra:", addr)
            t = threading.Thread(target=self.client_thread, args=(conn,))
            t.start()
            print("succes")

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

    def client_thread(self, conn):
        #får data fra client
        data = conn.recv(1024)
        print("Data: ", data)
        #string indeholder alt det spændende
        string = bytes.decode(data)
        request_method = string.split(' ')[0]
        print ("Metode:: ", request_method)
        print ("REQ BODY<< ", string + " >>REQ BODY")
        self.logging(string)

        #if string[0:3] == 'GET':
        if (request_method == 'GET') | (request_method == 'HEAD') | (request_method == 'POST'):

            file_requested = string.split(' ')
            file_requested = file_requested[1]

            #Kigger efter URL arguments, fjerner alt efter ?
            file_requested = file_requested.split('?')[0]

            if file_requested == '/test':
                file_requested = 'testfolder/test/test.html'

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
        #Til at holde variabler
        a = 0
        file = open("index.html")
        variablesDict = {}
        htmlArray = file.read().split("\n")
        print(htmlArray)
        if "(start-python-lang)" in htmlArray:
            #Hvis arrayet indeholder (start-python-lang), så forkort arrayet til:
            #index af (start-python-lang)             til index af (end-python-lang)
            pythonLang = htmlArray[htmlArray.index("(start-python-lang)"): htmlArray.index("(end-python-lang)")]
            #looper igennem alt relevant fra html
            for temp in pythonLang:
                if "print(\"" in temp:
                    print(temp[7:-2])
                    continue

                if "var" in temp:
                    variablesDict[temp[4:5]] = temp[8:]

                if "print(" in temp:

                    #Fjerner print foran og parantesen bagerst så vi kun har indholdet
                    content = temp[6:-1]
                    #Deler op i array på mellemrum
                    contentArray = content.split(" ")

                    values = []
                    bool = None
                    #Kører array igennem
                    for symbol in contentArray:

                        #Nu tester jeg om det er variabler eller tal
                        if re.match("^[A-Za-z0-9_-]*$", symbol):
                            #Så skriver den ud hvad A og B er
                            if variablesDict.get(symbol) is not None:
                                values.append(float(variablesDict.get(symbol)))

                        if symbol == '+':
                            bool = "Plus"
                        if symbol == '-':
                            bool = "Minus"
                        if symbol == '*':
                            bool = "Multiplication"
                        if symbol == '/':
                            bool = "Divide"

                    if bool is "Plus":
                        print(values[0]+values[1])

                    if bool is "Minus":
                        print(values[0]-values[1])

                    if bool is "Multiplication":
                        print(values[0]*values[1])

                    if bool is "Divide":
                        print(values[0]/values[1])







    def logging(self, string):
        if "log.txt" is None:
            open("log.txt", "w+")
        file_object = open("log.txt", 'a')
        file_object.write(datetime.datetime.now().isoformat() + "\n \n" + string + "\n \n")
        file_object.close()





print("Starter webserver")
s = Server(80)
s.activate_server()
