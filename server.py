import socket
import threading


class Server:
    def __init__(self):
        self.connections = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('10.103.161.69', 9999))
        self.server_socket.listen(1)
        print("Server is running and listening for connections...")

    def run(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} established.")
                connection_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                connection_handler.start()
                self.connections.append((client_socket, connection_handler))
        except KeyboardInterrupt:
            self.shutdown()

    def handle_client(self, client_socket):
        try:
            client_socket.send(b"Please enter a nickname: ")
            nickname = client_socket.recv(1024).decode().strip()
            ip_address = client_socket.getpeername()[0]
            self.broadcast(ip_address + "|" + f"{nickname} joined the chat!")
            while True:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    break
                elif message.startswith("/nick"):
                    new_nickname = message.split(" ", 1)[1]
                    self.broadcast(f"{nickname} renamed themselves to {new_nickname}")
                    nickname = new_nickname
                elif message == "/quit":
                    self.broadcast(f"{nickname} left the chat!")
                    break
                else:
                    self.broadcast(ip_address + "|" + f"{nickname}: {message}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def broadcast(self, message):
        for connection, _ in self.connections:
            connection.send(message.encode())

    def shutdown(self):
        print("Shutting down the server...")
        for connection, _ in self.connections:
            connection.close()
        self.server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.run()