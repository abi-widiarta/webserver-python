from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080
serverSocket.bind(("localhost",serverPort))
serverSocket.listen(1)

while True:
  print('Ready to serve...')

  connectionSocket, addr = serverSocket.accept()

  try:
    message = connectionSocket.recv(1024)
    filename = message.split()[1]

    if filename[1:] == b'':
      f = open('index.html')
    else:
      f = open(filename[1:])
    outputdata = f.read()

    # -- yang berubah
    connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
    connectionSocket.send("Content-Type: text/html\r\n".encode())
    connectionSocket.send("\r\n".encode())
    # ---------------

    for i in range(0, len(outputdata)):
      connectionSocket.send(outputdata[i].encode())

    connectionSocket.close()

  except IOError:
    # -- yang berubah
    connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
    connectionSocket.send("Content-Type: text/html\r\n".encode())
    # ---------------
    connectionSocket.send("<html><head></head<body><h1>404 Not Found</h1></body></html>\r\n".encode())
    connectionSocket.close()

serverSocket.close()