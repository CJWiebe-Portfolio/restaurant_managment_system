"""
final_report.py
================
The `Report` class: given a restaurant's data (menu, prices, sales,
inventory), prints a summary of the day -- revenue per item, total
revenue, and the best-selling item.
"""


class Report:
    """Builds and prints a daily sales report for a restaurant."""

    def __init__(self, name, menu, prices, sales, inventory):
        self.name = name
        self.menu = menu
        self.prices = prices
        self.sales = sales
        self.inventory = inventory

    def calculate_total_revenue(self):
        """Print revenue earned by each item, then print and return the total revenue."""
        total_revenue = 0

        for item in self.sales:  # iterating over a dict gives you its keys
            item_revenue = self.prices[item] * self.sales[item]
            total_revenue += item_revenue
            print(f"{item}: {self.sales[item]} sold, ${item_revenue:.2f} in revenue")

        print(f"\nThe total revenue is: ${total_revenue:.2f}")
        return total_revenue

    def find_best_seller(self):
        """Print and return the item with the highest sales count."""
        best_item = None
        largest_quantity = -1

        for item in self.sales:
            if self.sales[item] > largest_quantity:
                largest_quantity = self.sales[item]
                best_item = item

        print(f"The best-selling item is {best_item}, with {largest_quantity} sold.")
        return best_item

    def print_daily_report(self):
        """Print the full daily report: header, per-item + total revenue, and the best seller."""
        print(f"\n--- DAILY REPORT for {self.name} ---")
        self.calculate_total_revenue()
        self.find_best_seller()

    def report_text(self):
        """
        Build the same daily report as `print_daily_report()`, but return it
        as a single string instead of printing it -- handy for showing in a
        GUI window instead of the console.
        """
        lines = [f"--- DAILY REPORT for {self.name} ---", ""]

        total_revenue = 0
        for item in self.sales:
            item_revenue = self.prices[item] * self.sales[item]
            total_revenue += item_revenue
            lines.append(f"{item}: {self.sales[item]} sold, ${item_revenue:.2f} in revenue")
        lines.append("")
        lines.append(f"The total revenue is: ${total_revenue:.2f}")

        best_item = None
        largest_quantity = -1
        for item in self.sales:
            if self.sales[item] > largest_quantity:
                largest_quantity = self.sales[item]
                best_item = item
        lines.append(f"The best-selling item is {best_item}, with {largest_quantity} sold.")

        return "\n".join(lines)
