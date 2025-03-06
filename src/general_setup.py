import yaml
import os
import popUp
popUp = popUp.PopUp()

class ExperimentSetup:
    """
    This is a setup class to fetch the default variables from.
    """
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

        # windows assigned to screens
        self.screenA = self.config["winA"]
        self.screenB = self.config["winB"]

        # File paths
        self.output_folder = os.path.abspath(self.config["files"]["output_folder"])
        self.noise_soc = self.config["files"]["noise_soc"]
        self.noise_nonsoc = self.config["files"]["noise_nonsoc"]

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

        # OBS connection setup
        self.no_obs = self.config["obs_connection"]["no_obs"]
        self.obs_host = self.config["obs_connection"]["obs_host"]
        self.obs_port = self.config["obs_connection"]["obs_port"]
        self.obs_password = self.config["obs_connection"].get("obs_password", "")

    def validate_paths(self):
        """
        Ensure required files and directories exist
        """
        files_to_check = [
            self.noise_soc,
            self.noise_nonsoc
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
