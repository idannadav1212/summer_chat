import socket
import threading


class Server:

    def __init__(self, conns=100, host='0.0.0.0', port=9090):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(conns)

    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg.encode())

    def handle(self, client):
        while True:
            try:
                msg = client.recv(1024).decode()
                print(msg)
                self.broadcast(msg)
            except:
                self.clients.remove(client)
                client.close()
                break

    def receive(self):
        print("in receive")
        while True:
            cli_skt, cli_adr = self.server.accept()
            print(f"address {str(cli_adr)} connected.")
            cli_skt.send("Start Of Chat Here".encode())
            self.clients.append(cli_skt)
            self.broadcast("new connection...")
            cli_skt.send("connected".encode())
            thread = threading.Thread(target=self.handle, args=(cli_skt,))
            """handle without () so it treats it as object comma in args so it treats it as tuple, it does nothing by 
            itself; args is the output while target is the 'program' we will run in the thread """
            thread.start()

    def main(self):
        print("Server Running...")
        threading.Thread(target=self.receive).start()


if __name__ == '__main__':
    Server().main()
