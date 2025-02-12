import csv
import os

class CSVWriter:
    def __init__(self, file_path, headers=None):
        self.file_path = file_path
        self.headers = headers if headers else []
        self._initialize_file()
    
    def _initialize_file(self):
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            self.write_headers()
        else:
            self._load_existing_headers()
    
    def _load_existing_headers(self):
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            existing_headers = next(reader, [])
            self.headers = existing_headers
    
    def write_headers(self):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
    
    def add_header(self, new_header):
        if new_header not in self.headers:
            self.headers.append(new_header)
            self.write_headers()
    
    def modify_header(self, old_header, new_header):
        if old_header in self.headers:
            index = self.headers.index(old_header)
            self.headers[index] = new_header
            self.write_headers()
    
    def write_row(self, data):
        row = [None] * len(self.headers)
        data_dict = dict(data)
        
        for i, header in enumerate(self.headers):
            if header in data_dict:
                row[i] = data_dict[header]
        
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    
    def get_headers(self):
        return self.headers

# Example usage
headers = ["dyad_number", "trial_number", "target_img", "selected_img", "accuracy", "reaction_time"]
os.makedirs("output", exist_ok=True)
csv_writer = CSVWriter("output/data.csv", headers)

# Writing test data
csv_writer.write_row([("dyad_number", 1), ("trial_number", 101), ("target_img", "image1.jpg"), ("selected_img", "image2.jpg"), ("accuracy", 1), ("reaction_time", 2.5)])
csv_writer.write_row([("dyad_number", 2), ("trial_number", 102), ("target_img", "image3.jpg"), ("selected_img", "image3.jpg"), ("accuracy", 1), ("reaction_time", 1.8)])
