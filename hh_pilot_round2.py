from psychopy import visual, core, event, sound, data
from psychopy.hardware import mouse, keyboard
import os, random
from random import shuffle
import src.imageShower as imageShower

from src.setup import ExperimentSetup
from src.csvManager import CSVWriter
setup = ExperimentSetup("config.yaml")
setup.validate_paths()

# create window
win = visual.Window(setup.window_size, color=setup.window_color, units=setup.window_units, fullscr=setup.fullscreen)

# set up keyboard for the button box
kb = keyboard.Keyboard()

# Define output file for button presses 
output_file = os.path.join(setup.output_folder, setup.output_file)
# Define column headers
headers = ["dyad_number", "trial_number","target_img" "selected_img","accuracy", "reaction_time"]
# Prepare to record button presses
os.makedirs("output", exist_ok=True)
csv_writer = CSVWriter("output/data.csv", headers)

button_data = []

# Add dyad number
dyad_nr_text = "Dyad number: "
dyad_nr_stim = visual.TextStim(win, text=dyad_nr_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 0), wrapWidth=450)

# Display prompt for dyad number input
dyad_nr_stim.draw()
win.flip()

# Wait for the researcher to type the dyad number 
dyad_number = ""
while True:
    keys = kb.getKeys(waitRelease=False, clear=True)
    for key in keys:
        if key.name == 'return' and dyad_number != "":  # Press 'Enter' to submit the input
            break
        elif key.name == 'backspace':  # Handle backspace to delete characters
            dyad_number = dyad_number[:-1]
        elif len(key.name) == 1:  # Add characters to dyad number
            dyad_number += key.name
    core.wait(0.01)

# load background noises
soc_noise = sound.Sound(setup.noise_soc_10)
nonsoc_noise = sound.Sound(setup.noise_nonsoc_10)

# Decide on social or nonsocial noise
noise_text = "Noise type: "
noise_stim = visual.TextStim(win, text=noise_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 0), wrapWidth=450)

# Show the prompt
noise_stim.draw()
win.flip()

# Wait for user input (pressing 's' for soc or 'n' for nonsoc)
selected_noise = None
while selected_noise not in ['s', 'n']:  # Wait for 's' or 'n' to be pressed
    keys = kb.getKeys(waitRelease=False, clear=True)
    for key in keys:
        if key.name == 's':
            selected_noise = 'soc'
        elif key.name == 'n':
            selected_noise = 'nonsoc'
    core.wait(0.01)

# Load the selected noise based on input
if selected_noise == 'soc':
    noise_to_play = soc_noise
elif selected_noise == 'nonsoc':
    noise_to_play = nonsoc_noise

# create and display intro text 
ronde2 = visual.TextStim(win, text="Ronde 2", color="white", height=50)
ronde2.draw()
win.flip()  # Update the window

kb.clearEvents()  # Clear keyboard buffer

# Start a timer
timer = core.Clock()

# Wait for 1 minute or until Enter is pressed
print("Waiting for 5 seconds")
while timer.getTime() < 5:  # 5s
    imageShower.update_window(win, ronde2)

    keys = kb.getKeys(waitRelease=False, clear=True)  # Check for keypresses
    if setup.key_2 in [key.name for key in keys]:  # return = enter
        break
    core.wait(0.01)  # Add a small delay

# create and display instructions
instr2 = visual.TextStim(win, text="In deze opdracht zien jullie korte beschrijvingen van abstracte schilderijen op het scherm. \n\nStel jullie voor dat jullie bij een museumbezoek zijn en de gids beschrijft een schilderij aan jullie. \n\nDaarna zien jullie vier verschillende schilderijen op het scherm. Het is jullie taak om samen te overleggen en te beslissen welk van de vier schilderijen de gids heeft beschreven. \n\nAls jullie dat hebben besloten, gebruiken jullie het knoppenvak om een schilderij te selecteren. Dan verschijnt de volgende beschrijving.", color="white", height=27, wrapWidth=600)
instr2.draw()
win.flip()  # Update the window

# Start a timer
timer = core.Clock()

