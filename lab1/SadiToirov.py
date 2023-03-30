import argparse
import os
import socket

MSS = 20476  # MSS = Server buffer size (20480) - data header size (4)

parser = argparse.ArgumentParser()
parser.add_argument("server_port", type=str)
args = parser.parse_args()
server_port = int(args.server_port)
server_ip = '127.0.0.1'

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind((server_ip, server_port))

print(f'({server_ip}, {server_port}): Listening...')

# receive start packet from client
data, addr = udp_socket.recvfrom(MSS)
data = data.decode().split('|')
if data[0] != 's':
    print('Server: expected start comand "s", got:', data[0])
    exit(1)

print(addr, '|'.join(data))
seqno = (int(data[1]) + 1) % 2
file_name = data[2]
file_size = int(data[3])
packet = f'a|{seqno}'
udp_socket.sendto(packet.encode(), addr)

if not os.path.exists(file_name):
    print(f"{(server_ip, server_port)}: rewriting the file: {file_name}")

# open file a start receiving data and write it to the file
file = open(file_name, "bw")
while True:
    data, addr = udp_socket.recvfrom(MSS)
    if data[0:1].decode() != 'd':
        print('Server: expected data comand "d", got:', data[0:1].decode())
        exit(1)
    print(addr, data)
    seqno = (int(data[2:3].decode()) + 1) % 2
    file.write(data[4:])
    packet = f'a|{seqno}'
    udp_socket.sendto(packet.encode(), addr)
    file_size -= len(data[4:])
    
    if file_size <= 0:
        print(f'{(server_ip, server_port)}: Received {file_name}.')
        break

file.close()