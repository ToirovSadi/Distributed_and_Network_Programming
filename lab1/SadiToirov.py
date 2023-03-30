import argparse
import os
import socket

MSS = 20480  # MSS = Server buffer size (20480) - data header size (4)

parser = argparse.ArgumentParser()
parser.add_argument("server_port", type=str)
args = parser.parse_args()
server_port = int(args.server_port)
server_ip = '127.0.0.1'

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind((server_ip, server_port))

class File:
    def __init__(self, file_io=None, size=None, name=None, seqno=1):
        self.file_io = file_io
        self.size = size
        self.name = name
        self.seqno = seqno

files = dict()
print(f'({server_ip}, {server_port}): Listening...')

try:
    while True:
        data, addr = udp_socket.recvfrom(MSS)
        typ = data[0:1].decode()
        if typ == 's':
            data_decoded = data.decode().split('|')
            print(addr, data.decode())
            seqno = (int(data_decoded[1]) + 1) % 2
            file_name = data_decoded[2]
            file_size = int(data_decoded[3])
            packet = f'a|{seqno}'
            udp_socket.sendto(packet.encode(), addr)
            if os.path.exists(file_name):
                print(f"{(server_ip, server_port)}: rewriting the file: {file_name}")
            files[addr] = File(
                file_io=open(file_name, "bw"),
                name=file_name,
                size=file_size,
            )
        elif typ == 'd':
            if(addr not in files):
                print(f'{(server_ip, server_port)}: error got unregistred address')
                continue
            print(addr, data)
            seqno = (int(data[2:3].decode()) + 1) % 2
            if files[addr].seqno != seqno:
                files[addr].seqno = (files[addr].seqno + 1) % 2
                files[addr].file_io.write(data[4:])
                files[addr].size -= len(data[4:])
                if files[addr].size <= 0:
                    print(f'{(server_ip, server_port)}: Received {files[addr].name}.')
                    files[addr].file_io.close()
            packet = f'a|{seqno}'
            udp_socket.sendto(packet.encode(), addr)
        else:
            print(f'{(server_ip, server_port)}: unknown command, got: {typ}')
            break
except KeyboardInterrupt:
    print(f'{(server_ip, server_port)}: Shutting down...')
    udp_socket.close()
    exit(0)

udp_socket.close()