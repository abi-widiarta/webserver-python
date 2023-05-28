# import socket yang digunakan untuk berkomunikasi melalui soket.
from socket import *

# Membuat soket server menggunakan protokol IPv4(AF_INET) dengan
# tipe soket TCP (SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Menentukan 8080 sebagai port yang akan digunakan server dan membuat alamatnya
# menjadi "localhost"
serverPort = 8080
serverSocket.bind(("localhost", serverPort))

#soket siap menerima koneksi dari client
# angka 1 menunjukkan jumlah maksimum koneksi yang dapat diterima
serverSocket.listen(1)
print('Ready to serve... \n')

# melakukan looping untuk menerima request client
while True:
    # handshake! soket akan menerima koneksi dari client dan membuat
    # soket koneksi baru 'connectionSocket' dan alamat 'addr' dari client
    connectionSocket, addr = serverSocket.accept()

    # pesan dari client akan diterima melalui soket koneksi dan
    # 1024 merupakan maksimum byte yang akan disimpan dalam var message
    message = connectionSocket.recv(1024)

    # line code ini akan memcah pesan yang diterima dari client
    # dan dimasukkan dalam variabel filename
    try:
        print(f"Message from client:")
        print(message.decode().strip(), end="\n\n")
        filename = message.split()[1][1:]

        # memeriksa apakah nama file kosong, jika kosong maka filename akan dirubah
        # menjadi index.html sebagai default
        if filename == b'':
            filename = b'index.html'

        # file yang direquest client akan dibuka dan isi file tersebut akan disimpan dalam outputdata
        with open(filename, 'rb') as file:
            outputdata = file.read()

        response_header = "HTTP/1.1 200 OK\r\n" #jika berhasil, server akan memberikan response 200 ok

        # Baris dibawah akan menambahkan conten_type berdasarkan ekstensi file yang diminta oleh client
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

    # Baris dibawah akan menangani kemungkinan IOError yang terjadi jika file yang diminta tidak ditemukan
    # response dirubah menjadi 404 Not Found dan content_type diupdate menjadi text/html
    except IOError:
        response_header = "HTTP/1.1 404 Not Found\r\n"
        content_type = "Content-Type: text/html\r\n"
        outputdata = "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()

    # header response dan content type akan diencode menjadi byte dan dikirimkan ke clinet melalui soket koneksi
    # menggunakan metode .send
    connectionSocket.send(response_header.encode())
    connectionSocket.send(content_type.encode())
    
    # new line dikirimkan dan dalam protokol HTTP
    # ini akan menjadi penanda bahwa header telah selesai dan konten akan dimulai 
    connectionSocket.send("\r\n".encode())

    # isi file yang telah disiapkan dikirimkan ke client dan soket ditutup setelahnya
    connectionSocket.send(outputdata)
    connectionSocket.close()

# Semua permintaan telah dilayani, soket ditutup
serverSocket.close()
