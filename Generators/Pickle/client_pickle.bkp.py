import socket
import pickle # cPickle is considerably more efficient than pickle
import copyreg
import io
from PIL import Image#, ImageGrab
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def displayImage(image):
    plt.imshow(image)
    plt.show()

  
counter = 0
while True:
    start = timer()

    data = []
    my_socket=socket.socket()
    my_socket.connect(('127.0.0.1',8820))
    while True:
        #my_socket.send(client_input)
        packet = my_socket.recv(4096)
        #scr = Image.open(io.BytesIO(data))
        if not packet:
            break
        data.append(packet)
    image = pickle.loads(b"".join(data))
    #print(image.shape)
    #displayImage(image)
    print(image["filename"])
    time.sleep(5)
    print("Got image  {} in {} seconds".format(counter, timer()-start))
    counter+=1

    
#cv2.imshow('Image',data)
#my_socket.close()
