import tkinter as tk
from tkinter import messagebox


class RegisterWindow:
    def __init__(self, parent, user_model, auth_service):
        self.parent = parent
        self.user_model = user_model
        self.auth_service = auth_service

        self.window = tk.Toplevel(parent)
        self.window.title("Create Account")
        self.window.geometry("400x650")
        self.window.configure(bg="#2c3e50")
        self.window.resizable(False, False)
        self.window.grab_set()

        self.create_register_ui()

    def create_register_ui(self):
        """Create registration interface"""
        tk.Label(
            self.window,
            text="Create New Account",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=(30, 40))

        form_frame = tk.Frame(self.window, bg="#2c3e50")
        form_frame.pack(padx=40, fill=tk.BOTH, expand=True)

        # Full Name
        tk.Label(form_frame, text="Full Name", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7").pack(anchor="w",
                                                                                                    pady=(0, 5))
        self.name_entry = tk.Entry(form_frame, font=("Arial", 11), bg="#34495e", fg="white", insertbackground="white",
                                   relief=tk.FLAT)
        self.name_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))

        # Username
        tk.Label(form_frame, text="Username", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7").pack(anchor="w",
                                                                                                   pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 11), bg="#34495e", fg="white",
                                       insertbackground="white", relief=tk.FLAT)
        self.username_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))

        # Password
        tk.Label(form_frame, text="Password", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7").pack(anchor="w",
                                                                                                   pady=(0, 5))
        self.password_entry = tk.Entry(form_frame, font=("Arial", 11), bg="#34495e", fg="white",
                                       insertbackground="white", relief=tk.FLAT, show="●")
        self.password_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))

        # Confirm Password
        tk.Label(form_frame, text="Confirm Password", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7").pack(anchor="w",
                                                                                                           pady=(0, 5))
        self.confirm_entry = tk.Entry(form_frame, font=("Arial", 11), bg="#34495e", fg="white",
                                      insertbackground="white", relief=tk.FLAT, show="●")
        self.confirm_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))

        # Role
        tk.Label(form_frame, text="Role", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7").pack(anchor="w", pady=(0, 5))
        self.role_var = tk.StringVar(value="Staff")
        role_frame = tk.Frame(form_frame, bg="#2c3e50")
        role_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Radiobutton(role_frame, text="Staff", variable=self.role_var, value="Staff", bg="#2c3e50", fg="white",
                       selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="Admin", bg="#2c3e50", fg="white",
                       selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT)

        # Buttons
        button_frame = tk.Frame(form_frame, bg="#2c3e50")
        button_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            button_frame,
            text="CREATE ACCOUNT",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.register
        ).pack(fill=tk.X, ipady=10, pady=(0, 10))

        tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.window.destroy
        ).pack(fill=tk.X, ipady=8)

    def register(self):
        """Handle registration"""
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        role = self.role_var.get()

        # Validation checks
        if not all([name, username, password, confirm]):
            messagebox.showerror("Error", "Please fill all fields!", parent=self.window)
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.window)
            return

        # Show confirmation dialog
        confirm_msg = "Create account with the following details?\n\n"
        confirm_msg += f"Name: {name}\n"
        confirm_msg += f"Username: {username}\n"
        confirm_msg += f"Role: {role}"

        result = messagebox.askyesno("Confirm Account Creation", confirm_msg, parent=self.window)

        if result:
            success, message = self.auth_service.register_user(username, password, role, name)

            if success:
                messagebox.showinfo("Success", f"{message}\n\nYou can now login with username: {username}",
                                    parent=self.window)
                self.window.destroy()
            else:
                messagebox.showerror("Error", message, parent=self.window)