# Wait for 1 minute or until Enter is pressed
print("Waiting for 60 seconds")
while timer.getTime() < 60:  # 60s
    imageShower.update_window(win, instr2)

    keys = kb.getKeys(waitRelease=False, clear=True)  # Check for keypresses
    if setup.key_2 in [key.name for key in keys]:  # return = enter
        break  
    core.wait(0.01)  # Add a small delay

# load and display intro image
imageShower.show_image(setup.img_4pics, win, size=(700, 700))

# zoom in intro image
imageShower.show_image(setup.img_4pics, win, pos=(0,-50), size=(1000, 1000))

# stimulus file
# stim_file = "C:/Users/apalman/OneDrive - UvA/Desktop/stimuli_round2.xlsx"
stim_file = setup.stimuli_excel
stim_file_data = data.importConditions(stim_file)

# Counterbalance trial order by shuffling
random.shuffle(stim_file_data)

# folder containing images
img_folder = setup.img_folder

# load description background
# img_text = "C:/Users/apalman/OneDrive - UvA/Desktop/museum_text.jpg"
img_text = setup.img_text

button_mapping = {"s":1, "w":2, "a":3, "d":4}

# Iterate through each trial in the Excel sheet
for trial_number, trial in enumerate(stim_file_data, start=1):

    # Play the sound
    noise_to_play.play(loops=-1)  # Infinite loop for continuous playback

    # Display the description text
    # imageShower.show_image(img_text, win, size=(1000, 1000), pos=(0,-50), frame=False)
    image = visual.ImageStim(win, image=img_text, pos=(0,-50), size=(1000, 1000))
    desc_text = trial['description_text']  # Assuming a 'Description' column in the Excel file
    desc_stim = visual.TextStim(win, text=desc_text, color="#F5F5DC", colorSpace='hex', height=30, pos=(0, 20), wrapWidth=450)
    # image.draw()
    desc_stim.draw()
    win.flip()

    # Start a timer
    timer = core.Clock()

    print("Waiting for 5 seconds no skip")
    while timer.getTime() < 5:
        core.wait(0.01)

    # Load img4 as the background
    # imageShower.show_image(setup.img_4pics, win, pos=(0,-50), size=(1000, 1000))
    background = visual.ImageStim(win, image=setup.img_4pics, pos=(0,-50), size=(1000, 1000))
    # background.draw()
    
    # Load and display the 4 images
    images = [trial['stim1'], trial['stim2'], trial['stim3'], trial['stim4']]
    positions = [(-123, 146), (125, 146), (-123, -104), (125, -104)]
    size = (212, 212)

    # Shuffle positions to counterbalance
    shuffle(images)
    path_images = [os.path.join(setup.img_folder, image) for image in images]
    imageShower.show_multiple_images(path_images, win, positions, size=size, wait_time=0)

    # Wait for a valid button press to continue
    print("Waiting for a valid button press")
    button_pressed = None
    while button_pressed not in setup.allowed_keys:
        keys = kb.getKeys(waitRelease=False, clear=True)
        for key in keys:
            if key.name in setup.allowed_keys:
                button_pressed = key.name
                rt = key.rt
                button_data.append([dyad_number, trial_number, trial['target_img'], button_pressed, rt])
                break
        core.wait(0.01)  # Add a small delay
        
    # Stop the sound after the trial is done
    noise_to_play.stop()

    # Writing test data
    selected_image = images[button_mapping[button_pressed-1]]
    csv_writer.write_row([("dyad_number",dyad_number), ("trial_number", trial_number), ("target_img", trial['stim1']), ("selected_img", selected_image), ("accuracy", trial['stim1']==selected_image), ("reaction_time", 2.5)])

noise_to_play.stop() # Stop the sound completely


# # Write the data to a CSV file
with open(output_file, "w", newline="") as f:
     writer = csv.writer(f)
     writer.writerow(headers)  # Write headers
     writer.writerows(button_data)  # Write data rows
    
# # Close the window and exit
# win.close()
# core111.quit()

# # Exit experiment
# core.quit()

# # problems:
# # 5 texts are slightly too long
# # experiment ends weirdly, no csv file is created

# # csv file: I think target image is always stim_1, so it's just about naming it well and giving the button press names
# # James suggestion: give variable names (A,B,C,D) to positions and then see if button pressed corresponds
