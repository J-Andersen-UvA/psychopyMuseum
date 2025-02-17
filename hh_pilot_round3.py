"""
Author: Anna Palmann

Description: This script is the third round.
"""
from psychopy import visual, core, event, sound, data
from psychopy.hardware import mouse, keyboard
import os, random
from src.OBSRecorder.src.obsRecording import OBSController
from src.setup import ExperimentSetup
import src.popUp as popUp
import websocket

setup = ExperimentSetup("config.yaml")
setup.validate_paths()

# A: 1 painting first, then 4 paintings
# B: 4 paintings first, then 1 painting
if not setup.no_obs:
    obs = OBSController(setup.obs_host, setup.obs_port, setup.obs_password, popUp=popUp.PopUp())
    obs.set_save_location(setup.output_folder)
    obs.start_recording()

# Start a timer
timer = core.Clock()

# set up keyboard for the button box
kb = keyboard.Keyboard()

# Define output file for button presses 
output_file = "C:/Users/apalman/OneDrive - UvA/Desktop/output_round3.csv"
# Define column headers
headers = ["Key", "ReactionTime"]
# Prepare to record button presses
button_data = []

# time the 5 min (300s) that mark half of the experiment
while timer.getTime() < 30:  # 300s = 5min
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break
    core.wait(0.01)
        
#create window
winA = visual.Window([800, 600], color="black", units="pix", screen=2, fullscr=False) # 1 painting (participant A)
winB = visual.Window([800, 600], color="black", units="pix", screen=3, fullscr=False) # 4 paintings (participant B)

# create intro text 
ronde3A = visual.TextStim(winA, text="Ronde 3", color="white", height=50)
ronde3B = visual.TextStim(winB, text="Ronde 3", color="white", height=50)

#display intro
ronde3A.draw()
winA.flip()  # Update the window

ronde3B.draw()
winB.flip()  

kb.clearEvents()  # Clear keyboard buffer

# Start the main timer
main_timer = core.Clock()

# Wait for 1 minute or until Enter is pressed
while main_timer.getTime() < 5:  # 5s
    keys = kb.getKeys()   # Check for keypresses
    if "return" in [key.name for key in keys]:  # return = enter
        break  

# create instructions 
instr3A = visual.TextStim(winA, text="In deze opdracht kijken jullie naar verschillende schermen. Een van jullie ziet een abstract schilderij, terwijl de anderen vier schilderijen op het scherm zien. Het is jullie taak om samen te overleggen en voor degene die een schilderij ziet, om het zo te beschrijven dat de andere het juiste schilderij uit de vier schilderijen kan kiezen. Als jullie dat hebben besloten, gebruiken jullie het knoppenvak om een schilderij te selecteren. Vervolgens verschijnt de volgende beschrijving. Jullie wisselen van rol na de helft van de tijd.", color="white", height=30)
instr3B = visual.TextStim(winB, text="In deze opdracht kijken jullie naar verschillende schermen. Een van jullie ziet een abstract schilderij, terwijl de anderen vier schilderijen op het scherm zien. Het is jullie taak om samen te overleggen en voor degene die een schilderij ziet, om het zo te beschrijven dat de andere het juiste schilderij uit de vier schilderijen kan kiezen. Als jullie dat hebben besloten, gebruiken jullie het knoppenvak om een schilderij te selecteren. Vervolgens verschijnt de volgende beschrijving. Jullie wisselen van rol na de helft van de tijd.", color="white", height=30)

#display intro
instr3A.draw()
winA.flip()  # Update the window

instr3B.draw()
winB.flip()  

# Wait for 1 minute or until Enter is pressed
while main_timer.getTime() < 60:  # 60s
    keys = kb.getKeys()   # Check for keypresses
    if "return" in [key.name for key in keys]:  # return = enter
        break  
        
# load and display intro image for screen B
img_4pics = "C:/Users/apalman/OneDrive - UvA/Desktop/museum_4pics.jpg"
if os.path.exists(img_4pics):
    image = visual.ImageStim(winB, image=img_4pics, size=(700, 700))  
    frame = visual.Rect(
        win=winB,
        width=720,  # Slightly larger than the image width
        height=720,  # Slightly larger than the image height
        lineColor="black",  # Black frame
        fillColor=None,  # Transparent fill
        lineWidth=10  # Thickness of the frame
    )
    frame.draw()
    image.draw()
    
    winB.flip()
    core.wait(5)  
else:
    print(f"Image not found: {img_4pics}")
    
# zoom in intro image
img_4pics = "C:/Users/apalman/OneDrive - UvA/Desktop/museum_4pics.jpg"
if os.path.exists(img_4pics):
    image = visual.ImageStim(winB, image=img_4pics, pos=(0,-50), size=(1000, 1000))  
    frame = visual.Rect(
        win=winB,
        width=720,  # Slightly larger than the image width
        height=720,  # Slightly larger than the image height
        lineColor="black",  # Black frame
        fillColor=None,  # Transparent fill
        lineWidth=10  # Thickness of the frame
    )
    frame.draw()
    image.draw()
    
    winB.flip()
    core.wait(5)  
