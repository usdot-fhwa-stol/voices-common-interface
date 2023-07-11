import glob
import os
import sys
import time

from find_carla_egg import find_carla_egg

carla_egg_file = find_carla_egg()

sys.path.append(carla_egg_file)


import argparse
import logging
from numpy import random
import carla
import numpy as np

def find_camera_sensor(world, camera_id):
    """Find and return camera sensor by ID."""
    for actor in world.get_actors():
        if actor.id == camera_id and actor.type_id.startswith('sensor.camera.'):
            return actor
    return None

def process_image(image):
    """Process an image from the CARLA simulator."""
    # Convert the raw image data to a NumPy array
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))  # RGBA image
    array = array[:, :, :3]  # Remove alpha channel
    array = array[:, :, ::-1]  # Convert from BGR to RGB

    # Now `array` is an RGB image that you can use. For example, you can display it:
    import matplotlib.pyplot as plt
    plt.imshow(array)
    plt.show()

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    camera_id = 10  # The ID of the camera sensor you're interested in
    camera = find_camera_sensor(world, camera_id)

    if camera is not None:
        print(f"Found camera sensor with id {camera_id}.")
        
        # Set the function that will be called when the camera receives an image
        camera.listen(process_image)
        
        while True:
            # Keep the script running; images are processed by `process_image` function
            pass
    else:
        print(f"No camera sensor found with id {camera_id}.")

if __name__ == '__main__':
    main()


