import socket
import threading


class ClientSocket:
    def __init__(self):
        self.check = None

        self.registred = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.checked(login, passw)
        self.runs = True
        self.shutdown = True
        self.reads = ("registers", "registered", "commands", "chat", "getparams")

    def connect(self, ip, port=1802):
        if ip != '':
            try:
                self.check = True
                return self.sock.connect((ip, port))
            except OSError as e:
                self.check = False
            else:
                self.check = True
        else:
            self.check = False

    def checked(self, login, passw):
        print(login, passw)
        try:
            msg = "{}${}$registers".format(login, passw)
            self.sock.send(msg.encode())
        except:
            print('asdasda')
            self.runs = False
            self.sock.close()
            return False
        else:
            self.potok()
            return True

    def potok(self):
        self.potok = threading.Thread(target=self.run)
        self.potok.start()
        return self.potok

    def run(self):
        try:
            while self.runs:
                try:
                    data = self.sock.recv(1024)
                    if "quit" == data.decode():
                        self.sock.send(b'')
                    elif data == b'':

                        self.registred = False
                        print('Ошибка в потоке')
                        self.sock.send(b'')
                        self.runs = False
                        self.potok.join()
                    else:
                        data = data.decode('utf-8')
                        if data == "registered":
                            self.registred = True
                            print('Авторизация пройдера')
                except:
                    self.sock.close()
                    self.runs = False
                    self.shutdown = False
                    self.quit()
                print(data.decode())
        except:
            self.runs = False

    def push_comm(self, comm=None):
        try:
            if comm is None:
                self.sock.send("quit".encode('utf-8'))
            else:
                message = "{}${}${}".format(comm, self.reads[2], self.reads[1]).encode('utf-8')
                self.sock.send(message)

        except:
            try:
                self.sock.send("quit".encode('utf-8'))
            except:
                pass

    def quit(self):
        self.sock.close()
