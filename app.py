from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from inventory_manager import InventoryManager
from reports import ReportGenerator 
import os
from user_manager import UserManager
from rich.prompt import Prompt
from rich.console import Console
import time

class InventoryApp:
    def __init__(self):
        self.session = PromptSession()
        self.console = Console()
        self.inventory_manager = InventoryManager()
        self.report_generator = ReportGenerator(self.inventory_manager)
        self.user_manager = UserManager()
        self.session_user = None
        self.session_role = None

        # Define menu options dynamically
        self.menu_options = [
            ("View Inventory", self.inventory_manager.view_items, 'viewer'),
            ("Add Item", self.inventory_manager.add_item, 'admin'),
            ("Edit Item", self.inventory_manager.edit_item, 'admin'),
            ("Delete Item", self.inventory_manager.delete_item, 'admin'),
            ("Generate Summary Report", self.report_generator.generate_summary, 'viewer'),
            ("Search Items", self.inventory_manager.search_items, 'viewer'),
            ("Low-Stock Alerts", self._handle_low_stock_alerts, 'viewer'),
            ("Category-Wise Stock Distribution", self.report_generator.generate_category_distribution, 'viewer'),
            ("Inventory Value Trends", self.report_generator.generate_inventory_value_trend, 'viewer'),
            ("Exit", self.exit_app, "viewer"),
        ]
    
    def authenticate(self):
        """Handle user login or signup."""
        while not self.session_user:
            self.console.print("\n[bold cyan]Welcome to Inventory Management App[/bold cyan]")
            choice = Prompt.ask("Do you want to [b](L)[/b]ogin or [b](S)[/b]ign up?", choices=["L", "S"], case_sensitive=False)
            if choice == "L":
                self.session_user, self.session_role = self.user_manager.login()
            elif choice == "S":
                self.user_manager.sign_up()
    
    def _handle_low_stock_alerts(self):
        try:
            threshold = int(input("Enter low-stock threshold: "))
            self.report_generator.generate_low_stock_alert(threshold)
        except ValueError:
            print("[bold red]Threshold must be an integer.[/bold red]")


    def display_menu(self):
        """Display the menu based on the user's role."""
        self.console.print("\n[bold cyan]--- Inventory Management Menu ---[/bold cyan]")
        for idx, (description, _, role) in enumerate(self.menu_options, start=1):
            if self.is_action_allowed(role):
                self.console.print(f"{idx}. {description}")

    def is_action_allowed(self, role):
        """Check if the current user has the required role."""
        if self.session_role == "admin":
            return True  # Admins have access to everything
        return self.session_role == role

    def clear_screen(self):
        print('\033c', end='')


    def start(self):
        self.clear_screen()
        self.authenticate()  # Ensure the user is authenticated
        self.console.print(f"\n[bold green]Welcome, {self.session_user}![/bold green]")
        time.sleep(3)
        while True:
            self.clear_screen()
            self.display_menu()
            choice = Prompt.ask("Choose an option", choices=[str(i) for i in range(1, len(self.menu_options) + 1)], show_choices=False)
            idx = int(choice) - 1
            description, handler, role = self.menu_options[idx]
            if self.is_action_allowed(role):
                handler()
            else:
                self.console.print("[bold red]Access denied![/bold red]")
            input('\npress enter to continue...')

    def exit_app(self):
        self.console.print("[bold green]Exiting the application... Goodbye![/bold green]")
        exit()


if __name__ == "__main__":
    app = InventoryApp()
    app.start()