import numpy as np
import scipy.signal
from PIL import Image, ImageOps
import cv2
import matplotlib.pyplot as plt
import os
import shutil

class GameOfLifeArt:
    def __init__(self, input_image, num_generations, progress_bar=None):
        self.image = Image.open(input_image).convert('1')
        self.output_image = 'outputGOL.png'
        self.num_generations = num_generations
        self.progress_bar = progress_bar

        # create a blank image
        blank_image = Image.new('RGB', self.image.size, (255, 255, 255))
        blank_image.save(self.output_image)

        # create folder to save images
        folder_name = 'GOL_images'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            # delete the folder and create a new one
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)

    # function to convert a interger to 12 digit string
    def int2str(self, num):
        return str(num).zfill(12)
    
    def save_colored(self, array, index):
        img = Image.open(self.output_image)
        colorR = np.random.randint(0, 255, array.shape)
        colorG = np.random.randint(0, 255, array.shape)
        colorB = np.random.randint(0, 255, array.shape)
        # colorR, colorG, colorB = 255, 255, 255
        r = array * colorR
        g = array * colorG
        b = array * colorB
        img = np.dstack((r, g, b))
        img = Image.fromarray(img.astype(np.uint8))
       
        # edged = self.image
        # for i in range(edged.size[0]):
        #     for j in range(edged.size[1]):
        #         if edged.getpixel((i, j)) == 0:
        #             img.putpixel((i, j), (0, 0, 0))
        
        # img = ImageOps.invert(img)
        img.save('GOL_images/' + self.int2str(index) + '.png')
        img.save(self.output_image)

    def game_of_life(self, binary_image, num_generations):
        def apply_rules(arr):
            neighbors = scipy.signal.convolve2d(arr, np.ones((3, 3)), mode='same', boundary='wrap') - arr
            new_state = np.logical_or(np.logical_and(arr, neighbors == 2), neighbors == 3)
            return new_state.astype(int)
        input_array = 1 - np.array(binary_image, dtype=int)
        for generation in range(num_generations):
            input_array_temp = apply_rules(input_array)
            if np.array_equal(input_array, input_array_temp):break
            else:input_array = input_array_temp
            if generation % int(self.num_generations/200) == 0: # display 200 images in total
                self.save_colored(input_array, generation)
            self.progress_bar.empty()
            self.progress_bar.progress((generation/self.num_generations), text='Game of Life in Progress')
        return input_array
    
    def run(self):
        self.game_of_life(self.image, self.num_generations)


