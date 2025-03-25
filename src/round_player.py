from psychopy import visual, core, event
import helpers.csvManager as csvManager
from psychopy.hardware import keyboard
from psychopy.hardware import mouse as mouse
import os
from random import shuffle
import helpers.imageShower as imageShower
import setup.general_setup as gs
import setup.round_setup as rs
import asyncio
setup = gs.ExperimentSetup()
# from sound_player import SoundPlayer
# sound_player = SoundPlayer(python_path=setup.python_path)
import helpers.popUp as popUp
popUp = popUp.PopUp()
# Initialize keyboard
kb = keyboard.Keyboard()
role_switched = False

def ShowTargetImage(trial, round_setup):
    # load img1 as the background
    imageShower.show_image(round_setup.img1_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
    # load and display one image
    target_stim = trial['target_image']  
    img_name = trial[target_stim]  # This will get the image file name from the corresponding column (stim1, stim2, etc.)
    target_img_path = os.path.join(round_setup.img_folder, img_name)
    imageShower.show_image(target_img_path, winA, pos=(1,23), size=(485,485), flip=False)

def waitOrButtons(wait_time=600, buttons=["return"]):
    """
    Waits for a certain time (in seconds) or until a button (enter) is pressed
    """
    buttonTime = core.Clock()

    print(f"Press {buttons} to continue or wait for {wait_time} seconds")
    while buttonTime.getTime() < wait_time:  # 10 minutes (600s)
        keys = kb.getKeys()  # Check for keypresses
        for button in buttons:
            if button in keys:  # return = enter
                print("Button pressed")
                return
    print("Time is up")


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

def roleSwitch(round_setup):
    global role_switched
    global winA
    global winB
    if main_timer.getTime() > 300 and round_setup.role_switch:     # Check if it's time to end round
        print("Dit is het einde van deze ronde")
        role_switched = True  # Ensure roles are only switched once
        visual.TextStim(winA, text=round_setup.switch, color="white", height=40).draw()
        winA.flip()
        visual.TextStim(winB, text=round_setup.switch, color="white", height=40).draw()
        winB.flip()
        waitOrButtons()

# Add dyad number
dyad_nr_text = "Dyad: "
dyad_number = ""

# display text
dyad_nr_stim = visual.TextStim(winA, text=dyad_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)

dyad_nr_stim = visual.TextStim(winB, text=dyad_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)

# Wait for type the dyad number 
while True:
    dyad_nr_stim.text = dyad_nr_text + dyad_number
    dyad_nr_stim.draw()
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
round_nr_stim = visual.TextStim(winA, text=round_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)

round_nr_stim = visual.TextStim(winB, text=round_nr_text, 
                               color="#F5F5DC", 
                               colorSpace='hex', 
                               height=40, pos=(0, 0), 
                               wrapWidth=450)


# Wait for type the round number 
while True:
    round_nr_stim.text = round_nr_text + round_number
    round_nr_stim.draw()
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

# create output file for button presses 
output_file = os.path.join(setup.output_folder, f"hh_dyad_{dyad_number}_round_{round_number}") # change to nh later, there is surely a smoother way but that's it for now
# Check if the file already exists
if os.path.exists(output_file + ".csv"):
    popUp.show_warning_then_exit(
        "Warning", f"The file '{output_file}.csv' already exists. Quiting the program..."
    )

# define column headers
headers = ["round_number", "dyad_number", "trial_number", "target_img", "selected_img","accuracy", "reaction_time", "noise_type"]
os.makedirs(setup.output_folder, exist_ok=True)
csv_writer = csvManager.CSVWriter(output_file + ".csv", headers)

# Add social or nonsocial noise
noise_text = "Noise: "
selected_noise = ""

#display noise text
noise_stim = visual.TextStim(winA, text=noise_text, 
                             color="#F5F5DC", 
                             colorSpace='hex', 
                             height=40, pos=(0, 0), 
                             wrapWidth=450)

noise_stim = visual.TextStim(winB, text=noise_text, 
                             color="#F5F5DC", 
                             colorSpace='hex', 
                             height=40, pos=(0, 0), 
                             wrapWidth=450)

noise = None

while True:
    noise_stim.text = noise_text + selected_noise
    noise_stim.draw()
    winA.flip()
    winB.flip()

    # select noise dependent on input
    keys = kb.getKeys()

    for key in keys:
        if key.name == 's':
            selected_noise = 'soc'
        elif key.name == 'n':
            selected_noise = 'nonsoc'
    if 's' in [key.name for key in keys] or 'n' in [key.name for key in keys]:
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
    else:
        setup.audio_player.play()
    return

# create intro text for rounds 
visual.TextStim(winA, text="Ronde " + str(round_number), color="#F5F5DC", height=40, pos=(0, 0), wrapWidth=450).draw()
visual.TextStim(winB, text="Ronde " + str(round_number), color="white", height=50).draw()
winA.flip()
winB.flip()
waitOrButtons(5)

# Load in the round config
round_setup = rs.RoundSetup(round_number)

# create instruction text 
visual.TextStim(winA,text=round_setup.instr, height=30).draw()
visual.TextStim(winB,text=round_setup.instr, height=30).draw()
winA.flip()
winB.flip()
waitOrButtons(wait_time=600, buttons=list(setup.allowed_keys.keys()))

# Start a timer
main_timer = core.Clock()

# play prompts (only for for round 1)
if round_setup.prompts:
    round1_timer = core.Clock()
    if not setup.no_obs:
        asyncio.run(setup.obs.send_start_record_obs())
    for prompt in round_setup.prompts:
        play_noise()
        visual.TextStim(winA, text=prompt, color="white", height=40).draw()
        visual.TextStim(winB, text=prompt, color="white", height=40).draw()
        winA.flip()  
        winB.flip()  
        waitOrButtons(2)
        waitOrButtons(wait_time=600-round1_timer.getTime(), buttons=list(setup.allowed_keys.keys())) # 10 minutes or button
        setup.audio_player.pause()
        if round1_timer.getTime() >= 600:
            break
    if not setup.no_obs:
        asyncio.run(setup.obs.send_stop_record_obs())
        asyncio.run(setup.obs.send_request_file_obs())
    
    

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
    if not setup.no_obs:
        await setup.obs.send_name_obs("dyad_" + dyad_number + "_round_" + round_number)
        await setup.obs.send_start_record_obs()

    for trial_number, trial in enumerate(round_setup.stims):
        # Play the background noise
        play_noise()

        # load text background image
        imageShower.show_image(round_setup.text_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
        imageShower.show_image(round_setup.text_background, winB, pos=(0,-50), size=(1000, 1000), flip=False)

        # Display the description text
        if 'description_text' in trial:
            desc_text = trial['description_text']  
            visual.TextStim(winA, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450).draw()
            visual.TextStim(winB, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450).draw()
            winA.flip()
            winB.flip()
            # Don't accept multiple key presses
            waitOrButtons(wait_time=1, buttons=[""])
            waitOrButtons(wait_time=600, buttons=list(setup.allowed_keys.keys()))

        # Load img4 as the background
        imageShower.show_image(round_setup.img4_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
        imageShower.show_image(round_setup.img4_background, winB, pos=(0,-50), size=(1000, 1000), flip=False)

        # Load and display the 4 images
        images = [trial['stim1'], trial['stim2'], trial['stim3'], trial['stim4']]
        positions = [(-138, 184), (141, 184), (-138, -107), (141, -107)]  
        size = (238, 238) 

        # Shuffle positions to counterbalance
        shuffle(images)

        # get path of images
        path_images = [os.path.join(round_setup.img_folder, image) for image in images]

        # show shuffled images
        imageShower.show_multiple_images(path_images, winA, positions, size, show_tags=True, flip=False)
        imageShower.show_multiple_images(path_images, winB, positions, size, show_tags=True, flip=False)

        if round_setup.show_target:
            ShowTargetImage(trial, round_setup)
        winA.flip()
        winB.flip()

        # Reset clock
        rt_clock.reset()

        # Don't accept multiple key presses
        waitOrButtons(wait_time=1, buttons=[""])

        # Wait for a valid button press to continue
        button_pressed = ''
        print(setup.allowed_keys.keys())
        while button_pressed not in setup.allowed_keys.keys():
            keys = kb.getKeys()
            for key in setup.allowed_keys.keys():
                if key in keys:
                    button_pressed = key
                    rt = rt_clock.getTime()
                    break
            core.wait(0.01)  # Add a small delay
            
        # Stop the noise after the trial is done
        setup.audio_player.pause()
        # sound_player.stop()

        # Write test data
        selected_image = images[setup.allowed_keys[button_pressed]]
        csv_writer.write_row([("round_number", round_number), ("dyad_number",dyad_number), ("trial_number", trial_number), ("target_img", trial['stim1']), ("selected_img", selected_image), ("accuracy", trial['stim1']==selected_image), ("reaction_time", rt), ("noise_type", selected_noise)])

        roleSwitch(round_setup)
        if trial_timer.getTime() >= 600:
            break
    
    # End the round
    setup.audio_player.stop()
    if not setup.no_obs:
        await setup.obs.send_stop_record_obs()
        await setup.obs.send_request_file_obs()

# Iterate through each trial in the Excel sheet
try:
    if round_setup.play_trial:
        asyncio.run(go_trial())
    else:
        print("No trials to play")
except Exception as e:
    print(e)
    setup.audio_player.stop()
    # sound_player.stop()
    if not setup.no_obs:
        asyncio.run(setup.obs.send_stop_record_obs())
        asyncio.run(setup.obs.send_request_file_obs())
except KeyboardInterrupt:
    setup.audio_player.stop()
    # sound_player.stop()
    if not setup.no_obs:
        asyncio.run(setup.obs.send_stop_record_obs())
        asyncio.run(setup.obs.send_request_file_obs())

# Close windows
winA.close()
winB.close()

# Exit experiment
core.quit()