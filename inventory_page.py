import tkinter as tk
from tkinter import ttk, messagebox
from inventory_service import InventoryService


class HotelInventorySystem:
    def __init__(self, root, username, user_info):
        self.root = root
        self.username = username
        self.user_info = user_info
        self.root.title(f"Hotel Inventory Management - {user_info['name']} ({user_info['role']})")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        self.inventory_service = InventoryService()
        self.selected_item_id = None

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Title with user info
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="🏨 Hotel Inventory Management System",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        user_label = tk.Label(
            title_frame,
            text=f"👤 {self.user_info['name']} | {self.user_info['role']}",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        user_label.pack(side=tk.RIGHT, padx=20)

        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left panel - Input form
        left_frame = tk.LabelFrame(
            main_frame,
            text="Add/Edit Item",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=20
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        # Item Name
        tk.Label(left_frame, text="Item Name:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w",
                                                                                     pady=5)
        self.name_entry = tk.Entry(left_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        # Category
        tk.Label(left_frame, text="Category:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        categories = ["Linens", "Toiletries", "Kitchenware", "Electronics", "Furniture", "Cleaning Supplies", "Other"]
        self.category_combo = ttk.Combobox(
            left_frame,
            textvariable=self.category_var,
            values=categories,
            font=("Arial", 10),
            width=23,
            state="readonly"
        )
        self.category_combo.set("Linens")
        self.category_combo.grid(row=1, column=1, pady=5, padx=5)

        # Quantity
        tk.Label(left_frame, text="Quantity:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.quantity_entry = tk.Entry(left_frame, font=("Arial", 10), width=25)
        self.quantity_entry.grid(row=2, column=1, pady=5, padx=5)

        # Minimum Stock
        tk.Label(left_frame, text="Min Stock Level:", font=("Arial", 10), bg="white").grid(row=3, column=0, sticky="w",
                                                                                           pady=5)
        self.min_stock_entry = tk.Entry(left_frame, font=("Arial", 10), width=25)
        self.min_stock_entry.grid(row=3, column=1, pady=5, padx=5)

        # Price
        tk.Label(left_frame, text="Unit Price (₱):", font=("Arial", 10), bg="white").grid(row=4, column=0, sticky="w",
                                                                                          pady=5)
        self.price_entry = tk.Entry(left_frame, font=("Arial", 10), width=25)
        self.price_entry.grid(row=4, column=1, pady=5, padx=5)

        # Buttons
        button_frame = tk.Frame(left_frame, bg="white")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        self.add_btn = tk.Button(
            button_frame,
            text="Add Item",
            command=self.add_item,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.update_btn = tk.Button(
            button_frame,
            text="Update Item",
            command=self.update_item,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.update_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Statistics frame
        stats_frame = tk.LabelFrame(
            left_frame,
            text="Inventory Statistics",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        stats_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        self.total_items_label = tk.Label(stats_frame, text="Total Items: 0", font=("Arial", 9), bg="white")
        self.total_items_label.pack(anchor="w", pady=2)

        self.low_stock_label = tk.Label(stats_frame, text="Low Stock Items: 0", font=("Arial", 9), bg="white", fg="red")
        self.low_stock_label.pack(anchor="w", pady=2)

        self.total_value_label = tk.Label(stats_frame, text="Total Value: ₱0.00", font=("Arial", 9), bg="white")
        self.total_value_label.pack(anchor="w", pady=2)

        # Right panel - Table
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Search bar
        search_frame = tk.Frame(right_frame, bg="white")
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Search:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        # Table
        table_frame = tk.Frame(right_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")

        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Category", "Quantity", "Min Stock", "Price", "Total Value", "Status"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=20
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Define columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Min Stock", text="Min Stock")
        self.tree.heading("Price", text="Unit Price")
        self.tree.heading("Total Value", text="Total Value")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Category", width=120)
        self.tree.column("Quantity", width=80, anchor="center")
        self.tree.column("Min Stock", width=80, anchor="center")
        self.tree.column("Price", width=90, anchor="center")
        self.tree.column("Total Value", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        # Pack table and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Action buttons (delete button - only admin can delete items)
        action_frame = tk.Frame(right_frame, bg="white")
        action_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            action_frame,
            text="Delete",
            command=self.delete_item,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

    def add_item(self):
        """Add new item to inventory"""
        name = self.name_entry.get().strip()
        category = self.category_var.get()

        try:
            quantity = int(self.quantity_entry.get())
            min_stock = int(self.min_stock_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity, min stock, and price!")
            return

        if not name:
            messagebox.showerror("Error", "Please enter item name!")
            return

        if quantity < 0 or min_stock < 0 or price < 0:
            messagebox.showerror("Error", "Values cannot be negative!")
            return

        success, message = self.inventory_service.add_item(name, category, quantity, min_stock, price)

        if success:
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", f"Item '{name}' added successfully!")

    def update_item(self):
        """Update existing item"""
        if self.selected_item_id is None:
            return

        name = self.name_entry.get().strip()
        category = self.category_var.get()

        try:
            quantity = int(self.quantity_entry.get())
            min_stock = int(self.min_stock_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return

        if not name:
            messagebox.showerror("Error", "Please enter item name!")
            return

        success, message = self.inventory_service.update_item(
            self.selected_item_id, name, category, quantity, min_stock, price
        )

        if success:
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", message)

    def delete_item(self):
        """Delete selected item - Admin only"""
        if self.user_info['role'] != "Admin":
            messagebox.showerror("Access Denied", "Only Admins can delete items!")
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete!")
            return

        item_id = int(self.tree.item(selected[0])['values'][0])

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            success, message = self.inventory_service.delete_item(item_id)

            if success:
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Success", message)

    def on_item_double_click(self, event):
        """Handle double-click on table row"""
        selected = self.tree.selection()
        if selected:
            item_id = int(self.tree.item(selected[0])['values'][0])
            item = self.inventory_service.get_item(item_id)

            if item:
                self.selected_item_id = item_id
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, item['name'])
                self.category_var.set(item['category'])
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, str(item['quantity']))
                self.min_stock_entry.delete(0, tk.END)
                self.min_stock_entry.insert(0, str(item['min_stock']))
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, str(item['price']))

                self.add_btn.config(state=tk.DISABLED)
                self.update_btn.config(state=tk.NORMAL)

    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.category_var.set("Linens")
        self.quantity_entry.delete(0, tk.END)
        self.min_stock_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.selected_item_id = None
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)

    def refresh_table(self):
        """Refresh the table with current inventory"""
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_term = self.search_entry.get().lower()

        # Get items (filtered if search term exists)
        if search_term:
            items = self.inventory_service.search_items(search_term)
        else:
            items = self.inventory_service.get_all_items()

        # Display items
        for item in items:
            total_item_value = item['quantity'] * item['price']
            status = "Low Stock" if item['quantity'] <= item['min_stock'] else "In Stock"
            tag = 'low_stock' if status == "Low Stock" else 'in_stock'

            # FIX: Changed from item['id'] to item['item_id']
            self.tree.insert("", tk.END, values=(
                item['item_id'],
                item['name'],
                item['category'],
                item['quantity'],
                item['min_stock'],
                f"₱{item['price']:.2f}",
                f"₱{total_item_value:.2f}",
                status
            ), tags=(tag,))

        # Configure tags
        self.tree.tag_configure('low_stock', background='#ffcccc')
        self.tree.tag_configure('in_stock', background='#ccffcc')

        # Update statistics
        stats = self.inventory_service.get_statistics()
        self.total_items_label.config(text=f"Total Items: {stats['total_items']}")
        self.low_stock_label.config(text=f"Low Stock Items: {stats['low_stock_count']}")
        self.total_value_label.config(text=f"Total Value: ₱{stats['total_value']:.2f}")