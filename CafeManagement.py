import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from datetime import datetime

# File paths for storing data
FOODS_FILE = "foods.json"
ORDERS_FILE = "orders.json"

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class CafeManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cafe Management System")
        self.geometry("1000x700")
        self.minsize(900, 650)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure(bg="#f9f9fb")

        # Color palette for modern look
        self.primary_color = "#6a1b9a"  # deep purple
        self.secondary_color = "#ffffff"  # white
        self.bg_color = "#f9f9fb"
        self.text_color = "#222222"
        self.accent_color = "#ab47bc"  # lighter purple

        self.setup_styles()

        self.foods = load_data(FOODS_FILE)
        self.orders = load_data(ORDERS_FILE)

        self.cart_items = {}  # Initialize cart_items here
        self.create_widgets()

    def setup_styles(self):
        s = self.style
        s.configure("TButton", padding=6, font=("Poppins", 11), background=self.primary_color, foreground="white")
        s.map("TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', self.accent_color), ('active', self.accent_color)])

        s.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Poppins", 11))
        s.configure("Header.TLabel", font=("Poppins", 20, "bold"), foreground=self.primary_color, background=self.bg_color)
        s.configure("SubHeader.TLabel", font=("Poppins", 14, "bold"), foreground=self.primary_color, background=self.bg_color)
        s.configure("Card.TFrame", background=self.secondary_color, relief="raised", borderwidth=1)
        s.configure("Treeview.Heading", font=("Poppins", 11, "bold"), foreground=self.primary_color, background=self.secondary_color)
        s.configure("Treeview", font=("Poppins", 10), background=self.secondary_color, foreground=self.text_color, fieldbackground=self.secondary_color, bordercolor=self.secondary_color)
        s.configure("TEntry", padding=5)

    def create_widgets(self):
        # Create Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Tabs:
        self.tab_add_food = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_take_order = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_dashboard = ttk.Frame(self.notebook, style="Card.TFrame")

        self.notebook.add(self.tab_add_food, text="Add Food Items")
        self.notebook.add(self.tab_take_order, text="Sell Food / Invoice")
        self.notebook.add(self.tab_dashboard, text="Dashboard")

        self.create_add_food_tab()
        self.create_take_order_tab()
        self.create_dashboard_tab()

    def create_add_food_tab(self):
        frame = self.tab_add_food

        header = ttk.Label(frame, text="Add New Food Item", style="Header.TLabel")
        header.pack(pady=(20, 10), anchor="center")

        form_frame = ttk.Frame(frame)
        form_frame.pack(padx=30, pady=(0,10), fill="x")

        # Food Name
        lbl_name = ttk.Label(form_frame, text="Food Name:")
        lbl_name.grid(row=0, column=0, sticky="w", pady=12)

        self.food_name_var = tk.StringVar()
        ent_name = ttk.Entry(form_frame, textvariable=self.food_name_var, font=("Poppins", 12))
        ent_name.grid(row=0, column=1, sticky="ew", pady=12, padx=(12,0))

        # Price
        lbl_price = ttk.Label(form_frame, text="Price ($):")
        lbl_price.grid(row=1, column=0, sticky="w", pady=12)

        self.food_price_var = tk.StringVar()
        ent_price = ttk.Entry(form_frame, textvariable=self.food_price_var, font=("Poppins", 12))
        ent_price.grid(row=1, column=1, sticky="ew", pady=12, padx=(12,0))

        form_frame.columnconfigure(1, weight=1)

        # Buttons Frame
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=(0, 15))

        add_btn = ttk.Button(buttons_frame, text="Add Food", command=self.add_food_item)
        add_btn.grid(row=0, column=0, padx=6)

        self.modify_btn = ttk.Button(buttons_frame, text="Modify Selected", command=self.modify_food_item, state="disabled")
        self.modify_btn.grid(row=0, column=1, padx=6)

        self.delete_btn = ttk.Button(buttons_frame, text="Delete Selected", command=self.delete_food_item, state="disabled")
        self.delete_btn.grid(row=0, column=2, padx=6)

        # Food list below for reference
        lbl_list = ttk.Label(frame, text="Existing Food Items:", style="SubHeader.TLabel")
        lbl_list.pack(pady=(10,5), anchor="w")

        self.tree_foods = ttk.Treeview(frame, columns=("Name", "Price"), show="headings", selectmode="browse", height=12)
        self.tree_foods.heading("Name", text="Food Name")
        self.tree_foods.heading("Price", text="Price ($)")
        self.tree_foods.column("Name", width=300, anchor="w")
        self.tree_foods.column("Price", width=100, anchor="center")
        self.tree_foods.pack(fill="both", expand=True, padx=30, pady=(0,15))

        self.tree_foods.bind("<<TreeviewSelect>>", self.on_food_select)

        self.refresh_food_list()

    def on_food_select(self, event):
        selected = self.tree_foods.selection()
        if selected:
            self.modify_btn.config(state="normal")
            self.delete_btn.config(state="normal")
            food_id = int(selected[0])
            food = next((f for f in self.foods if f["id"] == food_id), None)
            if food:
                self.food_name_var.set(food["name"])
                self.food_price_var.set(f"{food['price']:.2f}")
        else:
            self.modify_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
            self.food_name_var.set("")
            self.food_price_var.set("")

    def add_food_item(self):
        name = self.food_name_var.get().strip()
        price_str = self.food_price_var.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Food name cannot be empty.")
            return
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid positive price.")
            return

        # Check if food already exists (case insensitive)
        if any(f["name"].lower() == name.lower() for f in self.foods):
            messagebox.showwarning("Duplicate Entry", "This food item already exists.")
            return

        new_food = {
            "id": (max([f["id"] for f in self.foods]) + 1) if self.foods else 1,
            "name": name,
            "price": price
        }
        self.foods.append(new_food)
        save_data(FOODS_FILE, self.foods)

        self.food_name_var.set("")
        self.food_price_var.set("")

        self.refresh_food_list()
        self.refresh_order_foods()
        self.refresh_dashboard_foods()

        messagebox.showinfo("Success", f"Food item '{name}' added successfully!")

        self.modify_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")

    def modify_food_item(self):
        selected = self.tree_foods.selection()
        if not selected:
            messagebox.showwarning("Modify Food", "Select a food item to modify.")
            return
        food_id = int(selected[0])
        name = self.food_name_var.get().strip()
        price_str = self.food_price_var.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Food name cannot be empty.")
            return
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid positive price.")
            return

        # Check for name collision with other items
        for food in self.foods:
            if food["id"] != food_id and food["name"].lower() == name.lower():
                messagebox.showwarning("Duplicate Entry", "Another food item with the same name exists.")
                return

        for food in self.foods:
            if food["id"] == food_id:
                food["name"] = name
                food["price"] = price
                break

        save_data(FOODS_FILE, self.foods)

        self.food_name_var.set("")
        self.food_price_var.set("")

        self.refresh_food_list()
        self.refresh_order_foods()
        self.refresh_dashboard_foods()

        messagebox.showinfo("Success", f"Food item ID {food_id} modified successfully!")

        self.modify_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        self.tree_foods.selection_remove(selected)

    def delete_food_item(self):
        selected = self.tree_foods.selection()
        if not selected:
            messagebox.showwarning("Delete Food", "Select a food item to delete.")
            return
        food_id = int(selected[0])
        food = next((f for f in self.foods if f["id"] == food_id), None)
        if not food:
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{food['name']}'?")
        if not confirm:
            return

        self.foods = [f for f in self.foods if f["id"] != food_id]
        save_data(FOODS_FILE, self.foods)

        # Remove from cart if present (in case food deleted while selling)
        if food_id in self.cart_items:
            del self.cart_items[food_id]
            self.refresh_cart()
            self.update_total_price()

        self.food_name_var.set("")
        self.food_price_var.set("")

        self.refresh_food_list()
        self.refresh_order_foods()
        self.refresh_dashboard_foods()

        messagebox.showinfo("Deleted", f"Food item '{food['name']}' deleted successfully!")

        self.modify_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        self.tree_foods.selection_remove(selected)

    def refresh_food_list(self):
        self.tree_foods.delete(*self.tree_foods.get_children())
        for food in self.foods:
            self.tree_foods.insert("", "end", iid=food["id"], values=(food["name"], f"{food['price']:.2f}"))

    def create_take_order_tab(self):
        frame = self.tab_take_order

        header = ttk.Label(frame, text="Sell Food & Generate Invoice", style="Header.TLabel")
        header.pack(pady=(20, 10))

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Food selection
        left_frame = ttk.Frame(content_frame, style="Card.TFrame")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

        lbl_foods = ttk.Label(left_frame, text="Available Food Items", style="SubHeader.TLabel")
        lbl_foods.pack(pady=10)

        # Treeview with columns: Food name, price, quantity selector
        self.tree_order_foods = ttk.Treeview(left_frame, columns=("Name", "Price", "Quantity"), show="headings", selectmode="browse")
        self.tree_order_foods.heading("Name", text="Food Name")
        self.tree_order_foods.heading("Price", text="Price ($)")
        self.tree_order_foods.heading("Quantity", text="Quantity")
        self.tree_order_foods.column("Name", width=220, anchor="w")
        self.tree_order_foods.column("Price", width=80, anchor="center")
        self.tree_order_foods.column("Quantity", width=90, anchor="center")
        self.tree_order_foods.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_order_foods.bind("<Double-1>", self.handle_add_quantity)

        lbl_instruction = ttk.Label(left_frame, 
                                    text="* Double-click item to add quantity",
                                    font=("Poppins", 9, "italic"),
                                    foreground="#666666")
        lbl_instruction.pack(pady=(0,10))

        self.refresh_order_foods()

        # Middle: Cart items and controls
        mid_frame = ttk.Frame(content_frame, style="Card.TFrame")
        mid_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        lbl_cart = ttk.Label(mid_frame, text="Order Cart", style="SubHeader.TLabel")
        lbl_cart.pack(pady=10)

        self.tree_cart = ttk.Treeview(mid_frame, columns=("Name", "Unit Price", "Quantity", "Total"), show="headings", selectmode="browse")
        self.tree_cart.heading("Name", text="Food Name")
        self.tree_cart.heading("Unit Price", text="Unit Price ($)")
        self.tree_cart.heading("Quantity", text="Quantity")
        self.tree_cart.heading("Total", text="Total ($)")
        self.tree_cart.column("Name", width=200, anchor="w")
        self.tree_cart.column("Unit Price", width=90, anchor="center")
        self.tree_cart.column("Quantity", width=80, anchor="center")
        self.tree_cart.column("Total", width=90, anchor="center")
        self.tree_cart.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_cart.bind("<Delete>", self.remove_cart_item)
        self.tree_cart.bind("<BackSpace>", self.remove_cart_item)

        # Buttons under cart
        cart_btn_frame = ttk.Frame(mid_frame)
        cart_btn_frame.pack(pady=(0,10))

        btn_remove = ttk.Button(cart_btn_frame, text="Remove Selected Item", command=self.remove_cart_item)
        btn_remove.pack(side="left", padx=10)

        btn_clear = ttk.Button(cart_btn_frame, text="Clear Cart", command=self.clear_cart)
        btn_clear.pack(side="left", padx=10)

        # Right: Customer info and invoice generation
        right_frame = ttk.Frame(content_frame, style="Card.TFrame")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        lbl_customer = ttk.Label(right_frame, text="Customer Information", style="SubHeader.TLabel")
        lbl_customer.pack(pady=10)

        customer_frame = ttk.Frame(right_frame)
        customer_frame.pack(padx=20, pady=10, fill="x")

        # Customer Name
        lbl_cust_name = ttk.Label(customer_frame, text="Name:")
        lbl_cust_name.grid(row=0, column=0, sticky="w", pady=12)

        self.cust_name_var = tk.StringVar()
        ent_cust_name = ttk.Entry(customer_frame, textvariable=self.cust_name_var, font=("Poppins", 12))
        ent_cust_name.grid(row=0, column=1, sticky="ew", pady=12, padx=(12,0))

        # Customer Phone
        lbl_cust_phone = ttk.Label(customer_frame, text="Phone:")
        lbl_cust_phone.grid(row=1, column=0, sticky="w", pady=12)

        self.cust_phone_var = tk.StringVar()
        ent_cust_phone = ttk.Entry(customer_frame, textvariable=self.cust_phone_var, font=("Poppins", 12))
        ent_cust_phone.grid(row=1, column=1, sticky="ew", pady=12, padx=(12,0))

        customer_frame.columnconfigure(1, weight=1)

        # Total Order Price below customer info
        self.total_price_var = tk.StringVar(value="0.00")

        lbl_total = ttk.Label(right_frame, text="Total Price ($):", font=("Poppins", 13, "bold"))
        lbl_total.pack(pady=(20,0))

        lbl_total_value = ttk.Label(right_frame, textvariable=self.total_price_var, font=("Poppins", 24, "bold"), foreground=self.primary_color)
        lbl_total_value.pack(pady=(0,20))

        btn_invoice = ttk.Button(right_frame, text="Generate Invoice and Save Order", command=self.generate_invoice)
        btn_invoice.pack(pady=10)

        self.refresh_order_foods()

    def refresh_order_foods(self):
        # Reload the order foods listview
        self.tree_order_foods.delete(*self.tree_order_foods.get_children())
        for food in self.foods:
            qty = self.cart_items.get(food["id"], 0)
            self.tree_order_foods.insert(
                "", "end", iid=food["id"], values=(
                    food["name"],
                    f"{food['price']:.2f}",
                    str(qty)  # Use quantity from cart
            ))

    def handle_add_quantity(self, event):
        item_id = self.tree_order_foods.focus()
        if not item_id:
            return
        food = next((f for f in self.foods if str(f["id"]) == item_id), None)
        if not food:
            return
        # Ask user for quantity (default 1)
        qty = simpledialog.askinteger("Add Quantity",
                                      f"Enter quantity for '{food['name']}':",
                                      initialvalue=1,
                                      minvalue=1,
                                      parent=self)
        if qty is None:
            return

        # Add or update quantity in cart
        food_id = food["id"]
        self.cart_items[food_id] = self.cart_items.get(food_id, 0) + qty

        self.refresh_cart()
        self.update_total_price()

        # Update quantity shown in left treeview for the item
        self.tree_order_foods.set(item_id, "Quantity", str(self.cart_items.get(food_id, 0)))

    def refresh_cart(self):
        self.tree_cart.delete(*self.tree_cart.get_children())
        for fid, qty in self.cart_items.items():
            food = next((f for f in self.foods if f["id"] == fid), None)
            if food:
                total = food["price"] * qty
                self.tree_cart.insert("", "end", iid=fid, values=(
                    food["name"],
                    f"{food['price']:.2f}",
                    str(qty),
                    f"{total:.2f}"
                ))

    def remove_cart_item(self, event=None):
        selected = self.tree_cart.focus()
        if not selected:
            messagebox.showwarning("Remove Item", "Select an item in the cart to remove.")
            return
        fid = int(selected)
        if fid in self.cart_items:
            del self.cart_items[fid]
        self.refresh_cart()
        self.update_total_price()
        # Reset quantity column in order foods list
        self.tree_order_foods.set(str(fid), "Quantity", "0")

    def clear_cart(self):
        if not self.cart_items:
            messagebox.showinfo("Clear Cart", "Cart is already empty.")
            return
        confirm = messagebox.askyesno("Clear Cart", "Are you sure you want to clear the entire cart?")
        if confirm:
            self.cart_items.clear()
            self.refresh_cart()
            self.update_total_price()
            for food in self.foods:
                self.tree_order_foods.set(str(food["id"]), "Quantity", "0")

    def update_total_price(self):
        total = 0.0
        for fid, qty in self.cart_items.items():
            food = next((f for f in self.foods if f["id"] == fid), None)
            if food:
                total += food["price"] * qty
        self.total_price_var.set(f"{total:.2f}")

    def generate_invoice(self):
        if not self.cart_items:
            messagebox.showwarning("Empty Cart", "Add some items to the cart before generating invoice.")
            return

        cust_name = self.cust_name_var.get().strip()
        cust_phone = self.cust_phone_var.get().strip()

        if not cust_name:
            messagebox.showerror("Customer Info", "Customer name is required.")
            return
        if not cust_phone or not cust_phone.isdigit():
            messagebox.showerror("Customer Info", "Valid customer phone number is required (digits only).")
            return

        total_price = float(self.total_price_var.get())

        # Create order object
        order_id = (max([o["id"] for o in self.orders]) + 1) if self.orders else 1
        order_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        items_detail = []
        for fid, qty in self.cart_items.items():
            food = next((f for f in self.foods if f["id"] == fid), None)
            if food:
                items_detail.append({
                    "food_id": fid,
                    "name": food["name"],
                    "unit_price": food["price"],
                    "quantity": qty,
                    "total": food["price"] * qty
                })

        order = {
            "id": order_id,
            "customer_name": cust_name,
            "customer_phone": cust_phone,
            "items": items_detail,
            "total": total_price,
            "datetime": order_datetime
        }

        self.orders.append(order)
        save_data(ORDERS_FILE, self.orders)

        # Show invoice modal with save invoice feature
        InvoiceWindow(self, order)

        # Reset cart and customer info
        self.cart_items.clear()
        self.cust_name_var.set("")
        self.cust_phone_var.set("")
        self.refresh_cart()
        self.update_total_price()
        for food in self.foods:
            self.tree_order_foods.set(str(food["id"]), "Quantity", "0")

        self.refresh_dashboard_orders()

    def create_dashboard_tab(self):
        frame = self.tab_dashboard

        header = ttk.Label(frame, text="Dashboard - Food Items and Orders", style="Header.TLabel")
        header.pack(pady=(20, 15))

        # Split top area into two frames side by side for foods & orders
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="both", expand=True, padx=20)

        # Food items panel
        food_panel = ttk.Frame(top_frame, style="Card.TFrame")
        food_panel.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        lbl_food = ttk.Label(food_panel, text="Food Items", style="SubHeader.TLabel")
        lbl_food.pack(pady=10)

        self.dashboard_foods_tree = ttk.Treeview(food_panel, columns=("Name", "Price"), show="headings")
        self.dashboard_foods_tree.heading("Name", text="Food Name")
        self.dashboard_foods_tree.heading("Price", text="Price ($)")
        self.dashboard_foods_tree.column("Name", width=250, anchor="w")
        self.dashboard_foods_tree.column("Price", width=100, anchor="center")
        self.dashboard_foods_tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Orders panel
        orders_panel = ttk.Frame(top_frame, style="Card.TFrame")
        orders_panel.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        lbl_orders = ttk.Label(orders_panel, text="Orders", style="SubHeader.TLabel")
        lbl_orders.pack(pady=10)

        self.dashboard_orders_tree = ttk.Treeview(orders_panel, columns=("ID", "Customer", "Phone", "Total", "DateTime"), show="headings")
        self.dashboard_orders_tree.heading("ID", text="Order ID")
        self.dashboard_orders_tree.heading("Customer", text="Customer Name")
        self.dashboard_orders_tree.heading("Phone", text="Phone")
        self.dashboard_orders_tree.heading("Total", text="Total ($)")
        self.dashboard_orders_tree.heading("DateTime", text="Date & Time")
        self.dashboard_orders_tree.column("ID", width=80, anchor="center")
        self.dashboard_orders_tree.column("Customer", width=180, anchor="w")
        self.dashboard_orders_tree.column("Phone", width=120, anchor="center")
        self.dashboard_orders_tree.column("Total", width=100, anchor="center")
        self.dashboard_orders_tree.column("DateTime", width=150, anchor="center")
        self.dashboard_orders_tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Order action buttons
        btn_frame = ttk.Frame(orders_panel)
        btn_frame.pack(pady=10)

        btn_view_order = ttk.Button(btn_frame, text="View Order Details", command=self.view_order_details)
        btn_view_order.grid(row=0, column=0, padx=6)

        btn_save_invoice = ttk.Button(btn_frame, text="Save Invoice", command=self.save_invoice_from_dashboard)
        btn_save_invoice.grid(row=0, column=1, padx=6)

        self.refresh_dashboard_foods()
        self.refresh_dashboard_orders()

    def refresh_dashboard_foods(self):
        self.dashboard_foods_tree.delete(*self.dashboard_foods_tree.get_children())
        for food in self.foods:
            self.dashboard_foods_tree.insert("", "end", values=(food["name"], f"{food['price']:.2f}"))

    def refresh_dashboard_orders(self):
        self.dashboard_orders_tree.delete(*self.dashboard_orders_tree.get_children())
        for order in self.orders:
            self.dashboard_orders_tree.insert("", "end", iid=order["id"], values=(
                order["id"],
                order["customer_name"],
                order["customer_phone"],
                f"{order['total']:.2f}",
                order["datetime"],
            ))

    def view_order_details(self):
        selected = self.dashboard_orders_tree.focus()
        if not selected:
            messagebox.showinfo("Order Details", "Select an order to view details.")
            return
        order_id = int(selected)
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if order:
            OrderDetailsWindow(self, order)
        else:
            messagebox.showerror("Error", "Selected order not found.")

    def save_invoice_from_dashboard(self):
        selected = self.dashboard_orders_tree.focus()
        if not selected:
            messagebox.showinfo("Save Invoice", "Select an order to save its invoice.")
            return
        order_id = int(selected)
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            messagebox.showerror("Error", "Selected order not found.")
            return

        # Generate invoice text content
        invoice_text = self.construct_invoice_text(order)

        # Ask for file save location
        default_filename = f"Invoice_Order_{order['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(title="Save Invoice As", defaultextension=".txt",
                                                 initialfile=default_filename,
                                                 filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(invoice_text)
            messagebox.showinfo("Success", f"Invoice saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save invoice:\n{e}")

    def construct_invoice_text(self, order):
        lines = []
        lines.append("Cafe Management System Invoice")
        lines.append("="*40)
        lines.append(f"Order ID: {order['id']}")
        lines.append(f"Date & Time: {order['datetime']}")
        lines.append(f"Customer Name: {order['customer_name']}")
        lines.append(f"Customer Phone: {order['customer_phone']}")
        lines.append("="*40)
        lines.append("Items:")
        lines.append(f"{'Name':20} {'Unit Price':>10} {'Qty':>6} {'Total':>10}")
        lines.append("-"*40)
        for item in order["items"]:
            name = (item["name"][:18] + '..') if len(item["name"]) > 20 else item["name"]
            lines.append(f"{name:20} ${item['unit_price']:>9.2f} {item['quantity']:>6} ${item['total']:>9.2f}")
        lines.append("="*40)
        lines.append(f"Total Amount: ${order['total']:.2f}")
        lines.append("="*40)
        lines.append("\nThank you for your purchase!\n")
        return "\n".join(lines)

