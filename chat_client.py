import threading
import socket
import tkinter
import tkinter.scrolledtext
import traceback


class Client:

    def __init__(self, host='127.0.0.1', port=9090):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def transmit(self, msg: str):
        self.sock.send(msg.encode())

    def receive(self, length=1024):
        x = self.sock.recv(length).decode()
        return x

    def end(self):
        self.sock.close()


class GuiClient(Client):
    def __init__(self, host='127.0.0.1', port=9090):
        Client.__init__(self, host, port)
        self.running = True
        self.gui_done = False
        gui_thread = threading.Thread(target=self.gui_loop)
        rcv_thread = threading.Thread(target=self.rcv)
        gui_thread.start()
        rcv_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()

        self.chat_label = tkinter.Label(self.win, text="Chat:")
        self.chat_label.pack(pady=20, padx=10)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(pady=20, padx=10)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:")
        self.msg_label.pack(pady=20, padx=10)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(pady=20, padx=10)

        self.send_bt = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_bt.pack(pady=20, padx=10)

        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.gui_done = True

        self.win.mainloop()

    def write(self):
        msg = f"{self.input_area.get('1.0', 'end')}"
        self.transmit(msg)
        self.input_area.delete('1.0', 'end')

    def close(self):
        self.running = False
        self.win.destroy()
        self.end()
        exit(0)

    def rcv(self):
        while self.running:
            try:
                msg = self.receive()
                if self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', msg)
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                traceback.print_exc()
                self.end()
                self.running = False
                break

    def main(self):
        GuiClient()


if __name__ == '__main__':
    GuiClient().main()