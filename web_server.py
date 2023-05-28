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
            content = file.read()

        response_header = "HTTP/1.1 200 OK\r\n".encode()
        if filename.endswith(b".html"):
          response_header += b"Content-Type: text/html\r\n"
        elif filename.endswith(b".css"):
          response_header += b"Content-Type: text/css\r\n"
        elif filename.endswith(b".jpg") or filename.endswith(b".jpeg"):
          response_header += b"Content-Type: image/jpeg\r\n"
        elif filename.endswith(b".svg"):
          response_header += b"Content-Type: image/svg+xml\r\n"
        else:
          response_header += b"Content-Type: text/plain\r\n"

        response_header += "\r\n".encode()
        response = response_header + content
    except IOError:
        response_header = "HTTP/1.1 404 Not Found\r\n".encode()
        response_header += "Content-Type: text/html\r\n".encode()
        response_header += "\r\n".encode()
        response_body = "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()
        response = response_header + response_body

    connectionSocket.sendall(response)
    connectionSocket.close()

serverSocket.close()
