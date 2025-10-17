from db_connection import DatabaseConnection
from helpers import hash_password, verify_password
from datetime import datetime


class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_user(self, username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        return self.db.fetch_one(query, (username,))

    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        user = self.get_user(username)
        if user and verify_password(password, user['password_hash']):
            return True, user
        return False, None

    def add_user(self, username, password, role, full_name):
        """Add new user"""
        if self.user_exists(username):
            return False, "Username already exists!"

        # Validate password strength
        if len(password) < 6:
            return False, "Password must be at least 6 characters long!"

        query = """
                INSERT INTO users (username, password_hash, role, full_name, created_at)
                VALUES (%s, %s, %s, %s, %s) \
                """
        hashed_password = hash_password(password)
        created_at = datetime.now()

        success, result = self.db.execute_query(
            query,
            (username, hashed_password, role, full_name, created_at)
        )

        if success:
            return True, "User added successfully!"
        return False, f"Error adding user: {result}"

    def update_user(self, user_id, full_name=None, role=None):
        """Update user information"""
        updates = []
        params = []

        if full_name:
            updates.append("full_name = %s")
            params.append(full_name)
        if role:
            updates.append("role = %s")
            params.append(role)

        if not updates:
            return False, "No fields to update!"

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"

        success, result = self.db.execute_query(query, tuple(params))

        if success:
            return True, "User updated successfully!"
        return False, f"Error updating user: {result}"

    def change_password(self, username, old_password, new_password):
        """Change user password"""
        user = self.get_user(username)
        if not user:
            return False, "User not found!"

        if not verify_password(old_password, user['password_hash']):
            return False, "Incorrect old password!"

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long!"

        query = "UPDATE users SET password_hash = %s WHERE username = %s"
        hashed_password = hash_password(new_password)

        success, result = self.db.execute_query(query, (hashed_password, username))

        if success:
            return True, "Password changed successfully!"
        return False, f"Error changing password: {result}"

    def delete_user(self, user_id):
        """Delete user"""
        # Check if it's admin (user_id = 1)
        if user_id == 1:
            return False, "Cannot delete admin user!"

        query = "DELETE FROM users WHERE user_id = %s"
        success, result = self.db.execute_query(query, (user_id,))

        if success:
            return True, "User deleted successfully!"
        return False, f"Error deleting user: {result}"

    def user_exists(self, username):
        """Check if user exists"""
        return self.get_user(username) is not None

    def get_all_users(self):
        """Get all users"""
        query = "SELECT user_id, username, role, full_name, created_at FROM users ORDER BY user_id"
        return self.db.fetch_all(query)

    def get_users_by_role(self, role):
        """Get all users with specific role"""
        query = "SELECT user_id, username, full_name, created_at FROM users WHERE role = %s"
        return self.db.fetch_all(query, (role,))