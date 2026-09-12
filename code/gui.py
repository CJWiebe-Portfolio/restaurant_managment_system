"""
gui.py
======
A Tkinter desktop UI for the Restaurant Management System.

This reuses the same `Restaurant` and `Report` classes that main.py
(the console version) uses -- it just replaces input()/print() with
windows, buttons, and forms.

Run it directly:
    python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from restaurant import Restaurant
from final_report import Report

SAVE_FILE = "restaurant_data.json"


# ==========================================================================
# Screen 1: Setup -- enter the restaurant name and build the menu
# ==========================================================================
class SetupFrame(ttk.Frame):
    """
    Collects the restaurant's name and its menu (item name, price,
    starting stock for each item). When "Open Restaurant" is clicked,
    builds a Restaurant object and hands it to `on_done`.
    """

    def __init__(self, master, on_done):
        super().__init__(master, padding=15)
        self.on_done = on_done
        self.rows = []  # each entry: (item_entry, price_entry, stock_entry)

        ttk.Label(self, text="New Restaurant Setup", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 10), sticky="w"
        )

        ttk.Label(self, text="Restaurant name:").grid(row=1, column=0, sticky="w")
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.grid(row=1, column=1, columnspan=2, sticky="we", pady=5)

        ttk.Label(self, text="Menu item").grid(row=2, column=0)
        ttk.Label(self, text="Price ($)").grid(row=2, column=1)
        ttk.Label(self, text="Starting stock").grid(row=2, column=2)

        self.rows_frame = ttk.Frame(self)
        self.rows_frame.grid(row=3, column=0, columnspan=3, sticky="we")

        self.add_row()  # start with one blank row to fill in

        button_bar = ttk.Frame(self)
        button_bar.grid(row=4, column=0, columnspan=3, pady=10, sticky="we")
        ttk.Button(button_bar, text="+ Add item", command=self.add_row).pack(side="left")
        ttk.Button(button_bar, text="Open Restaurant", command=self.finish).pack(side="right")

        # If a save file exists, offer to load it instead of filling out the form again
        saved = Restaurant.load(SAVE_FILE)
        if saved is not None:
            ttk.Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=3, sticky="we", pady=10)
            ttk.Button(
                self,
                text=f"Load Saved Restaurant ('{saved.name}')",
                command=lambda: self.on_done(saved),
            ).grid(row=6, column=0, columnspan=3, sticky="we")

    def add_row(self):
        """Add one blank (item, price, stock) row to the menu-builder form."""
        r = len(self.rows)
        item_entry = ttk.Entry(self.rows_frame, width=18)
        price_entry = ttk.Entry(self.rows_frame, width=10)
        stock_entry = ttk.Entry(self.rows_frame, width=10)
        item_entry.grid(row=r, column=0, padx=2, pady=2)
        price_entry.grid(row=r, column=1, padx=2, pady=2)
        stock_entry.grid(row=r, column=2, padx=2, pady=2)
        self.rows.append((item_entry, price_entry, stock_entry))

    def finish(self):
        """Validate the form, build the menu/prices/sales/inventory dicts, and launch the main app."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Missing name", "Enter a restaurant name.")
            return

        menu, prices, inventory, sales = {}, {}, {}, {}
        for item_entry, price_entry, stock_entry in self.rows:
            item = item_entry.get().strip()
            if not item:
                continue  # skip blank rows

            try:
                price = float(price_entry.get())
                stock = int(stock_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", f"Enter a valid price and stock number for '{item}'.")
                return

            menu[item] = None
            prices[item] = price
            inventory[item] = stock
            sales[item] = 0

        if not menu:
            messagebox.showerror("Empty menu", "Add at least one menu item.")
            return

        restaurant = Restaurant(name, menu, prices, sales, inventory)
        self.on_done(restaurant)


# ==========================================================================
# Screen 2: Main app -- browse the menu, take orders, restock, view reports
# ==========================================================================
class RestaurantApp(ttk.Frame):
    """The main window: a live menu table, an order/checkout panel, and a restock panel."""

    def __init__(self, master, restaurant):
        super().__init__(master, padding=15)
        self.master = master
        self.restaurant = restaurant
        self.cart = {}  # {item: quantity} currently in the customer's cart

        master.title(f"{restaurant.name} -- Restaurant Manager")

        ttk.Label(self, text=restaurant.name, font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        # --- Menu table: item / price / stock / sold so far ---
        columns = ("item", "price", "stock", "sold")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        for col, label in zip(columns, ("Item", "Price", "In Stock", "Sold")):
            self.tree.heading(col, text=label)
            self.tree.column(col, width=100, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=2, sticky="we", pady=10)

        # --- Order panel ---
        order_box = ttk.LabelFrame(self, text="Take an Order", padding=10)
        order_box.grid(row=2, column=0, sticky="nswe", padx=(0, 10))

        ttk.Label(order_box, text="Item:").grid(row=0, column=0, sticky="w")
        self.order_item = ttk.Combobox(order_box, values=list(restaurant.menu), state="readonly", width=15)
        self.order_item.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(order_box, text="Qty:").grid(row=1, column=0, sticky="w")
        self.order_qty = ttk.Spinbox(order_box, from_=1, to=999, width=5)
        self.order_qty.set(1)
        self.order_qty.grid(row=1, column=1, padx=5, pady=2)

        ttk.Button(order_box, text="Add to Cart", command=self.add_to_cart).grid(
            row=2, column=0, columnspan=2, pady=5
        )

        self.cart_list = tk.Listbox(order_box, height=5, width=28)
        self.cart_list.grid(row=3, column=0, columnspan=2, pady=5)

        self.total_label = ttk.Label(order_box, text="Total: $0.00")
        self.total_label.grid(row=4, column=0, columnspan=2)

        ttk.Button(order_box, text="Checkout", command=self.checkout).grid(
            row=5, column=0, columnspan=2, pady=5
        )

        # --- Restock (resupplying) panel ---
        restock_box = ttk.LabelFrame(self, text="Resupply Inventory", padding=10)
        restock_box.grid(row=2, column=1, sticky="nswe")

        ttk.Label(restock_box, text="Item:").grid(row=0, column=0, sticky="w")
        self.restock_item = ttk.Combobox(restock_box, values=list(restaurant.menu), state="readonly", width=15)
        self.restock_item.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(restock_box, text="Qty:").grid(row=1, column=0, sticky="w")
        self.restock_qty = ttk.Spinbox(restock_box, from_=1, to=999, width=5)
        self.restock_qty.set(1)
        self.restock_qty.grid(row=1, column=1, padx=5, pady=2)

        ttk.Button(restock_box, text="Restock", command=self.restock).grid(
            row=2, column=0, columnspan=2, pady=5
        )

        # --- Report / Save ---
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(bottom_bar, text="View Daily Report", command=self.show_report).pack(side="left", padx=5)
        ttk.Button(bottom_bar, text="Save", command=self.save).pack(side="left", padx=5)

        # Save automatically (after asking) when the window is closed
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.refresh_menu_table()

    # ----------------------------------------------------------------
    def refresh_menu_table(self):
        """Redraw the menu table from the restaurant's current data."""
        self.tree.delete(*self.tree.get_children())
        for item in self.restaurant.menu:
            self.tree.insert(
                "",
                "end",
                values=(
                    item,
                    f"${self.restaurant.prices[item]:.2f}",
                    self.restaurant.inventory[item],
                    self.restaurant.sales[item],
                ),
            )

    def add_to_cart(self):
        """Add the selected item/quantity to the cart, checking against remaining stock."""
        item = self.order_item.get()
        if not item:
            messagebox.showerror("No item selected", "Choose a menu item first.")
            return

        try:
            qty = int(self.order_qty.get())
        except ValueError:
            messagebox.showerror("Invalid quantity", "Enter a whole number.")
            return

        if qty <= 0:
            messagebox.showerror("Invalid quantity", "Quantity must be positive.")
            return

        already_in_cart = self.cart.get(item, 0)
        if already_in_cart + qty > self.restaurant.inventory[item]:
            available = self.restaurant.inventory[item] - already_in_cart
            messagebox.showerror("Not enough stock", f"Only {available} more {item} available.")
            return

        self.cart[item] = already_in_cart + qty
        self.refresh_cart()

    def refresh_cart(self):
        """Redraw the cart listbox and running total from self.cart."""
        self.cart_list.delete(0, "end")
        total = 0
        for item, qty in self.cart.items():
            line_total = qty * self.restaurant.prices[item]
            total += line_total
            self.cart_list.insert("end", f"{item} x{qty} = ${line_total:.2f}")
        self.total_label.config(text=f"Total: ${total:.2f}")

    def checkout(self):
        """Finalize the sale: apply the cart via Restaurant.sell(), then clear it."""
        if not self.cart:
            messagebox.showinfo("Empty cart", "Add items to the cart before checking out.")
            return

        total_cost = self.restaurant.sell(self.cart)

        messagebox.showinfo(
            "Order complete",
            f"Charged ${total_cost:.2f} for:\n" + "\n".join(f"{item} x{qty}" for item, qty in self.cart.items()),
        )

        self.cart = {}
        self.refresh_cart()
        self.refresh_menu_table()

    def restock(self):
        """Add stock back to the selected item via Restaurant.restock()."""
        item = self.restock_item.get()
        if not item:
            messagebox.showerror("No item selected", "Choose a menu item first.")
            return

        try:
            qty = int(self.restock_qty.get())
        except ValueError:
            messagebox.showerror("Invalid quantity", "Enter a whole number.")
            return

        try:
            new_stock = self.restaurant.restock(item, qty)
        except ValueError as error:
            messagebox.showerror("Restock failed", str(error))
            return

        self.refresh_menu_table()
        messagebox.showinfo("Restocked", f"{item} restocked to {new_stock} units.")

    def save(self):
        """Write the restaurant's current data to the save file."""
        self.restaurant.save(SAVE_FILE)
        messagebox.showinfo("Saved", f"'{self.restaurant.name}' saved to {SAVE_FILE}.")

    def on_close(self):
        """Ask to save before closing the window."""
        if messagebox.askyesno("Save before closing?", "Save this restaurant's data before quitting?"):
            self.restaurant.save(SAVE_FILE)
        self.master.destroy()

    def show_report(self):
        """Open a window showing the daily report (revenue per item, total, best seller)."""
        report = Report(
            self.restaurant.name,
            self.restaurant.menu,
            self.restaurant.prices,
            self.restaurant.sales,
            self.restaurant.inventory,
        )

        report_window = tk.Toplevel(self)
        report_window.title("Daily Report")

        text = tk.Text(report_window, width=50, height=15, padx=10, pady=10)
        text.insert("1.0", report.report_text())
        text.config(state="disabled")
        text.pack()


# ==========================================================================
# Entry point
# ==========================================================================
def main():
    root = tk.Tk()
    root.title("New Restaurant -- Setup")

    def launch_app(restaurant):
        """Swap the setup screen out for the main app once setup is complete."""
        for widget in root.winfo_children():
            widget.destroy()
        RestaurantApp(root, restaurant).pack(fill="both", expand=True)

    SetupFrame(root, on_done=launch_app).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
