import yaml
import os
import popUp
from psychopy import data
from random import shuffle

class RoundSetup:
    def __init__(self, round_number):
        # Load the YAML configuration file
        with open("src/roundconfig" + str(round_number) + ".yaml", 'r') as f:
            self.round = yaml.safe_load(f)

            # All texts to be displayed
            self.instr = self.round["texts"]["instr"]
            self.switch = self.switch["texts"]["switch"]
            self.prompts = list(self.round.get("prompts", {}).values())

            # Load in all images
            self.img_folder_root = self.round["images"]["img_folder"]
            self.img4_background = self.img_folder_root + self.round["images"]["img4_background"] if (self.round["images"]["img4_background"] and self.img_folder_root) else None
            self.img1_background = self.img_folder_root + self.round["images"]["img1_background"] if (self.round["images"]["img1_background"] and self.img_folder_root) else None
            self.text_background = self.img_folder_root + self.round["images"]["text_background"] if (self.round["images"]["text_background"] and self.img_folder_root) else None
            self.img_folder = self.img_folder_root + "artworks/" if self.img_folder_root else None

            # Load in the stimulus files
            self.stims = self.stimulus_setup(self.round["stimuli"]["stim_file"])

            self.role_switch = self.round.get("role_switch")

            # self.validate_paths()
    
    def stimulus_setup(self, file_path):
        stim_file_data = data.importConditions(file_path) # import Excel sheet data
        shuffle(stim_file_data)
        return stim_file_data


    def validate_paths(self):
        files_to_check = [
            self.img4_background,
            self.img1_background,
            self.text_background,
        ]

        # # Check if the root folder exists
        # if not os.path.exists(self.output_folder):
        #     create = popUp.show_popup_yesno(
        #         "Warning", f"The output folder '{self.output_folder}' does not exist. Do you want to create it?"
        #     )
        #     if not create:
        #         raise ValueError(f"Output folder path '{self.output_folder}' does not exist.")
        #     else:
        #         os.makedirs(self.output_folder, exist_ok=True)

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