class InvoiceWindow(tk.Toplevel):
    def __init__(self, parent, order):
        super().__init__(parent)
        self.title(f"Invoice - Order #{order['id']}")
        self.geometry("500x600")
        self.configure(bg="#f9f9fb")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("TLabel", font=("Poppins", 11), background="#f9f9fb", foreground="#222222")
        self.style.configure("Header.TLabel", font=("Poppins", 18, "bold"), foreground="#6a1b9a", background="#f9f9fb")

        header = ttk.Label(self, text="Invoice", style="Header.TLabel")
        header.pack(pady=(20, 10))

        # Invoice details text box (readonly)
        self.invoice_text = tk.Text(self, font=("Poppins", 11), bd=0, relief="flat", wrap="word")
        self.invoice_text.pack(fill="both", expand=True, padx=20, pady=10)
        self.invoice_text.configure(state="normal")

        content_lines = []
        content_lines.append("Cafe Management System Invoice")
        content_lines.append("="*40)
        content_lines.append(f"Order ID: {order['id']}")
        content_lines.append(f"Date & Time: {order['datetime']}")
        content_lines.append(f"Customer Name: {order['customer_name']}")
        content_lines.append(f"Customer Phone: {order['customer_phone']}")
        content_lines.append("="*40)
        content_lines.append("Items:")
        content_lines.append(f"{'Name':20} {'Unit Price':>10} {'Qty':>6} {'Total':>10}")
        content_lines.append("-"*40)
        for item in order["items"]:
            name = (item["name"][:18] + '..') if len(item["name"]) > 20 else item["name"]
            content_lines.append(f"{name:20} ${item['unit_price']:>9.2f} {item['quantity']:>6} ${item['total']:>9.2f}")
        content_lines.append("="*40)
        content_lines.append(f"Total Amount: ${order['total']:.2f}")
        content_lines.append("="*40)
        content_lines.append("\nThank you for your purchase!\n")

        self.invoice_text.insert("1.0", "\n".join(content_lines))
        self.invoice_text.configure(state="disabled")

        # Buttons Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        btn_save = ttk.Button(btn_frame, text="Save Invoice", command=self.save_invoice)
        btn_save.grid(row=0, column=0, padx=10)

        btn_close = ttk.Button(btn_frame, text="Close", command=self.destroy)
        btn_close.grid(row=0, column=1, padx=10)

        self.transient(parent)
        self.grab_set()
        self.focus()
        self.wait_window(self)

    def save_invoice(self):
        invoice_content = self.invoice_text.get("1.0", "end").strip()
        default_filename = f"Invoice_Order_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(title="Save Invoice As", defaultextension=".txt",
                                                 initialfile=default_filename,
                                                 filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(invoice_content)
            messagebox.showinfo("Success", f"Invoice saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save invoice:\n{e}")

