# README for psychopyMuseum

## Overview
This project implements a psychological experiment using the PsychoPy framework. The experiment involves displaying text, images, and interactive tasks for participants, recording their responses and reaction times. The goal is to provide a seamless and engaging experience while collecting reliable data.

## Directory Structure
#### Main Directories:
- src/helpers
    - Contains utility modules, such as `imageShower.py`.
- src/setup
    - Contains code related to setting up the experiment, such as `roundconfig1.yaml`.
- stimuli/
    - Contains Excel files and images for the experiment stimuli.
- output/
    - Stores the experiment's output files, such as CSV logs.
- img_folder/
    - Contains images of artworks used in the experiment.
- noise_folder/
    - A folder that you need to supply yourself containing the noises to be played during experiments.


#### Key Files:
- round_player.py
    - The main script for running the experiment, handling the display of images, text, and recording responses.
- config.yaml
    - Configuration file specifying experiment parameters, paths, and settings.
- roundconfig3.yaml
    - Configuration file for "Round 3" of the experiment, detailing instructions, images, and stimuli.
- stimuli_round3.xlsx
    - Excel sheet defining the trials and stimuli details for "Round 3" of the experiment.

## Installation
#### Requirements:
- Python 3.8 or higher
- PsychoPy library
##### Submodules:
- [OBSRecorder](https://github.com/J-Andersen-UvA/OBSRecorder/tree/8a4691142d1147759cee55cd6640cca6ee71f5cb)
- [audioPlayerPy](https://github.com/J-Andersen-UvA/audioPlayerPy/tree/28abdd860f846c884200ec5c74977a8e380af6e3)

#### Setup:
1. Install the dependencies:
    ```python
    pip install psychopy
    pip install obsws_python
    pip install websocket-client
    pip install pyaudio
    pip install pyyaml
    pip install asyncio
    ```
2. Ensure the `config.yaml` file is set up with the correct paths and parameters.
3. Place the stimuli images and Excel files in the appropriate folders.
4. Place the artworks in the artworks folder.
5. Import noise and set correct paths for the noise.


