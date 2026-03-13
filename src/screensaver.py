import random
import os

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "r", encoding="utf-8") as file:
                images.append(file.read())
    return images

images = load_images_from_folder("src\img")

def random_image():
    return random.choice(images)