class OrderDetailsWindow(tk.Toplevel):
    def __init__(self, parent, order):
        super().__init__(parent)
        self.title(f"Order Details - Order #{order['id']}")
        self.geometry("600x500")
        self.configure(bg="#f9f9fb")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("TLabel", font=("Poppins", 11), background="#f9f9fb", foreground="#222222")
        self.style.configure("Header.TLabel", font=("Poppins", 18, "bold"), foreground="#6a1b9a", background="#f9f9fb")

        header = ttk.Label(self, text="Order Details", style="Header.TLabel")
        header.pack(pady=(20, 10))

        info_frame = ttk.Frame(self)
        info_frame.pack(padx=20, fill="x")

        lbl_id = ttk.Label(info_frame, text=f"Order ID: {order['id']}")
        lbl_id.pack(anchor="w")

        lbl_date = ttk.Label(info_frame, text=f"Date & Time: {order['datetime']}")
        lbl_date.pack(anchor="w")

        lbl_name = ttk.Label(info_frame, text=f"Customer Name: {order['customer_name']}")
        lbl_name.pack(anchor="w")

        lbl_phone = ttk.Label(info_frame, text=f"Customer Phone: {order['customer_phone']}")
        lbl_phone.pack(anchor="w")

        # Items list
        columns = ("Name", "Unit Price", "Quantity", "Total")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            if col == "Name":
                tree.column(col, width=250, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        for item in order["items"]:
            tree.insert("", "end", values=(
                item["name"],
                f"{item['unit_price']:.2f}",
                item["quantity"],
                f"{item['total']:.2f}"
            ))

        lbl_total = ttk.Label(self, text=f"Total Amount: ${order['total']:.2f}", font=("Poppins", 14, "bold"), foreground="#6a1b9a")
        lbl_total.pack(pady=(0, 15))

        btn_close = ttk.Button(self, text="Close", command=self.destroy)
        btn_close.pack(pady=10)

        self.transient(parent)
        self.grab_set()
        self.focus()
        self.wait_window(self)

if __name__ == "__main__":
    app = CafeManagementApp()
    app.mainloop()
