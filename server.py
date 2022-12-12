from multiprocessing import Process
from bottle import route, run, template
import concurrent
import detector

latest_id = 0
free_cameras = []

@route('/getid')
def index():
    global free_cameras
    ret = []
    for cam in free_cameras:
        if cam[1] == 0:
            ret.append(cam)
    
    if len(ret) > 0:
        txt = "" + ' ' + str(ret[0][0])
        # for i in range(0,len(ret)):
            # txt += ' ' + str(ret[i][0])
        
        ret[0][1] = True

        return f"{len(ret)>1}{txt}"
    else:
        return "NOROOM"

@route('/get_close_list')
def index():
    with open('/home/croi/polipy/roomsqueue.txt', 'r') as f:
        return f.read()

@route('/add_room')
def index():
    global latest_id
    latest_id += 1
    free_cameras.append([latest_id, 0])
    return "S"

# Process(target=run, kwargs=dict(host='192.168.137.20', port=1234))











































# # import socket
# # import asyncio
# # import os, random

# # HOST, PORT = '192.168.137.20', 1234


# # def send_test_message(message) -> None:
# #     sock = socket.socket(socket.AF_INET,  # Internet
# #                          socket.SOCK_DGRAM)  # UDP
# #     sock.sendto(message.encode(), (HOST, PORT))


# # async def write_messages():
# #     await asyncio.sleep(random.uniform(0.1, 3.0))
# #     send_test_message("HELLO")
# #     print("SENT MESSAGE")


# # class SyslogProtocol(asyncio.DatagramProtocol):
# #     def __init__(self):
# #         super().__init__()

# #     def connection_made(self, transport):
# #         self.transport = transport

# #     def datagram_received(self, data, addr):
# #         if addr[0] == HOST:
# #             return
# #         # Here is where you would push message to whatever methods/classes you want.
# #         print(f"Received Syslog message: {data}")
# #         sock = socket.socket(socket.AF_INET,  # Internet
# #                          socket.SOCK_DGRAM)  # UDP
# #         sock.sendto('0'.encode(), (addr[0], PORT))


# import http.server
# import socketserver

# PORT = 1234



# class handler(http.server.BaseHTTPRequestHandler):
#     latest_id = 0
#     #Handler for the GET requests
#     def __get_id(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/plain')
#         self.end_headers()
#         # Send the html message
#         self.wfile.write(str(self.latest_id).encode())
#         self.latest_id += 1

#     def do_GET(self):
#         if(self.path == "/getid"):
#             self.__get_id()


# Handler = handler

# def start():
#     with socketserver.TCPServer(("192.168.137.20", PORT), Handler) as httpd:
#         print("serving at port", PORT)
