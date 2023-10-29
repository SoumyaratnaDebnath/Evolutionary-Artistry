from PIL import Image
import imageio
import os
import glob

def makeGIF(folder_path, output_gif_filename, duration=10):

    image_paths = glob.glob(os.path.join(folder_path, '*.png'))  
    image_paths.sort()

    images = [Image.open(image_path) for image_path in image_paths]

    images[0].save(
        output_gif_filename,
        save_all=True,
        append_images=images[1:],
        duration=duration,  
        loop=0  
    )

