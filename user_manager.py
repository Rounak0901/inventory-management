import hashlib
from rich.prompt import Prompt
from rich.console import Console
from datastore import DataStore
import logging

class UserManager:
    USERS_FILE = "data/users.json"  # Using the DataStore for user credentials

    def __init__(self):
        self.console = Console()
        self.data_store = DataStore(file_path=self.USERS_FILE)
        self.users = self.load_users()
        self.logger = logging.getLogger(__name__)

    def load_users(self):
        """Load user data using the DataStore."""
        # Ensure data is always a dictionary, even if the file is empty
        return self.data_store.load_data() or {}

    def save_users(self):
        """Save user data using the DataStore."""
        try:
            self.data_store.save_data(self.users)
            self.logger.info("User data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error saving user data: {e}")

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_up(self):
        """Sign up a new user."""
        self.console.print("\n[bold cyan]Sign Up[/bold cyan]")
        try:
            username = Prompt.ask("Enter a new username")
            if username in self.users:
                self.console.print("[bold red]Username already exists! Try logging in.[/bold red]")
                self.logger.warning(f"Username already exists: {username}")
                return False

            password = Prompt.ask("Enter a new password", password=True)
            confirm_password = Prompt.ask("Confirm your password", password=True)
            if password != confirm_password:
                self.console.print("[bold red]Passwords do not match![/bold red]")
                return False

            role = Prompt.ask("Assign a role (admin/viewer)", choices=["admin", "viewer"])
            self.users[username] = {"password": self.hash_password(password), "role": role}
            self.save_users()
            self.console.print("[bold green]Account created successfully![/bold green]")
            self.logger.info(f"New user signed up: {username}")
            return True
        except Exception as e:
            self.logger.error(f"An error occurred during sign-up: {e}")
            return False

    def login(self):
        """Login an existing user."""
        self.console.print("\n[bold cyan]Login[/bold cyan]")
        username = Prompt.ask("Enter your username")
        if username not in self.users:
            self.console.print("[bold red]Username not found![/bold red]")
            return None, None

        try:
            password = Prompt.ask("Enter your password", password=True)
            hashed_password = self.hash_password(password)
            if self.users[username]["password"] == hashed_password:
                self.console.print("[bold green]Login successful![/bold green]")
                self.logger.info(f"User logged in: {username}")
                return username, self.users[username]["role"]

            self.console.print("[bold red]Incorrect password![/bold red]")
            self.logger.warning(f"Login attempt failed for user: {username}")
            return None, None
        except Exception as e:
            self.logger.error(f"An error occurred during login: {e}")
            return None, None
