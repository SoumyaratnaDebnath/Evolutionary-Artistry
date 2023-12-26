import pygad
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.metrics import structural_similarity
import networkx as nx
import os
from PIL import Image, ImageOps
import shutil

class GeneticAlgoArt:
    def __init__(self, num_generations = 100, sol_per_pop = 100, image_size=512, save_frequency=10, progress_bar=None):
        self.num_generations = num_generations
        self.sol_per_pop = sol_per_pop
        self.image_size = image_size
        self.num_parents_mating = int(sol_per_pop/4)
        self.dimentions = 2
        self.image_name = 'inputGA.png'
        self.random_mutation_min_val = 10
        self.random_mutation_max_val = self.image_size
        self.result_image = [int(self.image_size/2), int(self.image_size/2)]
        self.reference_image = self.edgeDetection(self.image_name, self.image_size)
        self.reference_mse = 0
        self.save_frequency = save_frequency
        self.progress_bar = progress_bar
        self.function_inputs = []
        for i in range(self.dimentions):
            self.function_inputs.append(np.random.randint(0, self.image_size))
        
        # create folder to save images
        folder_name = 'GA_images'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            # delete the folder and create a new one
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)

    def edgeDetection(self, img, img_size):
        img = cv2.imread(img)
        # Resize the image to reduce the computational cost of edge detection
        img = cv2.resize(img, (img_size, img_size))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to the grayscale image to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Apply Laplacian of Gaussian (LoG) for edge detection
        edged = cv2.Laplacian(blurred, cv2.CV_64F)
        # Convert the floating-point image to an unsigned 8-bit image
        edged = np.uint8(np.absolute(edged))
        return edged

    def IntAndBound(self, x):
        x = [int(i) for i in x]
        x = [i % self.image_size for i in x]
        return x

    def findMSE(self, img1, img2):
        return np.square(np.subtract(np.array(img1).flatten(), np.array(img2).flatten())).mean()
    
    def findSSIM(self, img1, img2):
        return structural_similarity(np.array(img1).flatten(), np.array(img2).flatten())
    
    def make_image(self, size, points):
        img = Image.new('L', size, 0)
        draw = ImageDraw.Draw(img)
        for p in range(0, len(points), 2):
            draw.point((points[p+1], points[p]), fill=255)
        img = ImageOps.invert(img)
        return img

    # def make_image_display(self, size, points):
    #     num_points = len(points) // 2
    #     # Convert points to a numpy array for efficient calculations
    #     points_array = np.array(points).reshape((num_points, 2))
    #     # Calculate and store all pairwise distances
    #     distances = np.sqrt(((points_array[:, None] - points_array) ** 2).sum(axis=2))
    #     # Create a graph to represent the points and distances
    #     G = nx.Graph()
    #     for i in range(num_points):
    #         G.add_node(i, pos=(points[i * 2], points[i * 2 + 1]))
    #     for i in range(num_points):
    #         for j in range(i + 1, num_points):
    #             distance = distances[i, j]
    #             G.add_edge(i, j, weight=distance)
    #     # Calculate the minimum spanning tree using Kruskal's algorithm
    #     T = nx.minimum_spanning_tree(G)
    #     # Create the image
    #     img = Image.new('L', size, 0)
    #     draw = ImageDraw.Draw(img)
    #     # Draw the edges from the minimum spanning tree
    #     for edge in T.edges():
    #         i, j = edge
    #         x1, y1 = points[i * 2], points[i * 2 + 1]
    #         x2, y2 = points[j * 2], points[j * 2 + 1]
    #         # Compare squared distance to avoid square root calculation
    #         if (x1 - x2)**2 + (y1 - y2)**2 < (self.image_size * 0.2) ** 2:
    #             draw.line((y1, x1, y2, x2), fill=255, width=1)
    #     # invert the image
    #     img = ImageOps.invert(img)
        
    #     return img

    def make_image_display(self, size, points):
        num_points = len(points) // 2
        # Convert points to a numpy array for efficient calculations
        points_array = np.array(points).reshape((num_points, 2))
        sorted_indices = np.argsort(points_array[:, 0])  # Sort points by x-coordinate

        # Create the image
        img = Image.new('L', size, 0)
        draw = ImageDraw.Draw(img)

        # Initialize the starting point as the leftmost point
        start_point = sorted_indices[0]
        x, y = points_array[start_point]
        visited = set([start_point])

        while len(visited) < num_points:
            min_distance = float('inf')
            closest_point = None

            for i in range(num_points):
                if i not in visited:
                    distance = ((x - points_array[i, 0]) ** 2 + (y - points_array[i, 1]) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_point = i

            x2, y2 = points_array[closest_point]
            draw.line((y, x, y2, x2), fill=255, width=1)
            visited.add(closest_point)
            x, y = x2, y2

        # Invert the image
        img = ImageOps.invert(img)

        return img
    
    def fitness_func(self, ga_instance, solution, solution_idx):
        solution = self.IntAndBound(solution)
        return self.reference_mse + self.reference_image[solution[0]][solution[1]]

    def int2str(self, num):
        return str(num).zfill(12)

    def write_text_on_image(self, image, text):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 12)
        text_color = (128,)
        text_position = (5, 5)
        draw.text(text_position, text, font=font, fill=text_color)
        return image
        
    def on_generation(self, ga_instance):
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        solution = self.IntAndBound(solution)
        self.result_image.append(solution[0])
        self.result_image.append(solution[1])
        self.reference_mse = self.fitness_func(ga_instance, solution, solution_idx)
        instance = ga_instance.generations_completed
        if instance % self.save_frequency == 0:
            # img = self.make_image((self.image_size, self.image_size), self.result_image)
            img = self.make_image_display((self.image_size, self.image_size), self.result_image)
            img = self.write_text_on_image(img, 'Generation: ' + str(instance))
            img.save('GA_images/' + self.int2str(instance) + '.png')
            self.progress_bar.empty()
            self.progress_bar.progress((instance/self.num_generations), text='Genetic Algorithm in Progress')
        if instance == self.num_generations-1:
            self.progress_bar.empty()
            self.progress_bar.progress((instance/self.num_generations), text='Finishing Up')
            img = self.make_image_display((self.image_size, self.image_size), self.result_image)
            # img = self.make_image((self.image_size, self.image_size), self.result_image)
            img.save('outputGA.png')
    
    def run(self):
        ga_instance = pygad.GA(
                        num_generations=self.num_generations,
                        num_parents_mating=self.num_parents_mating,
                        fitness_func=self.fitness_func,
                        sol_per_pop=self.sol_per_pop,
                        num_genes=len(self.function_inputs),
                        init_range_low = 0,
                        init_range_high= self.image_size,
                        on_generation=self.on_generation,
                        random_mutation_min_val=self.random_mutation_min_val,
                        random_mutation_max_val=self.random_mutation_max_val,
                    )
        ga_instance.run()
    