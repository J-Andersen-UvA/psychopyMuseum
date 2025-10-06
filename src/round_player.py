from psychopy import visual, core, event
import helpers.csvManager as csvManager
from psychopy.hardware import keyboard
from psychopy.hardware import mouse as mouse
import os
import csv
from random import shuffle
import helpers.imageShower as imageShower
import setup.general_setup as gs
import setup.round_setup as rs

import asyncio
import threading
import buttonwebsite.buttonServer as bs
from LiveLinkFace import LiveLinkFaceServer
from helpers import screenNameShower as screenName

setup = gs.ExperimentSetup()
# from sound_player import SoundPlayer
# sound_player = SoundPlayer(python_path=setup.python_path)
import helpers.popUp as popUp
popUp = popUp.PopUp()
# Initialize keyboard
kb = keyboard.Keyboard()
role_switched = False
buttonInfo = bs.ButtonApp()
flask_thread = threading.Thread(
    target=buttonInfo.run,
    kwargs={"host": "0.0.0.0", "port": 5000, "debug": False},
    daemon=True
)
flask_thread.start()


### Functions ###

def ShowTargetImage(trial, round_setup):
    winA.flip(clearBuffer=True)
    # load img1 as the background
    imageShower.show_image(round_setup.img1_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
    # load and display one image
    target_stim = trial['target_image']  
    img_name = trial[target_stim]  # This will get the image file name from the corresponding column (stim1, stim2, etc.)
    target_img_path = os.path.join(round_setup.img_folder, img_name)
    imageShower.show_image(target_img_path, winA, pos=(1,23), size=(485,485), flip=False)
    screenName.show_screen_name(winA, "A", flip=False)

# def waitOrButtons(wait_time=600, buttons=["return"]):
#     """
#     Waits for a certain time (in seconds) or until a button (enter) is pressed
#     """
#     buttonTime = core.Clock()

#     print(f"Press {buttons} to continue or wait for {wait_time} seconds")
#     while buttonTime.getTime() < wait_time:  # 10 minutes (600s)
#         keys = kb.getKeys()  # Check for keypresses
#         for button in buttons:
#             if button in keys:  # return = enter
#                 print(f"Button pressed {button}")
#                 return button
#         core.wait(0.01)
#     print("Time is up")

def waitOrButtons(wait_time=600, buttons=["return"], reset_button_server=True):
    buttonTime = core.Clock()

    if reset_button_server:
        buttonInfo.last_pressed = None

    print(f"Press {buttons} to continue or wait for {wait_time} seconds")

    while buttonTime.getTime() < wait_time:
        if buttonInfo.last_pressed != None and buttonInfo.last_pressed in buttons:
            print(f"Button pressed {buttonInfo.last_pressed}, resetting buttonInfo")
            button = buttonInfo.last_pressed
            buttonInfo.last_pressed = None
            
            timestamp = button_timer.getTime()
            button_writer.writerow([timestamp, button])
            button_press_log.flush()

            return button
        else:
            for button in buttons:
                if button in keys:
                    print(f"Button pressed {button}")
                    return button
        # --- Keyboard keys ---
        keys = kb.getKeys()
        for key in keys:
            if key.name in buttons:
                print(f"Button pressed {key.name}")

                # log press
                timestamp = button_timer.getTime()
                button_writer.writerow([timestamp, key.name])
                button_press_log.flush()

                return key.name
        core.wait(0.01)
    print("WaitOrButton time is up.")


# create windows
winA = visual.Window(
    setup.window_size, 
    color=setup.window_color, 
    units=setup.window_units, 
    fullscr=setup.fullscreen,
    screen=setup.screenA)

winB = visual.Window(
    setup.window_size, 
    color=setup.window_color, 
    units=setup.window_units, 
    fullscr=setup.fullscreen,
    screen=setup.screenB)

def roleSwitch(round_setup, max, cur):
    global role_switched
    global main_timer
    global winA
    global winB
    if (main_timer.getTime() > 300 and round_setup.role_switch and not role_switched) or (max/2 <= cur and not role_switched and round_setup.role_switch):     # Check if it's time to end round
        print("Dit is het einde van deze ronde")
        role_switched = True  # Ensure roles are only switched once
        visual.TextStim(winA, text=round_setup.switch, color="white", height=40).draw()
        screenName.show_screen_name(winA, "A", flip=False)
        winA.flip()
        visual.TextStim(winB, text=round_setup.switch, color="white", height=40).draw()
        screenName.show_screen_name(winB, "B", flip=False)
        winB.flip()
        winA, winB = winB, winA
        waitOrButtons()

# Add dyad number
dyad_nr_text = "Dyad: "
dyad_number = ""

# display text
screenName.show_screen_name(winA, "A", flip=False)
dyad_nr_stim_a = visual.TextStim(winA, text=dyad_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)

screenName.show_screen_name(winB, "B", flip=False)
dyad_nr_stim_b = visual.TextStim(winB, text=dyad_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)

# Wait for type the dyad number 
while True:
    dyad_nr_stim_a.text = dyad_nr_text + dyad_number
    dyad_nr_stim_a.draw()
    dyad_nr_stim_b.text = dyad_nr_text + dyad_number
    dyad_nr_stim_b.draw()
    screenName.show_screen_name(winA, "A", flip=False)
    screenName.show_screen_name(winB, "B", flip=False)
    winA.flip()
    winB.flip()

    keys = kb.getKeys()
    for key in keys:
        if key.name == 'return' and dyad_number != "":  # Press 'Enter' to submit the input
            break
        elif key.name == 'backspace':  # Handle backspace to delete characters
            dyad_number = dyad_number[:-1]
        elif len(key.name) == 1:  # Add characters to dyad number
            dyad_number += key.name

    if 'return' in [key.name for key in keys]:
        break
    core.wait(0.01)

# Add round number
round_nr_text = "Round: "
round_number = ""

#display text
round_nr_stim_a = visual.TextStim(winA, text=round_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)
screenName.show_screen_name(winA, "A", flip=False)

round_nr_stim_b = visual.TextStim(winB, text=round_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)
screenName.show_screen_name(winB, "B", flip=False)


# Wait for type the round number 
while True:
    round_nr_stim_a.text = round_nr_text + round_number
    round_nr_stim_a.draw()
    round_nr_stim_b.text = round_nr_text + round_number
    round_nr_stim_b.draw()
    screenName.show_screen_name(winA, "A", flip=False)
    screenName.show_screen_name(winB, "B", flip=False)
    winA.flip()
    winB.flip()

    keys = kb.getKeys()
    for key in keys:
        if key.name == 'return' and round_number != "":  # Press 'Enter' to submit the input
            break
        elif key.name == 'backspace':  # Handle backspace to delete characters
            round_number = round_number[:-1]
        elif len(key.name) == 1:  # Add characters to dyad number
            round_number += key.name

    if 'return' in [key.name for key in keys]:
        break
    core.wait(0.01)

# start a timer for the button press timestamps
button_timer = core.Clock()


# create output file for trial results  
output_file = os.path.join(setup.output_folder, f"hh_dyad_{dyad_number}_round_{round_number}") # change to nh later, there is surely a smoother way but that's it for now
# Check if the file already exists
if os.path.exists(output_file + ".csv"):
    popUp.show_warning_then_exit(
        "Warning", f"The file '{output_file}.csv' already exists. Quiting the program..."
    )


# define column headers
headers = ["round_number", "dyad_number", "trial_number", "target_img", "selected_img","accuracy", "reaction_time", "noise_type"]
os.makedirs(setup.output_folder, exist_ok=True)
trial_writer = csvManager.CSVWriter(output_file + ".csv", headers)

# create output file with button press timestamps
button_timing_path = output_file + "_button_presses.csv"
# check if it already exists
if os.path.exists(button_timing_path):
    popUp.show_warning_then_exit(
        "Warning", f"The file '{button_timing_path}' already exists. Quitting the program..."
    )

# create and open csv file
button_press_log = open(button_timing_path, "w", newline="")
button_writer = csv.writer(button_press_log)
button_writer.writerow(["timestamp", "button"])  # Write header

# Add social or nonsocial noise
noise_text = "Noise: "
selected_noise = ""

#display noise text
noise_stim_a = visual.TextStim(winA, text=noise_text, 
                             color="#F5F5DC", 
                             colorSpace='hex', 
                             height=40, pos=(0, 0), 
                             wrapWidth=450)
screenName.show_screen_name(winA, "A", flip=False)

noise_stim_b = visual.TextStim(winB, text=noise_text, 
                             color="#F5F5DC", 
                             colorSpace='hex', 
                             height=40, pos=(0, 0), 
                             wrapWidth=450)
screenName.show_screen_name(winB, "B", flip=False)

noise = None

while True:
    noise_stim_a.text = noise_text + selected_noise
    noise_stim_a.draw()
    noise_stim_b.text = noise_text + selected_noise
    noise_stim_b.draw()
    screenName.show_screen_name(winA, "A", flip=False)
    screenName.show_screen_name(winB, "B", flip=False)
    winA.flip()
    winB.flip()

    # select noise dependent on input
    keys = kb.getKeys()

    for key in keys:
        if key.name == 's':
            selected_noise = 'soc'
        elif key.name == 'n':
            selected_noise = 'nonsoc'
        elif key.name == 'x':
            selected_noise = 'silence'
    if 's' in [key.name for key in keys] or 'n' in [key.name for key in keys] or 'x' in [key.name for key in keys]:
        break
    core.wait(0.01)

def play_noise():
    if not setup.audio_player.isPlaying():
        if selected_noise == 'soc':
            setup.audio_player.play(setup.noise_soc, setup.noise_soc_volume)
            # sound_player.play(setup.noise_soc)
        elif selected_noise == 'nonsoc':
            setup.audio_player.play(setup.noise_nonsoc, setup.noise_nonsoc_volume)
            # sound_player.play(setup.noise_nonsoc)
        elif selected_noise == 'silence':
            return
    else:
        setup.audio_player.play()
    return

# create intro text for rounds 
visual.TextStim(winA, text="Ronde " + str(round_number), color="#F5F5DC", height=40, pos=(0, 0), wrapWidth=450).draw()
screenName.show_screen_name(winA, "A", flip=False)
visual.TextStim(winB, text="Ronde " + str(round_number), color="white", height=50).draw()
screenName.show_screen_name(winB, "B", flip=False)

winA.flip()
winB.flip()
waitOrButtons(5)

# Load in the round config
round_setup = rs.RoundSetup(round_number)

iphone_ips = ["192.168.1.2", "192.168.1.3"]  # Replace with actual IPs
llf_args = {
    'llf_port': 12345,
    'receive_csv_port': 23456,
    'receive_video_port': 34567,
    'llf_save_path_csv': "./csv",
    'llf_save_path_video': "./video",
    'endpoint': "https://signcollect.nl/razerUpload/upload.php"
}
gloss = "trial"

llf_server = LiveLinkFaceServer(gloss, llf_args, iphone_ips)


# create instruction text 
visual.TextStim(winA,text=round_setup.instr, height=30).draw()
screenName.show_screen_name(winA, "A", flip=False)
visual.TextStim(winB,text=round_setup.instr, height=30).draw()
screenName.show_screen_name(winB, "B", flip=False)
winA.flip()
winB.flip()
waitOrButtons(wait_time=60, buttons=list(setup.allowed_keys.keys()))

# Start a timer
main_timer = core.Clock()

# play prompts (only for for round 1)
if round_setup.prompts:
    round1_timer = core.Clock()
    if not setup.no_obs:
        setup.obs.send_name_obs("dyad_" + dyad_number + "_round_" + round_number)
        setup.obs.send_start_record_obs()
        # asyncio.run(setup.obs.send_start_record_obs())
    for prompt in round_setup.prompts:
        play_noise()
        visual.TextStim(winA, text=prompt, color="white", height=40).draw()
        screenName.show_screen_name(winA, "A", flip=False)
        visual.TextStim(winB, text=prompt, color="white", height=40).draw()
        screenName.show_screen_name(winB, "B", flip=False)
        winA.flip()
        winB.flip()
        waitOrButtons(2)
        waitOrButtons(wait_time=600-round1_timer.getTime(), buttons=list(setup.allowed_keys.keys())) # 10 minutes or button
        setup.audio_player.pause()
        if round1_timer.getTime() >= 600:
            break
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        # asyncio.run(setup.obs.send_stop_record_obs())
        # asyncio.run(setup.obs.send_request_file_obs())
    
    

#  # load background image
# result1 = imageShower.show_image(round_setup.img4_background, winA, size=(700, 700))
# result2 = imageShower.show_image(round_setup.img4_background, winB, size=(700, 700))
# if result1 and result2:
#     waitOrButtons(wait_time=600, buttons=list(setup.allowed_keys.keys()))

# # zoom in background image
# result1 = imageShower.show_image(round_setup.img4_background, winA, pos=(0,-70), size=(1100, 1100))
# result2 = imageShower.show_image(round_setup.img4_background, winB, pos=(0,-70), size=(1100, 1100))
# if result1 and result2:
#     waitOrButtons(wait_time=600, buttons=list(setup.allowed_keys.keys()))

 # Create a response clock
rt_clock = core.Clock()

# Iterate through each trial in the Excel sheet
async def go_trial():
    trial_timer = core.Clock()

    print("Playing trials")

    # Start LLF recording for the round
    for client in llf_server.clients.values():
        client.start_capture()
   
    if not setup.no_obs:
        setup.obs.send_name_obs("dyad_" + dyad_number + "_round_" + round_number)
        setup.obs.send_start_record_obs()
        # await setup.obs.send_name_obs("dyad_" + dyad_number + "_round_" + round_number)
        # await setup.obs.send_start_record_obs()

    amount_of_rounds = len(round_setup.stims)

    for trial_number, trial in enumerate(round_setup.stims):
        # Play the background noise
        play_noise()

        # load text background image
        imageShower.show_image(round_setup.text_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
        imageShower.show_image(round_setup.text_background, winB, pos=(0,-50), size=(1000, 1000), flip=False)
        screenName.show_screen_name(winA, "A", flip=False)
        screenName.show_screen_name(winB, "B", flip=False)

        # Display the description text
        if 'description_text' in trial:
            desc_text = trial['description_text']  
            visual.TextStim(winA, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450).draw()
            visual.TextStim(winB, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450).draw()
            winA.flip()
            winB.flip()
            # Don't accept multiple key presses
            waitOrButtons(wait_time=1, buttons=[""])
            waitOrButtons(wait_time=40, buttons=list(setup.allowed_keys.keys()))

        print("[Trial] Clearing screen...")
        winA.flip(clearBuffer=True)
        winB.flip(clearBuffer=True)

        print("[Trial] Loading background...")
        # Load img4 as the background
        if not round_setup.show_target:
            imageShower.show_image(round_setup.img4_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
            screenName.show_screen_name(winA, "A", flip=False)
        imageShower.show_image(round_setup.img4_background, winB, pos=(0,-50), size=(1000, 1000), flip=False)
        screenName.show_screen_name(winB, "B", flip=False)

        print("[Trial] Loading stim images...")
        # Load and display the 4 images
        images = [trial['stim1'], trial['stim2'], trial['stim3'], trial['stim4']]
        positions = [(-138, 184), (141, 184), (-138, -107), (141, -107)]  
        size = (238, 238) 

        print("[Trial] Shuffling images...")
        # Shuffle positions to counterbalance
        shuffle(images)

        # get path of images
        path_images = [os.path.join(round_setup.img_folder, image) for image in images]

        print("[Trial] Showing multiple images...")
        # show shuffled images
        if not round_setup.show_target:
            imageShower.show_multiple_images(path_images, winA, positions, size, show_tags=True, flip=False)
            screenName.show_screen_name(winA, "A", flip=False)
        imageShower.show_multiple_images(path_images, winB, positions, size, show_tags=True, flip=False)
        screenName.show_screen_name(winB, "B", flip=False)

        if round_setup.show_target:
            print("[Trial] Showing target image...")
            ShowTargetImage(trial, round_setup)

        print("[Trial] Flip wins...")
        winA.flip(clearBuffer=False)
        winB.flip(clearBuffer=False)

        # Reset clock
        rt_clock.reset()

        # Don't accept multiple key presses
        # kb.clearEvents()
        # core.wait(0.1)
        # kb.clearEvents()

        # Wait for a valid button press to continue
        print("[Trial] Awaiting answer...")
        button_pressed = waitOrButtons(wait_time=6000, buttons=list(setup.allowed_keys.keys()))
        rt = rt_clock.getTime()

        # Stop the noise after the trial is done
        print("[Trial] Pausing noise...")
        setup.audio_player.pause()
        # sound_player.stop()

        # Write test data
        selected_image = images[setup.allowed_keys[button_pressed]]
        print(f"[Trial] Writing data to file:\tcorrect:{trial[trial['target_image']]==selected_image}\ttrialtarget_image:{trial[trial['target_image']]}\tselected_image:{selected_image}")
        trial_writer.write_row([("round_number", round_number), ("dyad_number",dyad_number), ("trial_number", trial_number), ("target_img", trial[trial['target_image']]), ("selected_img", selected_image), ("accuracy", trial[trial['target_image']]==selected_image), ("reaction_time", rt), ("noise_type", selected_noise)])

        roleSwitch(round_setup, amount_of_rounds, trial_number)
        if trial_timer.getTime() >= 600:
            print("Time is up, ending the round")
            break
    
    # End LLF recording for the round
    for client in llf_server.clients.values():
        client.stop_capture()

    # End the round
    setup.audio_player.stop()
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        # await setup.obs.send_stop_record_obs()
        # await setup.obs.send_request_file_obs()


# Iterate through each trial in the Excel sheet
try:
    if round_setup.play_trial:
        asyncio.run(go_trial())
    else:
        print("No trials to play")
except Exception as e:
    print(f"Exception: {e}")
    setup.audio_player.stop()
    # sound_player.stop()
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        # asyncio.run(setup.obs.send_stop_record_obs())
        # asyncio.run(setup.obs.send_request_file_obs())
except KeyboardInterrupt:
    setup.audio_player.stop()
    # sound_player.stop()
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        # asyncio.run(setup.obs.send_stop_record_obs())
        # asyncio.run(setup.obs.send_request_file_obs())

# Close windows
winA.close()
winB.close()

# close button press log
button_press_log.close()
trial_writer.close()

# Exit experiment
core.quit()