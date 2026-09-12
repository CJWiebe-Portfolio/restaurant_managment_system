"""
create_restaurant.py
=====================
Handles the restaurant *setup* step: collecting the restaurant's name,
menu items, prices, starting sales counts, and starting inventory
counts, all via user input.

The `Create` class doesn't build a `Restaurant` itself -- it just
gathers the raw data (name, menu, prices, sales, inventory) that
main.py then hands to `Restaurant(...)`.
"""


class Create:
    """Gathers a new restaurant's setup info (name, menu, prices, sales, inventory) from the user."""

    def create_name(self):
        """Ask for and return the restaurant's name."""
        name = input("What is the name of the restaurant? ")
        return name

    def create_menu(self):
        """
        Ask the user to list every item the restaurant sells.

        Returns a dict of {item_name: None} -- at this stage we only
        care about *which* items exist. Prices, sales, and inventory
        counts for each item are filled in separately below.
        """
        menu = {}

        while True:
            item = input("What is the name of the item you would like to add? ")
            menu[item] = None

            additional_item = input("Would you like to add another? (y/n) ")
            if additional_item != "y":
                break

        return menu

    def create_prices(self, menu):
        """Ask the user for a price for every item in `menu`, return {item: price}."""
        prices = {}

        for item in menu:
            prices[item] = float(input(f"What price would you like to set for {item}? "))

        return prices

    def create_sales(self, menu):
        """Every item starts with 0 units sold. Returns {item: 0}."""
        sales = {}

        for item in menu:
            sales[item] = 0

        return sales

    def create_inventory(self, menu):
        """Ask the user how many of each item are currently in stock, return {item: quantity}."""
        inventory = {}

        for item in menu:
            quantity_input = input(f"How many {item} do you currently have in stock? ")
            inventory[item] = int(quantity_input)

        return inventory
