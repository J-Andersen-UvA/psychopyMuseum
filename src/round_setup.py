import yaml
import os

class RoundSetup:
        def __init__(self, round_number=1):
                # Load the YAML configuration file
                with open("roundconfig" + round_number + ".yaml", 'r') as f:
                        self.round = yaml.safe_load(f)

                        # All texts to be displayed
                        self.instr = self.round["texts"]["instr"]
                        self.prompts = self.round.get("prompts")

                        # Load in all images
                        self.intro_image = self.round["images"]["intro_image"]

                        # Load in the stimulus files
                        self.stimuli_excel = self.round["stim_file"]

        def validate_paths(self):
        """
        Ensure required files and directories exist
        """
        files_to_check = [
            self.img_4pics,
            self.img_text,
            self.stimuli_excel,
            self.noise_soc_30,
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
