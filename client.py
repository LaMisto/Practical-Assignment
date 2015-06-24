import socket
import pickle
import struct
import datetime
from time import sleep
import argparse
import utils as u

S = 1
M = S * 60
H = M * 60
D = H * 24
ON = True

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="Default address is 'localhost'")
parser.add_argument("-p", "--port", help="Default port is '8888'", type=int)
args = vars(parser.parse_args())


def send_msg(server, msg):
    msg_ser = pickle.dumps(msg)
    l = struct.pack("!L", len(msg_ser))
    server.send(b"m")
    server.sendall(l + msg_ser)


def close_con(server):
    server.send(b"q")
    server.close()


def server_shutdown(server):
    server.send(b"s")
    server.close()


def get_info():
    info = dict()
    info["os_info"] = u.get_info()
    info["disk_info"] = u.get_disk_info()
    info["virtual_memory_info"] = u.get_virtual_memory_info()
    info["cpu_usage"] = u.psutil.cpu_percent()
    info["processes"] = u.get_process_info()
    info["timestamp"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return info


HOST, PORT = "localhost", 8888
if args["address"]:
    HOST = args["address"]
if args["port"]:
    PORT = args["port"]


def connect():
    new_info = get_info()
    global ON
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Connection cannot be established!")
        ON = False
    else:
        try:
            send_msg(sock, new_info)
        except socket.error.ConnectionResetError:
            print("Connection lost!")
        except:
            print("An error has occurred!")
    finally:
        sock.close()


while ON:
    connect()
    t = datetime.datetime.now().strftime('%H:%M:%S')
    print(str(t) + "\n")
    sleep(10 * M)