"""
main.py
=======
Entry point for the Restaurant Management System.

On startup, loads a previously-saved restaurant if one exists (asking
first), otherwise walks the user through setting up a new one. Lets
customers place orders, saves progress when done, and prints a daily
report.
"""

from create_restaurant import Create
from restaurant import Restaurant
from final_report import Report

SAVE_FILE = "restaurant_data.json"

# ----------------------------------------------------------------------
# Step 1: load a saved restaurant if one exists, otherwise set up a new one
# ----------------------------------------------------------------------
my_restaurant = Restaurant.load(SAVE_FILE)

if my_restaurant is not None:
    load_it = input(f"Found a saved restaurant, '{my_restaurant.name}'. Load it? (y/n) ")
    if load_it != "y":
        my_restaurant = None

if my_restaurant is None:
    creator = Create()
    name = creator.create_name()                # restaurant's name
    menu = creator.create_menu()                 # dict of {item_name: None} -- the set of items sold
    prices = creator.create_prices(menu)         # dict of {item_name: price}
    sales = creator.create_sales(menu)           # dict of {item_name: units sold}, starts at 0
    inventory = creator.create_inventory(menu)   # dict of {item_name: units in stock}
    my_restaurant = Restaurant(name, menu, prices, sales, inventory)

# ----------------------------------------------------------------------
# Step 2: run the restaurant and take customer orders
# ----------------------------------------------------------------------
my_restaurant.taking_an_order()

# ----------------------------------------------------------------------
# Step 3: save progress so it's there next time the program runs
# ----------------------------------------------------------------------
my_restaurant.save(SAVE_FILE)
print(f"Saved '{my_restaurant.name}' to {SAVE_FILE}.")

# ----------------------------------------------------------------------
# Step 4: print the daily report
# ----------------------------------------------------------------------
my_report = Report(my_restaurant.name, my_restaurant.menu, my_restaurant.prices,
                    my_restaurant.sales, my_restaurant.inventory)
my_report.print_daily_report()
