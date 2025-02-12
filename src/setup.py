import yaml
import os
from src import popUp
popUp = popUp.PopUp()

class ExperimentSetup:
    def __init__(self, config_file="config.yaml"):
        # Load the YAML configuration file
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Parse config into attributes
        self.experiment_name = self.config["experiment"]["name"]
        self.author = self.config["experiment"]["author"]
        self.description = self.config["experiment"]["description"]

        # Window configuration
        self.window_size = self.config["window"]["size"]
        self.window_color = self.config["window"]["color"]
        self.window_units = self.config["window"]["units"]
        self.fullscreen = self.config["window"]["fullscreen"]

        # File paths
        self.output_folder = os.path.abspath(self.config["files"]["output_folder"])
        self.output_file = os.path.abspath(self.config["files"]["output_file"])
        self.img_folder_museum = os.path.abspath(self.config["files"]["img_folder_museum"])
        self.img_4pics = os.path.join(self.img_folder_museum, self.config["files"]["img_4pics"])
        self.img_text = os.path.join(self.img_folder_museum, self.config["files"]["img_text"])
        self.stimuli_excel = os.path.abspath(self.config["files"]["stimuli_excel"])
        self.img_folder = os.path.abspath(self.config["files"]["img_folder"])
        self.noise_folder = os.path.abspath(self.config["files"]["noise_folder"])
        self.noise_soc_10 = os.path.join(self.noise_folder, self.config["files"]["noise_soc_10"])
        self.noise_soc_30 = os.path.join(self.noise_folder, self.config["files"]["noise_soc_30"])
        self.noise_nonsoc_10 = os.path.join(self.noise_folder, self.config["files"]["pink_noise_10"])
        self.noise_nonsoc_30 = os.path.join(self.noise_folder, self.config["files"]["pink_noise_30"])

        # Keyboard
        self.key_1 = self.config["input"]["key_1"]
        self.key_2 = self.config["input"]["key_2"]
        self.key_3 = self.config["input"]["key_3"]
        self.key_4 = self.config["input"]["key_4"]
        self.allowed_keys = [self.config["input"][key] for key in self.config["input"]]

        # Timing
        self.intro_duration = self.config["timing"]["intro_duration"]
        self.instructions_duration = self.config["timing"]["instructions_duration"]
        self.description_duration = self.config["timing"]["description_duration"]

        # Randomization
        self.shuffle_images = self.config["randomization"]["shuffle_images"]

        # stimulus file
        self.stim_folder = os.path.abspath(self.config["files"]["stimuli_folder"])
        self.stimuli_excel = os.path.join(self.stim_folder, self.config["files"]["stimuli_excel"])

# Counterbalance trial order by shuffling
    def validate_paths(self):
        # Ensure required files and directories exist
        files_to_check = [
            self.img_4pics,
            self.img_text,
            self.stimuli_excel,
            self.noise_soc_10,
            self.noise_soc_30,
            self.noise_nonsoc_10,
            self.noise_nonsoc_30
        ]

        # Check if the root folder exists
        if not os.path.exists(self.output_folder):
            create = popUp.show_popup_yesno(
                "Warning", f"The output folder '{self.output_folder}' does not exist. Do you want to create it?"
            )
            if not create:
                raise ValueError(f"Output folder path '{self.output_folder}' does not exist.")
            else:
                os.makedirs(self.output_folder, exist_ok=True)

        # Check if the main files exist
        for file in files_to_check:
            if not os.path.exists(file):
                popUp.show_warning_then_exit(
                    "Warning", f"The file '{file}' does not exist. Quiting the program..."
                )

        # Check if the image folder exists
        if not os.path.exists(self.img_folder):
            create = popUp.show_popup_yesno(
                "Warning", f"The image folder '{self.img_folder}' does not exist. Do you want to create it?"
            )
            if not create:
                raise FileNotFoundError(f"Image folder not found: {self.img_folder}")
            else:
                os.makedirs(self.img_folder, exist_ok=True)
