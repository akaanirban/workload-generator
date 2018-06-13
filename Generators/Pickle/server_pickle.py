import socket
import time
import random
import os
import copyreg
import io
import logging
import cv2
import pickle
import queue
from threading import Thread
from collections import deque


logging.basicConfig(format='%(asctime)s Content: %(message)s',level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

class SendImage(Thread):
    """Threaded Image Sender """
    def __init__(self, queue, folderPath, chunk_size=1, repeat_images = True):
        Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.source_path = folderPath
        self.chunk_size = chunk_size
        self.all_files = []
        self.counter = 0
        self.get_all_files()
        self.repeat_images_flag = repeat_images
        self.totalcounter = 0

    def get_all_files(self):
        try:
            if os.path.exists(self.source_path):
                for filename in os.listdir(self.source_path):
                    self.all_files.append(self.source_path + os.sep + filename)
        except Exception as e:
            logger.error(msg=str(e))

    def increment_counter(self):
        self.counter = self.counter + 1
        if self.repeat_images_flag is True and self.counter >= len(self.all_files):
            self.counter = 0
        self.totalcounter = self.totalcounter+ 1

    def run(self):
        while True:
            if not self.queue.full():
                image = self.all_files[self.counter]
                imagename = image.split(os.sep)[-1]
                image_ndarray = cv2.imread(image)
                self.queue.put(pickle.dumps({"filename": imagename, "payload":image_ndarray}))
                self.increment_counter()
                logger.info(msg = "Sent image: {}, total count {}".format(imagename, self.totalcounter))

    def getImage(self):
        image =  self.queue.get()
        self.queue.task_done()
        return image

if __name__ == "__main__":
    try:
        image_queue = queue.Queue(maxsize=3)
        image_sender = SendImage(image_queue, "/home/anirban/Pictures/First200/")
        image_sender.start()


        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#        server_socket.bind(('127.0.0.1',8820))
        server_socket.bind(('192.168.0.103',8820))
        server_socket.listen(1)

        while True:
            (client_socket, client_address) = server_socket.accept()
            pickled_image = image_sender.getImage()
            client_socket.send(pickled_image)
            client_socket.close()
        server_socket.close()
    except KeyboardInterrupt:
        server_socket.close()
        print("Bye...")

























