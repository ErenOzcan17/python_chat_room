import socket
import threading


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 9999))
        self.done = False

    def run(self):
        try:
            input_handler = threading.Thread(target=self.handle_input)
            input_handler.start()

            while not self.done:
                message = self.client_socket.recv(1024).decode().strip()
                if not message:
                    break
                print(message)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_input(self):
        try:
            while not self.done:
                message = input()
                if message == "/quit":
                    self.shutdown()
                self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error: {e}")

    def shutdown(self):
        print("Shutting down the client...")
        self.done = True
        self.client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.run()