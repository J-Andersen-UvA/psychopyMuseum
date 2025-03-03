from psychopy import visual, core, event, sound, data
import csvManager
from psychopy.hardware import mouse, keyboard
import os, random
from random import shuffle
import src.imageShower as imageShower
import yaml
import general_setup as gs
import round_setup as rs
setup = gs.ExperimentSetup()

def waitOrButton(wait_time=600, button="return"):
    """
    Waits for a certain time (in seconds) or until a button (enter) is pressed
    """
    waiting = True
    while waiting:
        keys = kb.getKeys(waitRelease=False, clear=True)
        for key in keys:
            if key.name in setup.allowed_keys:
                waiting = False  
                break

    while timer.getTime() < wait_time:  # 10 minutes (600s)
        keys = event.getKeys()  # Check for keypresses
        if button in keys:  # return = enter
            break 



# create windows
winA = visual.Window(
    setup.window_size, 
    color=setup.window_color, 
    units=setup.window_units, 
    fulscr=setup.fullscreen,
    monitor=setup.screenA)

winB = visual.Window(
    setup.window_size, 
    color=setup.window_color, 
    units=setup.window_units, 
    fullscr=setup.fullscreen,
    monitor=setup.screenB)

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

#display text
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

    keys = kb.getKeys()
    for key in keys:
        if key.name == 's':
            noise = sound.Sound(setup.noise_soc, stereo=True, sampleRate=44100)
            selected_noise = 'soc'
        elif key.name == 'n':
            noise = sound.Sound(setup.noise_nonsoc, stereo=True, sampleRate=44100)
            selected_noise = 'nonsoc'
    if 's' in [key.name for key in keys] or 'n' in [key.name for key in keys]:
        break
    core.wait(0.01)

noise.play()

# create intro text for rounds 
intro = visual.TextStim(winA, text="Ronde " + str(round_number), color="white", height=50)
intro = visual.TextStim(winB, text="Ronde " + str(round_number), color="white", height=50)

# Load in the round config
round_setup = rs.RoundSetup(round_number)

# create instruction text 
visual.TextStim(winA,text=round_setup.instr)

# Start a timer
timer = core.Clock()

# play prompts for round 1
for prompt in round_setup.prompts:
    visual.TextStim(winA, text=prompt, color="white", height=40).draw
    visual.TextStim(winB, text=prompt, color="white", height=40).draw
    waitOrButton()
    winA.flip()  
    winB.flip()  

# load images
if round_setup.intro_image:

    background_img = visual.ImageStim(winA, image=setup.img_4pics, pos=(0,-50), size=(1000, 1000))
    background_img = visual.ImageStim(winB, image=setup.img_4pics, pos=(0,-50), size=(1000, 1000))


 # background image
imageShower.show_image(setup.img_4pics, winA, size=(700, 700))
# zoom in intro image
imageShower.show_image(setup.img_4pics, winA, pos=(0,-70), size=(1100, 1100))


# Counterbalance trial order by shuffling
stim_file_data = data.importConditions(stim_file)
random.shuffle(stim_file_data)


# Iterate through each trial in the Excel sheet
for trial_number, trial in enumerate(stim_file_data, start=1):

    # Play the sound
    noise_to_play.play(loops=-1)  # Infinite loop for continuous playback

    # Display the description text
    # imageShower.show_image(img_text, win, size=(1000, 1000), pos=(0,-50), frame=False)
    image = visual.ImageStim(win, image=img_text, pos=(0,-50), size=(1000, 1000))
    desc_text = trial['description_text']  # Assuming a 'Description' column in the Excel file
    desc_stim = visual.TextStim(win, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450)
    
    image.draw()
    desc_stim.draw()
    win.flip()

    # Start a timer
    timer = core.Clock()

    while timer.getTime() < 5:
        core.wait(0.01)

    # Load img4 as the background
    # imageShower.show_image(setup.img_4pics, win, pos=(0,-50), size=(1000, 1000))
    background = visual.ImageStim(win, image=setup.img_4pics, pos=(0,-50), size=(1000, 1000))
    background.draw()
    
    # Load and display the 4 images
    images = [trial['stim1'], trial['stim2'], trial['stim3'], trial['stim4']]
    positions = [(-123, 146), (125, 146), (-123, -104), (125, -104)]
    size = (212, 212)

  # Shuffle positions to counterbalance
    shuffle(images)

  # get path of images
    path_images = [os.path.join(setup.img_folder, image) for image in images]

  # Create a response clock
    rt_clock = core.Clock()

  # show shuffled images
    imageShower.show_multiple_images(path_images, win, positions, size=size, wait_time=0, show_tags=True)

  # Refresh screen to show images and numbers
    win.flip()

  # Reset the clock right before starting to wait for a response
    rt_clock.reset()

    # Wait for a valid button press to continue
    button_pressed = ''
    while button_pressed not in button_mapping:
        keys = kb.getKeys()
        for key in keys:
            if key.name in button_mapping:
                button_pressed = key.name
                rt = key.rt
                button_data.append([dyad_number, trial_number, trial, button_pressed, rt])
                break
        core.wait(0.01)  # Add a small delay
        
    # Stop the sound after the trial is done
    #noise_to_play.stop()

    # Writing test data
    selected_image = images[button_mapping[button_pressed-1]]
    csv_writer.write_row([("dyad_number",dyad_number), ("trial_number", trial_number), ("target_img", trial['stim1']), ("selected_img", selected_image), ("accuracy", trial['stim1']==selected_image), ("reaction_time", rt)])
