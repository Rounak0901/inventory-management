from rich.console import Console
from rich.bar import Bar
from rich.table import Table
from rich.panel import Panel
from collections import defaultdict
from rich.progress import Progress, BarColumn, TimeRemainingColumn

console = Console()

class ReportGenerator:
    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager

    def generate_summary(self):
        inventory = self.inventory_manager.inventory
        if not inventory:
            console.print("[bold red]No items in inventory.[/bold red]")
            return

        total_items = sum(item["quantity"] for item in inventory)
        total_value = sum(item["quantity"] * item["price"] for item in inventory)

        console.print(f"\n[bold cyan]Inventory Summary[/bold cyan]")
        console.print(f"Total items: [bold]{total_items}[/bold]")
        console.print(f"Total value: [bold]${total_value:.2f}[/bold]\n")

    def generate_low_stock_alert(self, threshold=10):
        """Display items with stock below the specified threshold."""
        low_stock_items = [item for item in self.inventory_manager.inventory if item["quantity"] < threshold]

        if not low_stock_items:
            console.print(f"[bold green]No items below the threshold of {threshold}.[/bold green]")
            return

        table = Table(title=f"Low-Stock Items (Threshold: {threshold})")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="green")
        table.add_column("Category", style="magenta")
        table.add_column("Quantity", justify="right")
        table.add_column("Price", justify="right")

        for item in low_stock_items:
            table.add_row(
                str(item["id"]),
                item["name"],
                item["category"],
                str(item["quantity"]),
                f"${item['price']:.2f}"
            )

        console.print(table)
    

    def generate_category_distribution(self):
        """Generate a visually appealing category-wise stock distribution chart."""

        # Collect stock distribution by category
        category_distribution = defaultdict(int)
        for item in self.inventory_manager.inventory:
            category_distribution[item["category"]] += item["quantity"]

        if not category_distribution:
            console.print("[bold red]No inventory items to display.[/bold red]")
            return

        # Find the category with the maximum stock for scaling
        max_stock = max(category_distribution.values())

        console.print("\n[bold cyan]Category-Wise Stock Distribution:[/bold cyan]\n")

        # Create a table for better formatting
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan", justify="left")
        table.add_column("Stock Count", justify="right")
        table.add_column("Bar Chart", justify="left")

        # Add rows to the table
        for category, stock in category_distribution.items():
            # Generate a scaled bar
            bar_length = int((stock / max_stock) * 30)  # Scale bar to max 30 units
            bar = f"[green]{'█' * bar_length}[/green]" if stock > max_stock * 0.7 else \
                f"[yellow]{'█' * bar_length}[/yellow]" if stock > max_stock * 0.4 else \
                f"[red]{'█' * bar_length}[/red]"

            table.add_row(category, str(stock), bar)

        console.print(table)
    
    def generate_inventory_value_trend(self):
        """Generate inventory value trends."""
        total_value = sum(item["quantity"] * item["price"] for item in self.inventory_manager.inventory)

        console.print("\n[bold cyan]Inventory Value Trends:[/bold cyan]\n")
        table = Table(title="Inventory Value Details")
        table.add_column("Total Items", justify="right")
        table.add_column("Total Value", justify="right")

        table.add_row(
            str(len(self.inventory_manager.inventory)),
            f"${total_value:.2f}"
        )

        console.print(table)



