"""
restaurant.py
=============
The `Restaurant` class: represents one running restaurant (its menu,
prices, running sales totals, and inventory) and drives the ordering
loop that customers interact with.
"""

import json
import os


class Restaurant:
    """A restaurant that can take customer orders and track sales/inventory as it goes."""

    def __init__(self, name, menu, prices, sales, inventory):
        self.name = name
        self.menu = menu            # dict of {item_name: None} -- the set of items sold
        self.prices = prices        # dict of {item_name: price}
        self.sales = sales          # dict of {item_name: total units sold so far}
        self.inventory = inventory  # dict of {item_name: units currently in stock}

    # ------------------------------------------------------------------
    # Main ordering loop: keep serving customers until told to stop
    # ------------------------------------------------------------------
    def taking_an_order(self):
        """Repeatedly serve customers, one at a time, until the user says there are no more."""
        additional_customers = True

        while additional_customers:
            shopping_cart = {}

            print("--- THE RESTAURANT MANAGEMENT SYSTEM ---")
            print("These are the available menu items:")
            for item in self.menu:
                print(f"{item}, ${self.prices[item]}, currently {self.inventory[item]} items in stock")

            total_cost = self.sell_item(shopping_cart)
            print(f"The total:\n${total_cost}\nFor Items\n{shopping_cart}")

            additional_customers = self.customers(additional_customers)

    # ------------------------------------------------------------------
    # Ask whether to serve another customer
    # ------------------------------------------------------------------
    def customers(self, additional_customers):
        """Ask if there's another customer to serve; return False to stop the ordering loop."""
        another_customer = input("Would you like to checkout another customer? (y/n): ")
        if another_customer == "y":
            return additional_customers
        else:
            return False

    # ------------------------------------------------------------------
    # Take one customer's order (item + quantity, repeated until they quit)
    # ------------------------------------------------------------------
    def sell_item(self, shopping_cart):
        """
        Ask the customer for items and quantities, adding each to the
        shopping cart, until they type 'q' or successfully check out.
        """
        total_cost = 0  # in case the customer quits ('q') before ever checking out

        while True:
            item = input("What item would you like to buy? (type menu item) Or would you like to quit? (q)")

            if item == "q":
                break

            if item not in self.menu:
                print("Enter a valid item.")
                continue

            quantity_input = input("How many of that item would you like to buy: ")
            try:
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("Enter a valid quantity.")
                    continue
            except ValueError:
                print("Enter a valid quantity.")
                continue

            shopping_cart[item] = shopping_cart.get(item, 0) + quantity
            print(f"Your shopping cart contains: {shopping_cart}")

            total_cost = self.checking_out(shopping_cart)
            if total_cost > 0:
                break

        return total_cost

    # ------------------------------------------------------------------
    # Finalize the sale: update inventory + running sales, compute the bill
    # ------------------------------------------------------------------
    def checking_out(self, shopping_cart):
        """If the customer confirms, apply the cart to inventory/sales and return the bill total."""
        check_out = input("Would you like to checkout? (y/n): ")

        if check_out == "y":
            return self.sell(shopping_cart)

        return 0

    def sell(self, cart):
        """
        Apply a finished sale: given {item: quantity}, deduct the items from
        inventory, add them to the running sales totals, and return the total
        cost. Doesn't use input(), so it's safe to call from a GUI too.
        """
        total_cost = 0
        for item, quantity in cart.items():
            self.inventory[item] = self.inventory.get(item, 0) - quantity
            self.sales[item] = self.sales.get(item, 0) + quantity
            total_cost += quantity * self.prices[item]
        return total_cost

    # ------------------------------------------------------------------
    # Resupplying: add stock back to an item (e.g. after a delivery)
    # ------------------------------------------------------------------
    def restock(self, item, quantity):
        """Add `quantity` units of `item` back into inventory. Returns the new stock level."""
        if item not in self.inventory:
            raise ValueError(f"'{item}' is not on the menu.")
        if quantity <= 0:
            raise ValueError("Restock quantity must be a positive number.")

        self.inventory[item] += quantity
        return self.inventory[item]

    # ------------------------------------------------------------------
    # Saving / loading: persist this restaurant's data to a JSON file so
    # it can be picked back up the next time the program runs.
    # ------------------------------------------------------------------
    def to_dict(self):
        """Package this restaurant's data as a plain dict (JSON-friendly)."""
        return {
            "name": self.name,
            "menu": self.menu,
            "prices": self.prices,
            "sales": self.sales,
            "inventory": self.inventory,
        }

    def save(self, filepath="restaurant_data.json"):
        """Write this restaurant's data to a JSON file."""
        with open(filepath, "w") as save_file:
            json.dump(self.to_dict(), save_file, indent=2)

    @classmethod
    def load(cls, filepath="restaurant_data.json"):
        """
        Load a previously-saved restaurant from a JSON file.
        Returns None (instead of raising) if no save file exists yet,
        so callers can fall back to creating a new restaurant.
        """
        if not os.path.exists(filepath):
            return None

        with open(filepath) as save_file:
            data = json.load(save_file)

        return cls(data["name"], data["menu"], data["prices"], data["sales"], data["inventory"])