else:
    print(f"Image not found: {img_4pics}")
    
# load and display intro image for screen A
img_1pic = "C:/Users/apalman/OneDrive - UvA/Desktop/museum_1ic.jpg"
if os.path.exists(img_1pic):
    image = visual.ImageStim(winA, image=img_1pic, size=(700, 700))  
    frame = visual.Rect(
        win=winA,
        width=720,  # Slightly larger than the image width
        height=720,  # Slightly larger than the image height
        lineColor="black",  # Black frame
        fillColor=None,  # Transparent fill
        lineWidth=10  # Thickness of the frame
    )
    frame.draw()
    image.draw()
    
    winA.flip()
    core.wait(5)  
else:
    print(f"Image not found: {img_4pics}")
    
# zoom in intro image
img_1pic = "C:/Users/apalman/OneDrive - UvA/Desktop/museum_1pic.jpg"
if os.path.exists(img_1pic):
    image = visual.ImageStim(winA, image=img_1pic, pos=(0,-50), size=(1000, 1000))  
    frame = visual.Rect(
        win=winA,
        width=720,  # Slightly larger than the image width
        height=720,  # Slightly larger than the image height
        lineColor="black",  # Black frame
        fillColor=None,  # Transparent fill
        lineWidth=10  # Thickness of the frame
    )
    frame.draw()
    image.draw()
    
    winA.flip()
    core.wait(5)  
else:
    print(f"Image not found: {img_4pics}")
        
# stimulus file
stim_file = "C:/Users/apalman/OneDrive - UvA/Desktop/stimuli_round3.xlsx"
stim_file_data = data.importConditions(stim_file)

# Counterbalance trial order by shuffling
random.shuffle(stim_file_data)

# folder containing images
img_folder = "C:/Users/apalman/OneDrive - UvA/Desktop/img_folder/"

# Role switch info
role_switched = False

# Iterate through each trial in the Excel sheet
for trial in stim_file_data:
    # Check if it's time to switch roles 
    if main_timer.getTime() > 30 and not role_switched:
        role_switched = True  # Ensure roles are only switched once
        switch_text_A = visual.TextStim(winA, text="De rollen zijn nu omgedraaid", color="white", height=30)
        switch_text_B = visual.TextStim(winB, text="De rollen zijn nu omgedraaid", color="white", height=30)
        switch_text_A.draw() # draw text
        switch_text_B.draw() # draw text
        winA.flip()
        winB.flip()
        core.wait(5) # wait for 5s
        winA, winB = winB, winA  # Swap the windows
    
    # Load img4 as the backgroundB
    backgroundB = visual.ImageStim(winB, image=img_4pics, pos=(0,-50), size=(1000, 1000)) 
    backgroundB.draw()
    
    # Load and display the 4 images
    images = [trial['stim1'], trial['stim2'], trial['stim3'], trial['stim4']]
    positions = [(-123, 146), (125, 146), (-123, -104), (125, -104)]
    size = (212, 212)
    
    # Draw all four images
    for i, img_name in enumerate(images):
        image_path = os.path.join(img_folder, img_name)
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue
        img_stim = visual.ImageStim(winB, image=image_path, pos=positions[i], size=size)
        img_stim.draw()
    
    # Load 1pic as backgroundA
    backgroundA = visual.ImageStim(winA, image=img_1pic, pos=(0,-50), size=(1000, 1000)) 
    backgroundA.draw()
    
    # Display Painting A from the row (stim1) on the second window (Screen 2)
    painting_a_path = os.path.join(img_folder, trial['stim1'])
    if os.path.exists(painting_a_path):
        painting_a_stim = visual.ImageStim(winA, image=painting_a_path, pos=(1,23), size=(485,485))
        painting_a_stim.draw()
    
    winA.flip()
    winB.flip()

    # Wait for a valid button press to continue
    valid_buttons = ['1', '2', '3', '4']
    button_pressed = None
    while button_pressed not in valid_buttons:
        keys = kb.getKeys(waitRelease=False, clear=True)
        for key in keys:
            if key.name in valid_buttons:
                button_pressed = key.name
                rt = key.rt
                button_data.append([button_pressed, rt])
                break

if not setup.no_obs:
    obs.stop_recording()

# Write the data to a CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)  # Write headers
    writer.writerows(button_data)  # Write data rows
    
# Close the window and exit
winA.close()
winB.close()

# Exit experiment
core.quit()

# problems:
# no csv file created
# csv file should have trial number and target image 
# ideally just correct/wrong as output


#old positions and sizes of 4 paintings
#positions = [(-150, 150), (150, 150), (-150, -150), (150, -150)]
#size = (250, 250)