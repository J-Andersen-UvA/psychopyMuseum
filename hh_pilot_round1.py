from psychopy import visual, core, event, sound
from psychopy.hardware import keyboard

#create window
win = visual.Window([800, 600], color="black", units="pix", fullscr=False)

# create intro text 
ronde1 = visual.TextStim(win, text="Ronde 1", color="white", height=50)
instr1 = visual.TextStim(win, text="In deze opdracht zien jullie een gespreksonderwerp op het scherm. Gebruik deze als inspiratie voor een gesprek en praat er vrijuit over. Als jullie het gevoel hebben dat er niets meer is om over te praten, druk dan op een knop op de buttonbox en er verschijnen nieuwe gespreksonderwerpen.", color="white", height=30)

#display intro
ronde1.draw()
win.flip()  # Update the window

# Start a timer
timer = core.Clock()

# Wait for 1 minute or until Enter is pressed
while timer.getTime() < 5:  # 5s
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break  
        
#display instructions
instr1.draw()
win.flip()  # Update the window

# Start a timer
timer = core.Clock()

# Wait for 1 minute or until Enter is pressed
while timer.getTime() < 60:  # 60s
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break  
        
# display prompts
        
# Create prompt 1
prompt1 = visual.TextStim(win, text="Onderwerp 1: \n\nOntwerp een vijfgangendiner bestaande uit gerechten en drankjes die jullie allebei niet lekker vinden", color="white", height=40)

# Create sound object 
sound_file = "C:/Users/apalman/OneDrive - UvA/Desktop/background_noise/beep.mp3"  
sound = sound.Sound(sound_file)

# Play sound before prompt1
#sound.play()

#display prompt1
prompt1.draw()
win.flip()  # Update the window

# set up keyboard
kb = keyboard.Keyboard()
# define buttons
valid_buttons = ['a', 'b', 'c', 'd'] 

# Wait for button press (no time limit)
waiting = True
while waiting:
    keys = kb.getKeys(waitRelease=False, clear=True)
    for key in keys:
        if key.name in valid_buttons:
            waiting = False  
            break

# Wait for 10 minutes or until Enter is pressed
while timer.getTime() < 600:  # 10 minutes (600s)
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break  

# Create prompt 2
prompt2 = visual.TextStim(win, text="Onderwerp 2: \n\nBespreek en wordt het eens met elkaar over welke twee verschillende superkrachten jullie allebei willen hebben", color="white", height=40)

# Play sound before prompt2
#sound.play()

# Clear the window and display the second prompt
win.flip()  # Clear the previous stimulus
prompt2.draw()
win.flip()  # Update the window to show the new prompt

# Wait for 10 minutes or until Enter is pressed
while timer.getTime() < 600:  # 10 minutes (600s)
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break 

# Create prompt 3
prompt3 = visual.TextStim(win, text="Onderwerp 3: \n\nPlan een vakantie waar jullie allebei van zouden genieten", color="white", height=40)

# Play sound before prompt3
#sound.play()

# Clear the window and display the second prompt
win.flip()  # Clear the previous stimulus
prompt3.draw()
win.flip()  # Update the window to show the new prompt

# Wait for 10 minutes or until Enter is pressed
while timer.getTime() < 600:  # 10 minutes (600s)
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break 

# Create prompt 4
prompt4 = visual.TextStim(win, text="Onderwerp 4: \n\nPlan een festival waar jullie allebei van zouden genieten", color="white", height=40)

# Play sound before prompt4
#sound.play()

# Clear the window and display the second prompt
win.flip()  # Clear the previous stimulus
prompt4.draw()
win.flip()  # Update the window to show the new prompt

# Wait for 10 minutes or until Enter is pressed
while timer.getTime() < 600:  # 10 minutes (600s)
    keys = event.getKeys()  # Check for keypresses
    if "return" in keys:  # return = enter
        break 

# Close window 
win.close()

# Exit experiment
core.quit()