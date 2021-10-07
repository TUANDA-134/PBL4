#!/usr/bin/env python3

import socket

s = socket.socket()   
host = socket.gethostname()
port = 55555                
s.bind((host, port))       

s.listen(5)                 
while True:
    c, addr = s.accept()    
    print ( addr,c.recv(10240000))
    c.close()       