import detection_view_bot as det
import mouseController2 as mc
import threading
import numpy as np
import math
import time
import os
import keyboard

aim_toggle = True
aim_toggle_key = "v"
conf_limit = 0.79
freq_min = 0.001
freq_i_min = 0.01
dist_divider = 100
update_frequency = 0.0001
init_freq = 0.0001
incr = 1
is_quit = False
team_ident = ""
isFFA = True

def calc_dist(x,y):
    return math.sqrt(math.pow(x,2)+math.pow(y,2))



def bot_loop():
    global team_ident, isFFA, aim_toggle
    while True:
        if aim_toggle:
            heads = []
            bodies = []
            for i in det.fov_elements:
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


# thr = threading.Thread(target=mouseController.simple_move_mouse_loop, daemon=True)
"""thr = threading.Thread(target=mc.move_mouse_loop4, daemon=True)
thr.start()

thr2 = threading.Thread(target=det.main, daemon=True)
thr2.start()

thr3 = threading.Thread(target=bot_loop, daemon=True)
thr3.start()"""

logo = """    _   __        __                      _  ____   ____  ______
   / | / /__  __ / /_   ___  ____ ____   (_)/ __ ) / __ \/_  __/
  /  |/ // / / // __ \ / _ \/_  //_  /  / // __  |/ / / / / /   
 / /|  // /_/ // /_/ //  __/ / /_ / /_ / // /_/ // /_/ / / /    
/_/ |_/ \__,_//_.___/ \___/ /___//___//_//_____/ \____/ /_/     
                                                                """
                                                                
help = """ 
VAC-proofness is not guaranteed!

Use these inputs to control the bot:
"C" to toggle CT-side
"T" to toggle T-side
"A" to toggle deathmatch / ffa
"1" mild assist
"2" same as 1, but more aggresive
"3" like 1, but with adjsted gain settings
"4" 3 with less gain
"M" to manually change parameters (not yet implemented)
"Q" to quit
"""

def clear_and_print(input):
    initial = logo + help
    os.system('cls')
    print(f"{initial}\n{input}")
    
def quit_and_print():
    quitting = """
    Thanks for using NubezziBOT!
    """
    initial = logo + quitting
    os.system('cls')
    print(initial)
    
def handle_team_change(ident):
    global isFFA, team_ident
    if ident == "":
        isFFA = True
    else:
        isFFA = False
    team_ident = ident
    
def change_T():
    handle_team_change("CT")
    clear_and_print("Team changed to T's. Targeting only CT's")
    
def change_CT():
    handle_team_change("T")
    clear_and_print("Team changed to CT's. Targeting only T's")
    
def change_FFA():
    handle_team_change("")
    clear_and_print("Team changed to FFA")

def toggle_vision():
    det.showVision = not det.showVision
    clear_and_print("Toggled vision")
    
def toggle_aim():
    global aim_toggle
    aim_toggle = not aim_toggle
    if aim_toggle:
        clear_and_print("aimbot toggled on")
    else:
        clear_and_print("aimbot toggled off")
        
def toggle_snap_aim():
    mc.snapturn = not mc.snapturn
    clear_and_print("Toggled vision")

if __name__ == "__main__":
    det.conf_limit = conf_limit
    mc.direction = np.array([0, 0])
    mc.dist_divider = dist_divider
    mc.freq_i_min = freq_i_min
    mc.freq_min = freq_min
    mc.init_freq = init_freq
    mc.incr = incr
    mc.update_frequency = update_frequency
    keyboard.on_press_key("left", lambda _:change_CT())
    keyboard.on_press_key("right", lambda _:change_T())
    keyboard.on_press_key("down", lambda _:toggle_vision())
    keyboard.on_press_key("up", lambda _:change_FFA())
    keyboard.on_press_key(aim_toggle_key, lambda _:toggle_aim())
    keyboard.on_press_key('pgdown', lambda _:toggle_snap_aim())
    thr = threading.Thread(target=mc.move_mouse_loop4, daemon=True)
    thr.start()
    thr2 = threading.Thread(target=det.main, daemon=True)
    thr2.start()
    thr3 = threading.Thread(target=bot_loop, daemon=True)
    thr3.start()
    clear_and_print("")                                                                                    
    while not is_quit:
        # clear_and_print("")
        inp = input("")
        try:
            match str(inp).lower():
                case "c": 
                    handle_team_change("T")
                    clear_and_print("Team changed to CT's. Targeting only terrorists")
                case "t": 
                    handle_team_change("CT")
                    clear_and_print("Team changed to T's. Targeting only CT's")
                case "a": 
                    handle_team_change("")
                    clear_and_print("Targeting all players")
                case "1": 
                    mc.dist_divider = 100
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.001
                    mc.incr = 1
                    clear_and_print("Preset 1 activated")
                case "2": 
                    mc.dist_divider = 100
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.001
                    mc.incr = 2
                    clear_and_print("Preset 2 activated")
                case "3": 
                    mc.dist_divider = 4000
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.003
                    mc.incr = 1
                    clear_and_print("Preset 3 activated")
                case "4": 
                    mc.dist_divider = 2000
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.005
                    mc.incr = 2
                    clear_and_print("Preset 4 activated")
                case "5": 
                    mc.dist_divider = 4000
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.003
                    mc.incr = 3
                    clear_and_print("Preset 4 activated")
                case "6": 
                    mc.dist_divider = 100
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.001
                    mc.incr = 4
                    clear_and_print("Preset 4 activated")
                case "7": 
                    mc.dist_divider = 2000
                    mc.freq_i_min = 0.01
                    mc.freq_min = 0.005
                    mc.incr = 6
                    clear_and_print("Preset 4 activated")
                case "q": 
                    is_quit = True
                    quit_and_print()
                    
                case _: clear_and_print("Please input something! empty input not processed")
        except Exception as e:
            print(f"ran into error: {e}")
            is_quit = True