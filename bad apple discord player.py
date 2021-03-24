import asyncio
import functools
import pathlib
import time

import discord
from PIL import Image

CLIP_FRAMES = 6571

CLIP_LENGTH = 219.0666

ASCII_CHARS = ['⠀', '⠄', '⠆', '⠖', '⠶', '⡶', '⣩', '⣪', '⣫', '⣾', '⣿']
ASCII_CHARS.reverse()
ASCII_CHARS = ASCII_CHARS[::-1]

WIDTH = 60
FPS = CLIP_FRAMES / CLIP_LENGTH
TIMEOUT = 1 / FPS


def resize(image, new_width=WIDTH):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height) / float(old_width)
    new_height = int((aspect_ratio * new_width) / 2)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image


def grayscalify(image):
    return image.convert('L')


def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value // buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)


def do(image, new_width=WIDTH):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index + int(new_width)] for index in range(0, len_pixels, int(new_width))]

    return '\n'.join(new_image)


def runner(path):
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in", path)
        return
    image = do(image)

    return image


frames = []

for i in range(0, CLIP_FRAMES):
    frames_dir = pathlib.Path() / "frames"
    path = frames_dir / f"frame{i}.jpg"  # <--- path to folder containing every frame of the video
    frames.append(runner(path))

FRAME_COUNTER = 0
PREVIOUS_FRAME = None
BOT_COUNT = 0
FRAME_TIMES = []


async def on_message(bot_number, message):
    global FRAME_COUNTER
    global BOT_COUNT
    global PREVIOUS_FRAME
    if message.content.startswith('!bad apple'):
        initial_timestamp = time.time()
        while FRAME_COUNTER < len(frames) - 1:
            await asyncio.sleep(0.005)
            if BOT_COUNT % len(BOT_IDS) != bot_number:
                continue
            while True:
                new_timestamp = time.time()
                FRAME_TIMES.append((new_timestamp - initial_timestamp, new_timestamp, initial_timestamp))
                FRAME_COUNTER = int((new_timestamp - initial_timestamp) / TIMEOUT)
                if FRAME_COUNTER == PREVIOUS_FRAME:
                    continue
                PREVIOUS_FRAME = FRAME_COUNTER
                if FRAME_COUNTER >= len(frames):
                    break
                await message.channel.send(frames[FRAME_COUNTER])
                BOT_COUNT = (BOT_COUNT + 1) % len(BOT_IDS)
                break
        FRAME_COUNTER = 0
        PREVIOUS_FRAME = None
        BOT_COUNT = 0


BOT_1_ID = ''
BOT_2_ID = ''
BOT_3_ID = ''
BOT_4_ID = ''
BOT_5_ID = ''
BOT_6_ID = ''
BOT_7_ID = ''
BOT_8_ID = ''
BOT_IDS = [BOT_1_ID, BOT_2_ID, BOT_3_ID, BOT_4_ID, BOT_5_ID, BOT_6_ID, BOT_7_ID, BOT_8_ID]
threads = []


async def on_ready(client, bot_number):
    print(f'We have logged in as {client.user} {bot_number}')


def build_client(event_loop, i):
    client = discord.Client(loop=event_loop)
    ready_callback = functools.partial(on_ready, client, i)
    ready_callback.__name__ = "on_ready"
    message_callback = functools.partial(on_message, i)
    message_callback.__name__ = "on_message"
    client.event(coro=ready_callback)
    client.event(coro=message_callback)
    return client


async def main():
    event_loop = asyncio.get_event_loop()
    tasks = []
    for i, bot_id in enumerate(BOT_IDS):
        client = build_client(event_loop, i)
        tasks.append(asyncio.ensure_future(client.start(bot_id)))
    await asyncio.wait(tasks)


asyncio.run(main())
