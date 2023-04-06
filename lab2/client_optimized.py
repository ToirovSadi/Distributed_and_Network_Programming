import os
import socket
import time
from PIL import Image
from threading import Thread
from multiprocessing import Pool

SERVER_URL = '127.0.0.1:1234'
FILE_NAME = 'SadiToirov.gif'
CLIENT_BUFFER = 1024
FRAME_COUNT = 5000
n_threads = 50

def download_set_frames(i, n_frames):
    for j in range(n_frames):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ip, port = SERVER_URL.split(':')
            s.connect((ip, int(port)))
            image = b''
            while True:
                packet = s.recv(CLIENT_BUFFER)
                if not packet:
                    break
                image += packet
            with open(f'frames/{i + j}.png', 'wb') as f:
                f.write(image)


def download_frames():
    t0 = time.time()
    if not os.path.exists('frames'):
        os.mkdir('frames')
        
    threads = []
    downloaded_frames = 0
    frame_per_thread = (FRAME_COUNT + n_threads - 1) // n_threads
    for _ in range(n_threads):
        threads.append(Thread(
            target=download_set_frames,
            args=(
                downloaded_frames,
                min(FRAME_COUNT - downloaded_frames, frame_per_thread)
            )
        ))
        downloaded_frames += frame_per_thread
    
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    
    return time.time() - t0


def append_images(frame_id):
    return Image.open(f"frames/{frame_id}.png").convert("RGBA")


def create_gif():
    t0 = time.time()
    frames = []
    
    with Pool() as pool:
        frames = pool.map(append_images, range(FRAME_COUNT))
        frames[0].save(FILE_NAME, format="GIF",
                    append_images=frames[1:], save_all=True, duration=500, loop=0)
        
    return time.time() - t0


if __name__ == '__main__':
    print(f"Frames download time: {download_frames()}")
    print(f"GIF creation time: {create_gif()}")
