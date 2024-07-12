import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk

# Define the expense limits and corresponding tags
LIMITS = [
    (100, "#8b0000"),    # Dark red for expenses over $100
    (50, "#808000"),     # Olive for expenses between $50 and $100
    (20, "#556b2f"),     # Dark olive green for expenses between $20 and $50
]

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if date and category and amount:
        try:
            month, day, year = map(int, date.split('-'))
            formatted_date = f"{month:02d}-{day:02d}-{year}"
            float(amount)
        except ValueError:
            status_label.config(text="Please enter a valid date or amount!", fg="red")
            return

        with open("expenses.txt", "a") as file:
            file.write(f"{formatted_date},{category},{amount}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        display_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def get_tag_for_amount(amount):
    for limit, color in LIMITS:
        if amount > limit:
            return color
    return ""

def display_expenses():
    global expenses_tree
    if os.path.exists("expenses.txt"):
        total_expense = 0
        expenses_tree.delete(*expenses_tree.get_children())
        with open("expenses.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split(",")
                    if len(parts) == 3:  # Ensure the line has exactly three values
                        date, category, amount = parts
                        amount = float(amount)
                        total_expense += amount
                        tag = get_tag_for_amount(amount)
                        expenses_tree.insert("", tk.END, values=(date, category, amount), tags=(tag,))
        total_label.config(text=f"Total Expense: ${total_expense:.2f}")
    else:
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())

def open_expenses_file():
    if os.path.exists("expenses.txt"):
        current_os = platform.system()
        if current_os == "Windows":
            os.system(f'start "" "expenses.txt"')
        elif current_os == "Darwin":  # macOS
            os.system(f'open "expenses.txt"')
        elif current_os == "Linux":
            os.system(f'xdg-open "expenses.txt"')

def close_program():
    root.destroy()

def adjust_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text

        # Create a new window for adjustment
        adjust_window = tk.Toplevel(root)
        adjust_window.title("Adjust Expense")

        tk.Label(adjust_window, text="Date (MM-DD-YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        adjust_date_entry = tk.Entry(adjust_window)
        adjust_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        adjust_date_entry.insert(0, date)

        tk.Label(adjust_window, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        adjust_category_entry = tk.Entry(adjust_window)
        adjust_category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        adjust_category_entry.insert(0, category)

        tk.Label(adjust_window, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        adjust_amount_entry = tk.Entry(adjust_window)
        adjust_amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        adjust_amount_entry.insert(0, amount)

        def save_adjustment():
            new_date = adjust_date_entry.get()
            new_category = adjust_category_entry.get()
            new_amount = adjust_amount_entry.get()

            if new_date and new_category and new_amount:
                try:
                    month, day, year = map(int, new_date.split('-'))
                    formatted_new_date = f"{month:02d}-{day:02d}-{year}"
                    float(new_amount)
                except ValueError:
                    adjust_status_label.config(text="Please enter a valid date or amount!", fg="red")
                    return

                # Update file
                with open("expenses.txt", "r") as file:
                    lines = file.readlines()
                with open("expenses.txt", "w") as file:
                    for line in lines:
                        if line.strip() == f"{date},{category},{amount}":
                            file.write(f"{formatted_new_date},{new_category},{new_amount}\n")
                        else:
                            file.write(line)

                status_label.config(text="Expense adjusted successfully!", fg="green")
                adjust_window.destroy()
                restart_program()  # Restart the program after adjustment
            else:
                adjust_status_label.config(text="Please fill all the fields!", fg="red")

        save_button = tk.Button(adjust_window, text="Save Adjustment", command=save_adjustment)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        adjust_status_label = tk.Label(adjust_window, text="", fg="green")
        adjust_status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    else:
        status_label.config(text="Please select an expense to adjust!", fg="red")

def restart_program():
    root.destroy()
    python = sys.executable
    subprocess.call([python, os.path.realpath(__file__)])


# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (MM-DD-YYYY):")
date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Define tags for different expense limits
for limit, color in LIMITS:
    expenses_tree.tag_configure(color, background=color)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Create a label to show the status of expense addition and adjustment
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Create buttons to view, adjust expenses, and close the program
view_button = tk.Button(root, text="View Expenses", command=open_expenses_file)
view_button.grid(row=7, column=0, padx=5, pady=10)

adjust_button = tk.Button(root, text="Adjust Expense", command=adjust_expense)
adjust_button.grid(row=7, column=1, padx=5, pady=10)

close_button = tk.Button(root, text="Close", command=close_program)
close_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass
# Display existing expenses on application start
display_expenses()

root.mainloop()
              
