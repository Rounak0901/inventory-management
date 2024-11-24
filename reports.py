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
        """Generate a bar chart showing stock distribution by category."""
        from collections import defaultdict
        from rich.progress import Progress, BarColumn, TimeRemainingColumn

        category_distribution = defaultdict(int)
        for item in self.inventory_manager.inventory:
            category_distribution[item["category"]] += item["quantity"]

        console.print("\n[bold cyan]Category-Wise Stock Distribution:[/bold cyan]\n")

        with Progress("[progress.description]{task.description}", BarColumn(), TimeRemainingColumn(), console=console) as progress:
            for category, stock in category_distribution.items():
                task = progress.add_task(category, total=max(category_distribution.values()))
                progress.advance(task, stock)
    
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



