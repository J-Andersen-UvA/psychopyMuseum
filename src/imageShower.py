import os
from psychopy import visual, core
from random import shuffle


def show_image(image_location, window, size=(700, 700), width=720, height=720, lineColor="black", lineWidth=10, pos=(0, 0), frame=True, flip=True):
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
    if not image_location:
        return False

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
        if flip:
            window.flip()

        return True
    else:
        print(f"Image not found: {image_location}")
        return False

def show_multiple_images(image_locations, window, positions, size=(212, 212), show_tags=True):
    # Shuffle positions to counterbalance

    # Draw all images
    for i, image_location in enumerate(image_locations):
        if os.path.exists(image_location):
            visual.ImageStim(window, image=image_location, pos=positions[i], size=size).draw()
            if show_tags:
                tagx, tagy = positions[i][0] + size[0] / 2 - 30, positions[i][1] - size[1] / 2 + 30  # Adjusting for bottom-right position
                visual.Rect(window, width=40, height=40, color='black', pos=(tagx, tagy)).draw()
                visual.TextStim(window, text=str(i+1), color="#F5F5DC", height=30, pos=(tagx, tagy)).draw()
        else:
            print(f"Image not found: {image_location}")

    window.flip()
