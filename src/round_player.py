from psychopy import visual, core, event
import csvManager
from psychopy.hardware import keyboard
from psychopy.hardware import mouse as mouse
import os
from random import shuffle
import imageShower as imageShower
import general_setup as gs
import round_setup as rs
setup = gs.ExperimentSetup()
from sound_player import SoundPlayer
sound_player = SoundPlayer(python_path=setup.python_path)
# Initialize keyboard
kb = keyboard.Keyboard()
role_switched = False

def roleSwitch(enable):
    if main_timer.getTime() > 30 and enable and not role_switched:     # Check if it's time to switch roles 
        print("Switching roles")
        role_switched = True  # Ensure roles are only switched once
        visual.TextStim(winA, text=round_setup.switch, color="white", height=30).draw()
        visual.TextStim(winB, text=round_setup.switch, color="white", height=30).draw()
        winA.flip()
        winB.flip()
        core.wait(5) # wait for 5s
        winA, winB = winB, winA  # Swap the windows

def waitOrButton(wait_time=600, button="return"):
    """
    Waits for a certain time (in seconds) or until a button (enter) is pressed
    """
    buttonTime = core.Clock()

    print(f"Press {button} to continue or wait for {wait_time} seconds")
    while buttonTime.getTime() < wait_time:  # 10 minutes (600s)
        keys = kb.getKeys()  # Check for keypresses
        if button in keys:  # return = enter
            print("Button pressed")
            break 
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

# Add round number
round_nr_text = "Round number: "
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

# Add dyad number
dyad_nr_text = "Dyad number: "
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

# create output file for button presses 
output_file = os.path.join(setup.output_folder, dyad_number)
# define column headers
headers = ["round_number", "dyad_number", "trial_number","target_img" "selected_img","accuracy", "reaction_time"]
os.makedirs(setup.output_folder, exist_ok=True)
csv_writer = csvManager.CSVWriter(output_file + ".csv", headers)

# Add social or nonsocial noise
noise_text = "Noise type: "
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
    if selected_noise == 'soc':
        noise = sound_player.play(setup.noise_soc)
    elif selected_noise == 'nonsoc':
        noise = sound_player.play(setup.noise_nonsoc)
    return noise

# create intro text for rounds 
visual.TextStim(winA, text="Ronde " + str(round_number), color="#F5F5DC", height=40, pos=(0, 0), wrapWidth=450).draw()
visual.TextStim(winB, text="Ronde " + str(round_number), color="white", height=50).draw()
winA.flip()
winB.flip()
waitOrButton()

# Load in the round config
round_setup = rs.RoundSetup(round_number)

# create instruction text 
visual.TextStim(winA,text=round_setup.instr, height=35).draw()
visual.TextStim(winB,text=round_setup.instr, height=35).draw()
winA.flip()
winB.flip()
waitOrButton()

# Start a timer
main_timer = core.Clock()

# play prompts (only for for round 1)
if round_setup.prompts:
    for prompt in round_setup.prompts:
        visual.TextStim(winA, text=prompt, color="white", height=40).draw()
        visual.TextStim(winB, text=prompt, color="white", height=40).draw()
        winA.flip()  
        winB.flip()  
        waitOrButton()

 # load background image
imageShower.show_image(round_setup.img4_background, winA, size=(700, 700))
imageShower.show_image(round_setup.img4_background, winB, size=(700, 700))
waitOrButton()

# zoom in background image
imageShower.show_image(round_setup.img4_background, winA, pos=(0,-70), size=(1100, 1100))
imageShower.show_image(round_setup.img4_background, winB, pos=(0,-70), size=(1100, 1100))
waitOrButton()

 # Create a response clock
rt_clock = core.Clock()

# Iterate through each trial in the Excel sheet
def go_trial():
    if not setup.no_obs:
        setup.obs.send_name_obs(setup.output_folder, "dyad_" + dyad_number + "_round_" + round_number)
        setup.obs.send_start_record_obs()

    for trial_number, trial in enumerate(round_setup.stims):

        # Play the background noise
        play_noise()

        # Display the description text
        desc_text = trial['description_text']  
        visual.TextStim(winA, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450).draw()
        visual.TextStim(winB, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450).draw()
        winA.flip()
        winB.flip()
        waitOrButton(5)

        # Load img4 as the background
        imageShower.show_image(round_setup.img4_background, winA, pos=(0,-50), size=(1000, 1000), flip=False)
        imageShower.show_image(round_setup.img4_background, winB, pos=(0,-50), size=(1000, 1000), flip=False)

        # Load and display the 4 images
        images = [trial['stim1'], trial['stim2'], trial['stim3'], trial['stim4']]
        positions = [(-123, 146), (125, 146), (-123, -104), (125, -104)]
        size = (212, 212)

        # Shuffle positions to counterbalance
        shuffle(images)

        # get path of images
        path_images = [os.path.join(round_setup.img_folder, image) for image in images]

        # show shuffled images
        imageShower.show_multiple_images(path_images, winA, positions, size, show_tags=True)
        imageShower.show_multiple_images(path_images, winB, positions, size, show_tags=True)

        # Reset clock
        rt_clock.reset()

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
        sound_player.stop()

        # Write test data
        selected_image = images[setup.allowed_keys[button_pressed]]
        csv_writer.write_row([("dyad_number",dyad_number), ("trial_number", trial_number), ("target_img", trial['stim1']), ("selected_img", selected_image), ("accuracy", trial['stim1']==selected_image), ("reaction_time", rt)])

        roleSwitch(round_setup.role_switch)
    
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        setup.obs.send_request_file_obs()

# Iterate through each trial in the Excel sheet
try:
    go_trial()
except Exception as e:
    print(e)
    sound_player.stop()
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        setup.obs.send_request_file_obs()
except KeyboardInterrupt:
    sound_player.stop()
    if not setup.no_obs:
        setup.obs.send_stop_record_obs()
        setup.obs.send_request_file_obs()

# Close windows
winA.close()
winB.close()

# Exit experiment
core.quit()