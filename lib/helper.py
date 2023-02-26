from PIL import Image
from math import ceil

import os
import zipfile
import threading
import subprocess


def write_image(colors : list, width : int = 1920, height : int =1080, filename : str ='image') -> None:
    # Calculate the total number of pixels in the image
    total_pixels : int = width * height

    # Calculate the number of images required to write all the pixels
    num_images : int = ceil(len(colors) / total_pixels)

    # Loop through each image and write the corresponding pixels
    for i in range(num_images):
        # Calculate the start and end indices for the current image
        start_index : int = i * total_pixels
        end_index = min((i + 1) * total_pixels, len(colors))

        # Create a new image with the given dimensions and a transparent background
        image : Image = Image.new('RGBA', (width, height), color=(0, 0, 0, 255))

        # Set the color of each pixel in the current image
        pixel_data = colors[start_index:end_index]
        image.putdata(pixel_data)

        # Save the current image to a file
        image.save(f'{filename}_{i}.png')

        # Print progress message
        progress_pct = (i + 1) / num_images * 100
        print(f'[Writing image] {i+1}/{num_images} [{progress_pct:.2f}%]', end='\r')

    # Print completion message
    print(f'\nWriting complete. {num_images} images written.\n')


def generate_video():
    if not os.path.isdir('output'): os.mkdir('output');
    if os.path.isfile('./output/output.mp4'): os.remove('./output/output.mp4')
    cmd = f"cd {os.getcwd()}; ffmpeg -framerate 30 -i './output/frame_%d.png' -c:v libx264rgb -crf 0 -preset ultrafast -pix_fmt rgb24 './output/output.mp4'"
    
    # Run command and capture output
    result_code = os.system( cmd +" > ./logs/ffmpeg_generate.log 2>&1" )
    return result_code
    

def degenerate_video(video : str) -> int:
    if not os.path.isfile(video): return 1;
    if not os.path.isdir('degenerated'): os.mkdir('degenerated');
    
    cmd = f"cd {os.getcwd()}; ffmpeg -i {video} -vf \"select=gte(scene\,0),setpts=N/FRAME_RATE/TB\" -vsync vfr ./degenerated/output_%04d.png"
    
    return os.system( cmd +" > ./logs/ffmpeg_degenerate.log 2>&1")


def prepare_file(i_file : str) -> bytes:
    filename = f"data.zip"

    # Create a new zip file and add the file to it
    with zipfile.ZipFile(filename, 'w') as zip_file:
        zip_file.write(i_file)

    # Open the file in binary mode and read its contents
    with open(filename, 'rb') as file:
        file_bytes = file.read()

    os.remove('data.zip')
    
    return str( file_bytes.hex() );


# Fix print issue when using Threading
s_print_lock = threading.Lock()
def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)

def deg_line(line: int) -> None:
    # Move cursor to beginning of specified line
    print(f"\033[{line + 1};0H", end="")
       
        
def process_string_part(part, thread_num : int, total_threads : int) -> list:
    # Process a part of the string and return the result
    colors = []
    part_len = len(part)
    spaces = "\033[0H" + ("\n"*(thread_num+1))
    thread_name = ("0" if (thread_num+1) < 10 else "") + str(thread_num+1)            
  
            
    for i in range(0, len(part), 6):
        color = '#' + part[i:i+6]
        
        if i % 10000 == 0 or i <= 2:
            s_print(f"{spaces}Thread[{thread_name}] [{str(i)} / {part_len}] [{color}] {(' '*10)}")

        if len(color) < 7:
            color += 'f' * (7 - len(color))
        rgb_color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        rgba_color = rgb_color + (255,)
        colors.append(rgba_color)
    return colors

def split_string(string, n):
    # Split the string into n parts of equal size
    size = len(string) // n
    parts = [string[i:i+size] for i in range(0, len(string), size)]
    return parts