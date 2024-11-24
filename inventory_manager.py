from rich.table import Table
from rich.console import Console
from datastore import DataStore
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


class InventoryManager:
    def __init__(self):
        self.datastore = DataStore()
        self.inventory = self.datastore.load_data()
        self.next_id = self._get_next_id()
        self.console = Console()

    def _get_next_id(self):
        """Get the next ID based on existing data."""
        if not self.inventory:
            return 1
        return max(item["id"] for item in self.inventory) + 1

    def view_items(self):
        if not self.inventory:
            console.print("[bold red]No items in inventory.[/bold red]")
            return

        table = Table(title="Inventory Items")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="green")
        table.add_column("Category", style="magenta")
        table.add_column("Quantity", justify="right")
        table.add_column("Price", justify="right")

        for item in self.inventory:
            table.add_row(
                str(item["id"]),
                item["name"],
                item["category"],
                str(item["quantity"]),
                f"${item['price']:.2f}"
            )

        self.console.print(table)

    def _validate_positive_number(self, value, field_name):
        """Ensure the input is a positive number."""
        try:
            value = float(value)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            raise ValueError(f"{field_name} must be a positive number.")

    def add_item(self):
        try:
            name = input("Enter item name: ")
            category = input("Enter item category: ")
            quantity = self._validate_positive_number(input("Enter quantity: "), "Quantity")
            price = self._validate_positive_number(input("Enter price: "), "Price")

            new_item = {
                "id": self.next_id,
                "name": name,
                "category": category,
                "quantity": int(quantity),
                "price": float(price),
            }
            self.inventory.append(new_item)
            self.datastore.save_data(self.inventory)
            self.next_id += 1

            self.console.print("[bold green]Item added successfully![/bold green]")
        except ValueError as e:
            self.console.print(f"[bold red]{e}[/bold red]")

    def edit_item(self):
        try:
            item_id = int(input("Enter the ID of the item to edit: "))
            for item in self.inventory:
                if item["id"] == item_id:
                    item["name"] = input(f"Enter new name ({item['name']}): ") or item["name"]
                    item["category"] = input(f"Enter new category ({item['category']}): ") or item["category"]
                    item["quantity"] = self._validate_positive_number(
                        input(f"Enter new quantity ({item['quantity']}): ") or item["quantity"], "Quantity"
                    )
                    item["price"] = self._validate_positive_number(
                        input(f"Enter new price ({item['price']}): ") or item["price"], "Price"
                    )
                    self.datastore.save_data(self.inventory)
                    self.console.print("[bold green]Item updated successfully![/bold green]")
                    return

            self.console.print("[bold red]Item not found.[/bold red]")
        except ValueError as e:
            self.console.print(f"[bold red]{e}[/bold red]")
    
    def delete_item(self):
        item_id = int(input("Enter the ID of the item to delete: "))
        for item in self.inventory:
            if item["id"] == item_id:
                self.inventory.remove(item)
                self.datastore.save_data(self.inventory)
                self.console.print("[bold green]Item deleted successfully![/bold green]")
                return

        self.console.print("[bold red]Item not found.[/bold red]")

    def search_items(self):
        search_options = WordCompleter(
            ["name", "category", "price range"],
            ignore_case=True,
            sentence=True,
        )
        search_by = prompt("Search by (name, category, price range): ", completer=search_options)

        if search_by.lower() == "name":
            name = input("Enter the item name to search: ").lower()
            results = [item for item in self.inventory if name in item["name"].lower()]
        elif search_by.lower() == "category":
            category = input("Enter the category to search: ").lower()
            results = [item for item in self.inventory if category in item["category"].lower()]
        elif search_by.lower() == "price range":
            min_price = float(input("Enter minimum price: "))
            max_price = float(input("Enter maximum price: "))
            results = [item for item in self.inventory if min_price <= item["price"] <= max_price]
        else:
            self.console.print("[bold red]Invalid search option.[/bold red]")
            return

        if results:
            table = Table(title="Search Results")
            table.add_column("ID", style="cyan", justify="center")
            table.add_column("Name", style="green")
            table.add_column("Category", style="magenta")
            table.add_column("Quantity", justify="right")
            table.add_column("Price", justify="right")

            for item in results:
                table.add_row(
                    str(item["id"]),
                    item["name"],
                    item["category"],
                    str(item["quantity"]),
                    f"${item['price']:.2f}"
                )

            self.console.print(table)
        else:
            self.console.print("[bold red]No items found matching the search criteria.[/bold red]")
