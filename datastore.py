import json
import os
from rich.console import Console

class DataStore:
    def __init__(self, file_path="data/inventory.json"):
        self.file_path = file_path
        self.console = Console()
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load_data(self):
        """Load inventory data from the JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def save_data(self, data):
        """Save inventory data to the JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
        self.console.print("[bold green]Data saved successfully![/bold green]")
