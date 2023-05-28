from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)

print('Ready to serve... \n')

while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024)

    try:
        print(f"Message from client:")
        print(message.decode().strip(), end="\n\n")
        filename = message.split()[1][1:]

        if filename == b'':
            filename = b'index.html'

        with open(filename, 'rb') as file:
            outputdata = file.read()

        response_header = "HTTP/1.1 200 OK\r\n"

        if filename.endswith(b".html"):
          content_type = "Content-Type: text/html\r\n"
        elif filename.endswith(b".css"):
          content_type = "Content-Type: text/css\r\n"
        elif filename.endswith(b".jpg") or filename.endswith(b".jpeg"):
          content_type = "Content-Type: image/jpeg\r\n"
        elif filename.endswith(b".svg"):
          content_type = "Content-Type: image/svg+xml\r\n"
        else:
          content_type = "Content-Type: text/plain\r\n"

    except IOError:
        response_header = "HTTP/1.1 404 Not Found\r\n"
        content_type = "Content-Type: text/html\r\n"
        outputdata = "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()

    connectionSocket.send(response_header.encode())
    connectionSocket.send(content_type.encode())
    connectionSocket.send("\r\n".encode())

    connectionSocket.send(outputdata)
    connectionSocket.close()

serverSocket.close()
