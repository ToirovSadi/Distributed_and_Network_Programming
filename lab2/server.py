import socket
import random
from PIL import Image
from io import BytesIO
from threading import Thread

server_ip = '127.0.0.1'
server_port = 1234
server = (server_ip, server_port)
BUFFER_SIZE = 1024

def generate_image(save=False, filename='gen_image.png', height=10, width=10):
    imarray = [[(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        255
        ) for _ in range(width)] for _ in range(height)]
    im = Image.new('RGBA', (width, height))

    for y in range(height):
        for x in range(width):
            im.putpixel((x, y), (imarray[y][x]))
    if save:
        im.save(filename, "PNG")
    
    cin = BytesIO()
    im.save(cin, "PNG")
    return cin.getvalue()
    

def handle_connection(conn, addr):
    image = generate_image()
    conn.sendall(image)
    print(f'Sent an image to {addr}')
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(server)
    s.listen()
    print(f'Listening on {server}')
    
    while True:
        try:
            conn, addr = s.accept()
            Thread(args=(conn, addr), target=handle_connection).start()
        except KeyboardInterrupt:
            print('Shutting down the server...')
            s.close()
            exit()
        
