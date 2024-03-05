import cv2
import mss
import numpy as np
from screeninfo import get_monitors
from ultralytics import YOLO
import mouseController2 as mc
import math
import threading
import time
import torch

torch.cuda.set_device(0)



fov_elements = []

conf_limit = 0.75
team_ident = ""
isFFA = True
showVision = False

def get_center_region(width, height, fov_size):
    center_x, center_y = width // 2, height // 2
    top = center_y - fov_size // 2
    left = center_x - fov_size // 2
    return {'top': top, 'left': left, 'width': fov_size, 'height': fov_size}

def capture_screen(region):
    with mss.mss() as sct:
        screen = sct.grab(region)
        return np.array(screen)[:, :, :3]  # Convert to BGR format

def resize_image_and_boxes(image, boxes, scale_factor):
    resized_image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)
    scaled_boxes = []
    if boxes:
        for box in boxes.xyxy:
            scaled_box = [coordinate * scale_factor for coordinate in box]
            scaled_boxes.append(scaled_box)
    return resized_image, scaled_boxes

def detect_and_display(model, image, scale_factor):
    # Perform detection
    results = model.predict(source=image, verbose=False)
    # Resize image and boxes
    resized_image, scaled_boxes = resize_image_and_boxes(image, results[0].boxes, scale_factor)
    #resized_image, scaled_boxes = image, results[0].boxes
    detections = []

    # Draw results on the resized image
    for detection in results:
        if detection is not None and detection.boxes:
            for i, box in enumerate(scaled_boxes):
                x1, y1, x2, y2 = box
                cp_x = ((int(x1) + int(x2)) / 2) - fov_size/2
                cp_Y = ((int(y1) + int(y2)) / 2) - fov_size/2
                conf, cls_id = detection.boxes.conf[i], detection.boxes.cls[i]
                class_name = detection.names[int(cls_id)]
                detections.append({"x": cp_x, "y": cp_Y, "class_name": class_name, "conf": conf})
                if showVision:
                    cv2.rectangle(resized_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(resized_image, f'{class_name} {conf:.2f}', (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    if showVision: 
        cv2.imshow('YOLOv8 Detection', resized_image)
    return detections

def calc_dist(x,y):
    return math.sqrt(math.pow(x,2)+math.pow(y,2))

def bot_loop():
    global team_ident
    while True:
        heads = []
        bodies = []
        for i in fov_elements:
            if i["class_name"] == "CT_head" or i["class_name"] == "T_head":
                if i["conf"] >= conf_limit:
                    if isFFA or i["class_name"] == f"{team_ident}_head":
                        heads.append(i)
            else:
                if i["conf"] >= conf_limit and i["class_name"] == f"{team_ident}_body":
                    if isFFA or i["class_name"] == f"{team_ident}_body":
                        bodies.append(i)
                
        if len(heads)>0:
            best_dist = 999999
            best = {}
            for i in heads:
                curr_dist = calc_dist(i["x"], i["y"])
                if curr_dist < best_dist:
                    best_dist = curr_dist
                    best = i
            mc.direction = np.array([best["x"], best["y"]])
            # print("head")
        elif len(bodies) > 0:
            best_dist = 999999
            best = {}
            for i in bodies:
                curr_dist = calc_dist(i["x"], i["y"])
                if curr_dist < best_dist:
                    best_dist = curr_dist
                    best = i
            mc.direction = np.array([best["x"], best["y"]])
            # print("body")
        else:
            mc.direction = np.array([0, 0])
            # print("no")
            
        time.sleep(0.001)


def main2():
    global fov_elements, fov_size
    
    # Load the trained YOLO model
    model = YOLO('best.pt')  # Update this path to your trained model
    
    # Get the main monitor's resolution
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height

    # Define the size of the FOV region (in pixels)
    fov_size = 400  # Adjust this based on your requirement

    # Scale factor for resizing image
    scale_factor = 1  # 100x100 to 400x400

    # Calculate the center region
    region = get_center_region(width, height, fov_size)
    # print("starting exec")
    while True:
        screen = capture_screen(region)
        fov_elements = detect_and_display(model, screen, scale_factor)
        # Break the loop if 'h' is pressed
        if cv2.waitKey(1) == ord('h'):
            break

    cv2.destroyAllWindows()
    
def main3():
    global fov_elements, fov_size
    
    # Load the trained YOLO model
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    

    model = YOLO('best.pt').to(device)

    # Define the size of the FOV region (in pixels)
    fov_size = 200  # Adjust this based on your requirement

    # Scale factor for resizing image
    scale_factor = 1  # Adjust scaling if needed
    print(f'Using device: {device}')
    while True:
        # Dynamically get the current screen resolution
        monitor = get_monitors()[0]
        width, height = monitor.width, monitor.height

        # Calculate the center region based on current resolution
        region = get_center_region(width, height, fov_size)

        # Capture screen
        screen = capture_screen(region)

        # Detect and display
        fov_elements = detect_and_display(model, screen, scale_factor)

        # Break the loop if 'h' is pressed
        if cv2.waitKey(1) == ord('h'):
            break

    cv2.destroyAllWindows()
    
def main():
    global fov_elements, fov_size
    
    # Load the trained YOLO model
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    

    model = YOLO('best.pt').to(device)

    # Define the size of the FOV region (in pixels)
    fov_size = 200  # Adjust this based on your requirement

    # Scale factor for resizing image
    scale_factor = 1  # Adjust scaling if needed
    print(f'Using device: {device}')

    # Dynamically get the current screen resolution
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height

    # Calculate the center region based on current resolution
    region = get_center_region(width, height, fov_size)
    while True:
        # Capture screen
        screen = capture_screen(region)

        # Detect and display
        fov_elements = detect_and_display(model, screen, scale_factor)

        # Break the loop if 'h' is pressed
        if cv2.waitKey(1) == ord('h'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    thr = threading.Thread(target=mc.move_mouse_loop4, daemon=True)
    thr.start()

    thr2 = threading.Thread(target=bot_loop, daemon=True)
    thr2.start()

    main()
    
    