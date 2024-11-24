from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from inventory_manager import InventoryManager
from reports import ReportGenerator 
import os

class InventoryApp:
    def __init__(self):
        self.session = PromptSession()
        self.inventory_manager = InventoryManager()
        self.report_generator = ReportGenerator(self.inventory_manager)

        # Define menu options dynamically
        self.menu_options = [
            ("View Inventory", self.inventory_manager.view_items),
            ("Add Item", self.inventory_manager.add_item),
            ("Edit Item", self.inventory_manager.edit_item),
            ("Delete Item", self.inventory_manager.delete_item),
            ("Generate Summary Report", self.report_generator.generate_summary),
            ("Search Items", self.inventory_manager.search_items),
            ("Low-Stock Alerts", self._handle_low_stock_alerts),
            ("Category-Wise Stock Distribution", self.report_generator.generate_category_distribution),
            ("Inventory Value Trends", self.report_generator.generate_inventory_value_trend)        ]
    
    def _handle_low_stock_alerts(self):
        try:
            threshold = int(input("Enter low-stock threshold: "))
            self.report_generator.generate_low_stock_alert(threshold)
        except ValueError:
            print("[bold red]Threshold must be an integer.[/bold red]")


    def display_menu(self):
        print("\n--- Inventory Management Menu ---")
        for idx, (description, _) in enumerate(self.menu_options, start=1):
            print(f"{idx}. {description}")
        print(f"{len(self.menu_options) + 1}. Exit")


    def clear_screen(self):
        print('\033c', end='')


    def start(self):
        while True:
            self.clear_screen()
            self.display_menu()
            try:
                choice = int(self.session.prompt("Choose an option: "))
                if 1 <= choice <= len(self.menu_options):
                    _, handler = self.menu_options[choice - 1]
                    handler()
                elif choice == len(self.menu_options) + 1:
                    print("Exiting... Goodbye!")
                    break
                else:
                    raise ValueError("Invalid choice.")
            except ValueError as e:
                print("[bold red]Invalid input. Please select a valid option.[/bold red]")

            input('\npress enter to continue...')


if __name__ == "__main__":
    app = InventoryApp()
    app.start()