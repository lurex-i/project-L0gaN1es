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

start_images = load_images_from_folder("src\img")
exit_images = load_images_from_folder("src\img")

def random_start_image():
    return random.choice(start_images)

def random_exit_image():
    return random.choice(exit_images)