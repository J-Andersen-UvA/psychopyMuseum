import yaml
import os

class RoundSetup:
    def __init__(self, round_number=1):
        # Load the YAML configuration file
        with open("roundconfig" + str(round_number) + ".yaml", 'r') as f:
            self.round = yaml.safe_load(f)

            # All texts to be displayed
            self.instr = self.round["texts"]["instr"]
            self.switch = self.round["texts"]["switch"]
            self.prompts = self.round.get("prompts")

            # Load in all images
            self.img4_background = self.round["images"]["img4_background"]
            self.img1_background = self.round["images"]["img1_background"]
            self.text_background = self.round["images"]["text_background"]

            # Load in the stimulus files
            self.stim_file = self.round["stim_file"]

    def validate_paths(self):
        files_to_check = [
            self.img4_background,
            self.img1_background,
            self.text_background,
            self.stim_file,
        ]
        
        # Loop through files to check if they exist
        for file in files_to_check:
            if not os.path.isfile(file):
                print(f"Warning: The file {file} does not exist.")


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
