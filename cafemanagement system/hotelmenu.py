# in this project we use dictionarry datatype and conditional statements
import re
from datetime import datetime
import csv
menu = {
    'coffee': 40,
    'tea': 30,
    'orange juice': 50,
    'sandwich': 100,
    'burger': 150,
    'pasta': 120,
    'salad': 80,
    'pizza': 180,
    'soda': 25,
    'water': 15,
    'cake': 90,
    'ice cream': 70,
    'fruit bowl': 60,
    'smoothie': 110,
    'steak': 200,
    'noodles': 130,
    'fried rice': 140,
    'chocolate shake': 95,
    'oreoshake': 85,
    'Biryani': 75,
    'Lassi': 55,
    'Momos': 45,
    'Samosa': 25,
    'Chaat': 35,
    'Dosa': 85,
    'Idli': 40,
    'Vada': 50,
    'Pani Puri': 30,
    'Jalebi&rabdi': 65,
}


# greet
print("Welcome to our desi cafe!")
print("Here is our menu:")
for name, price in menu.items():
    print(f"{name}: Rs{price}")


# Order state
order_total = 0
ordered_items = []  # list of (name, qty, unit_price)


def add_item(name, qty=1):
    """Add item to order, parsing optional quantity from name if needed."""
    global order_total
    # parse quantity from input: "Dosa x2", "tea:3", "pizza 2"
    m = re.match(r"^(.*?)(?:\s*[xX]\s*(\d+)|\s*:\s*(\d+)|\s+(\d+))?\s*$", name)
    if m:
        item_name = m.group(1).strip()
        qty_str = m.group(2) or m.group(3) or m.group(4)
        qty = int(qty_str) if qty_str else qty
    else:
        item_name = name.strip()

    key = item_name.lower()
    # Check if item exists (case-insensitive)
    menu_key = None
    for menu_name in menu:
        if menu_name.lower() == key:
            menu_key = menu_name
            break

    if menu_key:
        unit = menu[menu_key]
        order_total += unit * qty
        ordered_items.append((menu_key, qty, unit))
        print(f"Added {menu_key} x{qty}. Current total: Rs{order_total}")
    else:
        print(f"Sorry, we don't have '{item_name}' on the menu.")


def save_order_csv(path='orders.csv'):
    # append order: timestamp, items (name x qty; ...), total
    items_str = '; '.join([f"{n} x{q}" for n, q, u in ordered_items])
    now = datetime.now().isoformat(sep=' ', timespec='seconds')
    header = ['timestamp', 'items', 'total']
    write_header = False
    try:
        with open(path, 'r', newline='', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        write_header = True
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([now, items_str, order_total])


# accept comma-separated names on first ask
first_input = input(
    "Please enter the name(s) of item(s) you would like to order (separate multiple items with commas):  ")
for part in [p.strip() for p in first_input.split(',') if p.strip()]:
    add_item(part)

another_order = input(
    "Would you like to order another item? (yes/no): ").strip().lower()
if another_order == 'yes':
    more = input(
        "Please enter the name(s) of the next item(s) you would like to order (comma-separated):  ")
    for part in [p.strip() for p in more.split(',') if p.strip()]:
        add_item(part)

if ordered_items:
    print("Thank you for your order! Here is your summary:")
    for n, q, u in ordered_items:
        print(f"- {n} x{q} @ Rs{u} = Rs{u*q}")
    print(f"Your total is Rs{order_total}. Please proceed to payment.")
    save_order_csv()
    print("Order saved to orders.csv")
else:
    print("No valid items ordered.")
