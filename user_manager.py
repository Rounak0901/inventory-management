import hashlib
from rich.prompt import Prompt
from rich.console import Console
from datastore import DataStore

class UserManager:
    USERS_FILE = "data/users.json"  # Using the DataStore for user credentials

    def __init__(self):
        self.console = Console()
        self.data_store = DataStore(file_path=self.USERS_FILE)
        self.users = self.load_users()

    def load_users(self):
        """Load user data using the DataStore."""
        # Ensure data is always a dictionary, even if the file is empty
        return self.data_store.load_data() or {}

    def save_users(self):
        """Save user data using the DataStore."""
        self.data_store.save_data(self.users)

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_up(self):
        """Sign up a new user."""
        self.console.print("\n[bold cyan]Sign Up[/bold cyan]")
        username = Prompt.ask("Enter a new username")
        if username in self.users:
            self.console.print("[bold red]Username already exists! Try logging in.[/bold red]")
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
        return True

    def login(self):
        """Login an existing user."""
        self.console.print("\n[bold cyan]Login[/bold cyan]")
        username = Prompt.ask("Enter your username")
        if username not in self.users:
            self.console.print("[bold red]Username not found![/bold red]")
            return None, None

        password = Prompt.ask("Enter your password", password=True)
        hashed_password = self.hash_password(password)
        if self.users[username]["password"] == hashed_password:
            self.console.print("[bold green]Login successful![/bold green]")
            return username, self.users[username]["role"]

        self.console.print("[bold red]Incorrect password![/bold red]")
        return None, None
