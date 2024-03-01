import cv2
import mss
import numpy as np
import time
import os
import keyboard
from screeninfo import get_monitors
import datetime

def get_center_region(width, height, fov_size):
    center_x, center_y = width // 2, height // 2
    top = center_y - fov_size // 2
    left = center_x - fov_size // 2
    return {'top': top, 'left': left, 'width': fov_size, 'height': fov_size}

def capture_screen(region):
    with mss.mss() as sct:
        screen = sct.grab(region)
        return np.array(screen)

def save_image(image, count, ident):
    filename = f'training_images/image_{ident}_{count}.png'
    cv2.imwrite(filename, image)

def main():
    # Get the main monitor's resolution
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height
    
    someDate = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Define the size of the FOV region (in pixels)
    fov_size = 200  # Adjust this based on your requirement

    # Calculate the center region
    region = get_center_region(width, height, fov_size)

    # Create a directory to store images
    if not os.path.exists('training_images'):
        os.makedirs('training_images')

    count = 0
    print("Press 'e' to capture images. Press 'h' to quit.")

    while True:
        if keyboard.is_pressed('e'):
            screen = capture_screen(region)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            save_image(screen, count, someDate)
            count += 1
            time.sleep(0.3)

        if keyboard.is_pressed('h'):
            break

        time.sleep(0.1)

if __name__ == "__main__":
    main()
