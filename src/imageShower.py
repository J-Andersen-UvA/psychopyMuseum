import os
from psychopy import visual, core
from random import shuffle


def show_image(image_location, window, size=(700, 700), width=720, height=720, lineColor="black", lineWidth=10, pos=(0, 0), wait_time=5, frame=True):
    """
    Displays an image with an optional frame on a PsychoPy window.

    Args:
        image_location (str): Path to the image file.
        window (psychopy.visual.Window): The PsychoPy window object.
        size (tuple): Size of the image (width, height).
        width (int): Width of the frame.
        height (int): Height of the frame.
        lineColor (str): Color of the frame.
        lineWidth (int): Thickness of the frame line.
        pos (tuple): Position of the image and frame.
        wait_time (float): Time to display the image (seconds).
        frame (bool): Whether to draw a frame around the image.

    """
    # load and display intro image
    if os.path.exists(image_location):
        image = visual.ImageStim(window, image=image_location, pos=pos, size=size)
        if frame:
            frame = visual.Rect(
                win=window,
                width=width,  # Slightly larger than the image width
                height=height,  # Slightly larger than the image height
                lineColor=lineColor,  # Black frame
                fillColor=None,  # Transparent fill
                lineWidth=lineWidth  # Thickness of the frame
            )
            frame.draw()
        image.draw()
        window.flip()

        print(f"[Show image] Waiting for {wait_time} seconds no skip")
        timer = core.Clock()
        while timer.getTime() < wait_time:
            core.wait(0.01)
    else:
        print(f"Image not found: {image_location}")

def show_multiple_images(image_locations, window, positions, size=(212, 212), wait_time=5):
    # Shuffle positions to counterbalance
    shuffle(positions)

    # Draw all images
    for i, image_location in enumerate(image_locations):
        if os.path.exists(image_location):
            img_stim = visual.ImageStim(window, image=image_location, pos=positions[i], size=size)
            img_stim.draw()
        else:
            print(f"Image not found: {image_location}")

    window.flip()

    print(f"[Show multiple images] Waiting for {wait_time} seconds no skip")
    timer = core.Clock()
    while timer.getTime() < wait_time:
        core.wait(0.01)

def show_multiple_images(show_tags=True):
    if show_tags:
        number_tags = ["1", "2", "3", "4"]  # Define number tags (always in the same positions)
        number_pos = [(89, 328), (337, 328), (89, 78), (337, 78)]
        for i in range(4):
            number_text = visual.TextStim(win, text=number_tags[i], color="#F5F5DC", height=30, pos=number_pos)
            number_text.draw()  # Draw on top of images

def update_window(window, content):
    content.draw()
    window.flip()

