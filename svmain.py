import asyncio
from multiprocessing import Process
import server 
import detector
import cv2
if __name__ == '__main__':
    server.run(host='192.168.137.20', port=1234)