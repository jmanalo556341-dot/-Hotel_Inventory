from helpers import hash_password


class AuthService:
    def __init__(self, user_model):
        self.user_model = user_model

    def authenticate(self, username, password):
        """Authenticate user"""
        user = self.user_model.get_user(username)
        # FIX: Changed from user["password"] to user["password_hash"]
        if user and user["password_hash"] == hash_password(password):
            return True, {
                'user_id': user['user_id'],
                'name': user['full_name'],
                'username': user['username'],
                'role': user['role']
            }
        return False, None

    def register_user(self, username, password, role, name):
        """Register new user"""
        if self.user_model.user_exists(username):
            return False, "Username already exists!"

        if len(password) < 6:
            return False, "Password must be at least 6 characters!"

        success, message = self.user_model.add_user(username, password, role, name)
        return success, message