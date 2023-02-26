import sys
import os
import threading


from PIL import Image
from lib.helper import *
from collections import deque


os.system('cls' if os.name == 'nt' else 'clear')
if not os.path.isdir('logs'): os.mkdir('logs')

i_file = None;
extract = False;
threads = 1

for arg_i,arg in enumerate( sys.argv ):
    arg = arg.lower().replace("-","")
    if arg == "i":
        i_file = sys.argv[ arg_i + 1]
        if not os.path.exists(i_file):
            raise OSError('File does not Exist.')

    elif arg == "t": # reserved for threads
        threads = int( sys.argv[ arg_i + 1] )

    elif arg == "e":
        extract = True

assert i_file != None;

##################################################################################################################################

if not extract:
    
    hex_data_str : str = prepare_file(i_file)

    # Split the hex string into n parts and process each part in a separate thread
    # n = threads  # number of threads
    # parts = split_string(hex_data_str, n)
    # threads = []
    # results = [[] for _ in range(n)]
    
    
    
    
    # for i in range(n):
       
    #     i_value = i
    #     thread = threading.Thread(target=lambda idx, i=i_value, t_i=n: results[idx].extend(process_string_part(parts[idx], i, t_i)), args=(i,))
        
        
    #     thread.daemon = True
    #     thread.start()
    #     threads.append(thread)

    # # Wait for all threads to finish
    # for thread in threads:
    #     thread.join()

    colors = process_string_part(hex_data_str, 0,1)

    n : int = 1
    print("\n"*n)
    
    # Combine the results from all threads and write the output image
    # colors = [color for result in results for color in result]
    if not os.path.isdir('output'): os.mkdir('output')
    write_image(colors, 1920, 1080, './output/frame')
    
    video_result = generate_video();
    
    if video_result == 0:
        print("Generated Video Saved!")
        [os.remove(f"./output/{x}") for x in os.listdir('output') if x.endswith(".png")]
        
    else:
        print("Could not Generate Video!")

##################################################################################################################################

else:
    degenerate_video(i_file)
    
    with open('extracted_data.zip','wb') as hex_file:
        enc_images = os.listdir('./degenerated');        
        for filename in enc_images:
            print( f"Writing: {filename}            " )
            if not filename.endswith('png'): continue;
            
            buffer = deque([], maxlen=100) # used to find ending of file.

            image : Image = Image.open(f"./degenerated/{filename}")
            
            pixels = image.getdata()
            
            for i,rgb_color in enumerate( pixels ):
                extracted_byte = ''.join(format(c, '02x') for c in rgb_color[:3])
            
                buffer.append(extracted_byte)
                if all( [ str(x) == "000000" for x in buffer ] ):
                    break;

                hex_file.write( bytes.fromhex(extracted_byte) )         
                
                if i % 10000 == 0 or i == 0:
                    print( f"\t[ {i} / {len(pixels)}]     ",end="\r")
    
    [os.remove(f"./degenerated/{x}") for x in os.listdir('degenerated') if x.endswith(".png")]
