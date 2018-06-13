import socket
import pickle
import io
import time
from timeit import default_timer as timer

class SocketImageClient(object):
    def __init__(self, host, port):
        self.counter = 0
        self.host = host
        self.port = port
        self.socket=socket.socket()
        self.socket.connect((self.host, self.port))      

    def get_image(self):
        data = []
        while True:
            packet = self.socket.recv(4096)
            if not packet:
                break
            data.append(packet)
        image = pickle.loads(b"".join(data))
        self.counter+=1
        return image
    
    def terminate_client(self):
        self.socket.close()


if __name__ == "__main__":
    try:
        while True:
            #client = SocketImageClient('127.0.0.1',8820)
            client = SocketImageClient('192.168.0.100',8820)
            start = timer()
            image = client.get_image()
            print("Got image  {} in {} seconds".format(image["filename"], timer()-start))
            client.terminate_client()
            #time.sleep(5)
    except KeyboardInterrupt:
        print("Bye")

