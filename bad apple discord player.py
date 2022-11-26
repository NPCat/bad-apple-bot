import discord
import time
from PIL import Image

CONFIG = open('config.txt', 'rt')

FRAMES_PATH = CONFIG.readline().split(' ')[2:][0][:-1] #Get thing after the space after = on line 1 but not the new line charecter

TOKEN = CONFIG.readline().split(' ')[2:][0][:-1] #each time readline is called it just get's the next line so, yeah

CLIP_FRAMES = int(CONFIG.readline().split(' ')[2:][0][:-1])

CLIP_LENGTH = float(CONFIG.readline().split(' ')[2:][0][:-1])

CONFIG.close()

ASCII_CHARS = ['⠀','⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']

WIDTH = 60

TIMEOUT = 1/((int(CLIP_FRAMES/4)+1)/CLIP_LENGTH)*18

def resize(image, new_width=WIDTH):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int((aspect_ratio * new_width)/2)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

def grayscalify(image):
    return image.convert('L')

def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

def do(image, new_width=WIDTH):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index+int(new_width)] for index in range(0, len_pixels, int(new_width))]

    return '\n'.join(new_image)

def runner(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        return
    image = do(image)

    return image

frames = []

for i in range(0, int(CLIP_FRAMES/4)+1):
    path = f"{FRAMES_PATH}/frame"+str(i*4)+".jpg" #<--- path to folder containing every frame of the video
    frames.append(runner(path))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.content.startswith('!bad apple'):
        
        oldTimestamp = time.time()

        start = oldTimestamp

        seconds = 0
        minutes = 0

        i = 0
        
        while i < len(frames)-1:
            disp = False
            while not disp:
                newTimestamp = time.time()
                if (newTimestamp - oldTimestamp) >= TIMEOUT:

                    await message.channel.send(f'```{frames[int(i)]}```') #added `````` for markdown so it's monospace
                    
                    newTimestamp = time.time()

                    i += (newTimestamp - oldTimestamp)/TIMEOUT
                    
                    oldTimestamp = newTimestamp

                    disp = True
client.run(TOKEN)