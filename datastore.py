import json
import os
import logging

class DataStore:
    def __init__(self, file_path="data/inventory.json"):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load_data(self):
        """Load inventory data from the JSON file."""
        if os.path.exists(self.file_path):
            self.logger.info(f"Loading data from {self.file_path}")
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    self.logger.info("Data loaded successfully.")
                    return data
                except json.JSONDecodeError:
                    self.logger.error(f"Error loading data from {self.file_path}: Invalid JSON format.")
                    return []
        else:
            self.logger.warning(f"File not found: {self.file_path}. Starting with empty inventory.")
        return []

    def save_data(self, data):
        """Save inventory data to the JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
        self.logger.info(f"Data saved to {self.file_path}")
