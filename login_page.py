import tkinter as tk
from tkinter import messagebox
from models.user_model import UserModel
from auth_service import AuthService
from register_page import RegisterWindow
from inventory_page import HotelInventorySystem
from helpers import center_window


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Inventory - Login")
        self.root.geometry("450x550")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        center_window(self.root)

        self.user_model = UserModel()
        self.auth_service = AuthService(self.user_model)

        self.create_login_ui()

    def create_login_ui(self):
        """Create login interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#34495e", height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🏨",
            font=("Arial", 40),
            bg="#34495e",
            fg="white"
        ).pack(pady=(15, 0))

        tk.Label(
            header_frame,
            text="Hotel Inventory System",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white"
        ).pack()

        # Main form
        form_frame = tk.Frame(self.root, bg="#2c3e50")
        form_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)

        tk.Label(
            form_frame,
            text="Sign In",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=(0, 30))

        # Username
        tk.Label(
            form_frame,
            text="Username",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        ).pack(anchor="w", pady=(0, 5))

        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#34495e",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            bd=0
        )
        self.username_entry.pack(fill=tk.X, ipady=10, pady=(0, 20))
        self.username_entry.focus()

        # Password
        tk.Label(
            form_frame,
            text="Password",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        ).pack(anchor="w", pady=(0, 5))

        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#34495e",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            bd=0,
            show="●"
        )
        self.password_entry.pack(fill=tk.X, ipady=10, pady=(0, 30))

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())

        # Login button
        self.login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.login
        )
        self.login_btn.pack(fill=tk.X, ipady=12)

        # Register button
        tk.Button(
            form_frame,
            text="Create New Account",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#3498db",
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
            command=self.show_register
        ).pack(pady=(15, 0))

        # Info label
        tk.Label(
            form_frame,
            text="Default: admin / admin123",
            font=("Arial", 9, "italic"),
            bg="#2c3e50",
            fg="#7f8c8d"
        ).pack(pady=(20, 0))

    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        success, user = self.auth_service.authenticate(username, password)

        if success:
            messagebox.showinfo("Success", f"Welcome, {user['name']}!")
            self.open_inventory_system(username, user)
        else:
            messagebox.showerror("Error", "Invalid username or password!")
            self.password_entry.delete(0, tk.END)

    def show_register(self):
        """Show registration window"""
        RegisterWindow(self.root, self.user_model, self.auth_service)

    def open_inventory_system(self, username, user_info):
        """Open main inventory system"""
        self.root.withdraw()
        inventory_window = tk.Toplevel(self.root)
        app = HotelInventorySystem(inventory_window, username, user_info)

        def on_closing():
            inventory_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

        inventory_window.protocol("WM_DELETE_WINDOW", on_closing)
