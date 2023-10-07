import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('10.0.0.222', 12345))
client_socket.connect(('127.0.0.1', 12345))
payload = "Hello, world!"

try:
    while True:
        client_socket.send(payload.encode())
        data = client_socket.recv(1024)
        print(data.decode())
        more = input("Want to send more data to the server? (y/n): ")
        if more.lower() == 'y':
            payload = input("Enter payload: ")
        else:
            break
except KeyboardInterrupt:
    print("Exited by user")
client_socket.close()