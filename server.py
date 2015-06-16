import socket
import pickle
import struct
import sqlite3 as sql


CL_NODE = dict()
CL_ID = 0


def insert_info(os, cpu, v, d, p, time, addr):
    global CL_ID, CL_NODE
    new = True
    node = str(addr) + " " + str(os["node"])
    if node in CL_NODE:
        new = False
    else:
        CL_NODE[node] = CL_ID
        CL_ID += CL_ID
    ins_gen = (CL_NODE[node], os["system"], os["node"], os["platform"], cpu, v["total"], v["used"], v["free"], v["usage"])
    ins_disk = []
    for i in d:
        aux = (CL_NODE[node], time, d[i]["partition"], d[i]["total"], d[i]["used"], d[i]["free"], d[i]["usage"])
        ins_disk.append(aux)
    ins_p = []
    for i in p:
        aux = (CL_NODE[node], time, p[i]["pid"], p[i]["name"], p[i]["username"], p[i]["cpu_usage"], p[i]["memory_usage"], p[i]["threads"])
        ins_p.append(aux)
    conn = None
    try:
        conn = sql.connect('info.db')
        cur = conn.cursor()
        if new:
            cur.execute('INSERT INTO general_info VALUES (?,?,?,?,?,?,?,?,?)', ins_gen)
        cur.executemany('INSERT INTO disk_info VALUES (?,?,?,?,?,?,?)', ins_disk)
        cur.executemany('INSERT INTO process_info VALUES (?,?,?,?,?,?,?,?)', ins_p)
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        print("Error: ", e.args[0])
    else:
        CL_ID += 1
    finally:
        if conn:
            conn.close()


def print_dict(a):
    for i in a:
        print("\n")
        for j in a[i]:
            print(j, ": ", a[i][j])


def process_msg(msg, addr):
    try:
        os_info = msg["os_info"]
        disk_info = msg["disk_info"]
        virtual_memory_info = msg["virtual_memory_info"]
        cpu_usage = msg["cpu_usage"]
        processes = msg["processes"]
        time = msg["timestamp"]
    except KeyError:
        return
    insert_info(os_info, cpu_usage, virtual_memory_info, disk_info, processes, time, addr)


def get_msg(sock):
    cmd = sock.recv(1)
    if cmd == b"q":
        return "quit"
    elif cmd == b"m":
        l = client.recv(4)
        msg_l, = struct.unpack("!L", l)
        msg_ser = client.recv(msg_l)
        msg = pickle.loads(msg_ser)
        return msg
    elif cmd == b"s":
        server_shutdown()
    else:
        return b"???"


def handle_client(sock, addr):
    ad, nr = addr
    msg = get_msg(sock)
    if msg == "quit":
        sock.close()
    elif msg == "???":
        sock.close()
    else:
        sock.close()
        process_msg(msg, ad)


def server_shutdown():
    server.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8888))
server.listen(10)


try:
    while 1:
        (client, address) = server.accept()
        print("A client with address:", address, "has connected!")
        handle_client(client, address)
except KeyboardInterrupt:
    print("Shutdown!")
    server.close()


