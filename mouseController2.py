import ctypes
import time
import numpy as np
from timeit import default_timer as timer

# Constants for the ctypes mouse event
MOVE_MOUSE = 0x0001

# Set initial direction
direction = np.array([0, 0])  # x, y

# Variables to control speed and frequency
freq_min = 0.001
freq_i_min = 0.01
dist_divider = 100
incr = 1
# minmove = 5
# move_speed = 2 
# speed_m = 0.6
# speed_a = 0.02
# speed_i_m = 1.5
update_frequency = 0.0001 # Time in seconds between updates
init_freq = 0.0001

# Function to move the mouse
def move_mouse(x, y):
    ctypes.windll.user32.mouse_event(MOVE_MOUSE, int(x), int(y), 0, 0)

"""# Function to get current mouse position
def get_mouse_pos():
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return np.array([pt.x, pt.y])

# Function to move towards a target position
def move_towards(target_pos, current_pos):
    direction = target_pos - current_pos
    distance = np.linalg.norm(direction)
    if distance < move_speed:
        return target_pos
    else:
        step = direction / distance * move_speed
        return current_pos + step

"""
        
def dynamic_time_interval(x, y):
    # Example function to calculate dynamic time interval
    # You can replace this with any logic you need
    distance = np.linalg.norm([x, y])
    return max(freq_min, min(freq_i_min, distance / dist_divider)), distance

def move_mouse_loop4():
    global direction, update_frequency
    x_i = direction[0]
    y_i = direction[1]
    x_r = direction[0]
    y_r = direction[1]

    while True:
        if not (x_i == direction[0] and y_i == direction[1]):
            # print("change")
            x_r = direction[0]
            y_r = direction[1]
            x_i = direction[0]
            y_i = direction[1]
        if not np.array_equal(direction, np.array([0, 0])):
            
            update_frequency, dist = dynamic_time_interval(x_r, y_r)
            
            if dist > 14:
                incr_i = incr
            elif dist > 6:
                incr_i = min(2, incr)
            else:
                incr_i = 1

            x = -1*incr_i if x_r < -1 else incr_i if x_r > 1 else 0
            y = -1*incr_i if y_r < -1 else incr_i if y_r > 1 else 0


            # print(f"dist {dist}, incr_i {incr_i}")
            x_r -= x
            y_r -= y
            if dist > 1.5:
                move_mouse(x, y)

            time.sleep(update_frequency)
        else:
            time.sleep(init_freq)
            
"""
# Main loop function
def move_mouse_loop():
    global direction
    x_i = direction[0]
    y_i = direction[1]
    x_r = direction[0]
    y_r = direction[1]
    while True:
        if not (x_i == direction[0] and y_i == direction[1]):
            x_r = direction[0]
            y_r = direction[1]
            x_i = direction[0]
            y_i = direction[1]
        if not np.array_equal(direction, np.array([0, 0])) and ((x_r > 1 or x_r < -1) and (y_r > 1 or y_r < -1)):
            x= direction[0]
            y= direction[1]
            x_r -= x
            y_r -= y
            move_mouse(x,y)

        time.sleep(update_frequency)

def move_mouse_loop1():
    global direction
    x_i = direction[0]
    y_i = direction[1]
    x_r = direction[0]
    y_r = direction[1]
    while True:
        # print(".")
        if not (x_i == direction[0] and y_i == direction[1]):
            # print("change")
            x_r = direction[0]
            y_r = direction[1]
            x_i = direction[0]
            y_i = direction[1]
        if (not np.array_equal(direction, np.array([0, 0]))) and ((x_r > 1 or x_r < -1) and (y_r > 1 or y_r < -1)):
            x= direction[0]*move_speed
            y= direction[1]*move_speed
            if abs(x) >= abs (x_r):
                x = x_r
            if abs(y) >= abs (y_r):
                y = y_r
            
            print(f"x {x}, y {y}, x_r {x_r}, y_r {y_r}")
            x_r -= x
            y_r -= y
            move_mouse(x,y)

        time.sleep(update_frequency)
        
def move_mouse_loop2():
    global direction, move_speed, update_frequency
    x_i, y_i = direction

    while True:
        x_r, y_r = direction

        if x_i != x_r or y_i != y_r:
            x_i, y_i = x_r, y_r

        if not np.array_equal(direction, np.array([0, 0])):
            distance = np.linalg.norm([x_r, y_r])
            if distance > move_speed:
                ratio = move_speed / distance
                x = x_r * ratio
                y = y_r * ratio
            else:
                x, y = x_r, y_r

            print(f"x {x}, y {y}, x_r {x_r}, y_r {y_r}, dist {distance}")
            direction[0] -= x
            direction[1] -= y
            move_mouse(x, y)

        time.sleep(update_frequency)
        
        
def move_mouse_loop3():
    global direction
    x_i = direction[0]
    y_i = direction[1]
    x_r = direction[0]
    y_r = direction[1]
    while True:
        # print(".")
        if not (x_i == direction[0] and y_i == direction[1]):
            # print("change")
            x_r = direction[0]
            y_r = direction[1]
            x_i = direction[0]
            y_i = direction[1]
        if (not np.array_equal(direction, np.array([0, 0]))) and ((x_r > 1 or x_r < -1) or (y_r > 1 or y_r < -1)):
            start = timer()
            x = speed_m * np.arcsinh(x_r * speed_i_m) + speed_a * x_r
            y = speed_m * np.arcsinh(y_r * speed_i_m) + speed_a * y_r
            end = timer()
            if abs(x) >= abs (x_r):
                x = x_r
            if abs(y) >= abs (y_r):
                y = y_r
            
            print(f"x {x}, y {y}, x_r {x_r}, y_r {y_r}, time {end - start}")
            x_r -= x
            y_r -= y
            move_mouse(x,y)

        time.sleep(update_frequency)
"""