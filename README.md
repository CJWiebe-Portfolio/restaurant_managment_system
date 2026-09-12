# Restaurant Management System

A small restaurant management app written in Python. Set up a restaurant
(name, menu, prices, starting inventory), take customer orders, resupply
inventory, and print a daily sales report -- with your progress saved
between runs.

Available two ways:
- **`gui.py`** -- a Tkinter desktop app (recommended)
- **`main.py`** -- a text/console version

## Features

- Build a restaurant from scratch: name, menu items, prices, starting stock
- Take customer orders through a running shopping cart and checkout flow
- Resupply (restock) inventory at any time
- Daily report: revenue per item, total revenue, and the best-selling item
- Save/load: progress is written to `restaurant_data.json` and reloaded
  automatically the next time the program runs

## Running it

Requires Python 3.10+ (no extra packages needed -- everything used is
in the standard library).

```bash
python gui.py    # desktop app
python main.py   # console version
```

## Project structure

| File | Purpose |
|---|---|
| `create_restaurant.py` | `Create` -- collects name/menu/prices/sales/inventory from user input (console setup) |
| `restaurant.py` | `Restaurant` -- menu, prices, sales, inventory, ordering logic, restocking, save/load |
| `final_report.py` | `Report` -- builds and prints/returns the daily sales report |
| `gui.py` | Tkinter desktop UI |
| `main.py` | Console entry point |

## Building a standalone .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name RestaurantManager gui.py
```

The finished app will be at `dist/RestaurantManager.exe` -- no Python
install required to run it.

## Credits

Built by C.J. Wiebe.
