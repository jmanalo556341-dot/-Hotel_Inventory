from db_connection import DatabaseConnection
from datetime import datetime


class InventoryService:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_item(self, name, category, quantity, min_stock, price):
        """Add new item to inventory"""
        # Validation
        if not name or not category:
            return False, "Name and category are required!"

        if quantity < 0 or min_stock < 0 or price < 0:
            return False, "Quantity, minimum stock, and price must be non-negative!"

        # Check for duplicate names
        if self.item_name_exists(name):
            return False, "Item with this name already exists!"

        query = """
            INSERT INTO inventory (name, category, quantity, min_stock, price, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        created_at = datetime.now()

        success, result = self.db.execute_query(
            query,
            (name, category, quantity, min_stock, price, created_at)
        )

        if success:
            return True, "Item added successfully!"
        return False, f"Error adding item: {result}"

    def update_item(self, item_id, name, category, quantity, min_stock, price):
        """Update existing item"""
        # Validation
        if not name or not category:
            return False, "Name and category are required!"

        if quantity < 0 or min_stock < 0 or price < 0:
            return False, "Quantity, minimum stock, and price must be non-negative!"

        # Check if item exists
        if not self.get_item(item_id):
            return False, "Item not found!"

        query = """
            UPDATE inventory
            SET name = %s,
                category = %s,
                quantity = %s,
                min_stock = %s,
                price = %s
            WHERE item_id = %s
        """

        success, result = self.db.execute_query(
            query,
            (name, category, quantity, min_stock, price, item_id)
        )

        if success:
            return True, "Item updated successfully!"
        return False, f"Error updating item: {result}"

    def delete_item(self, item_id):
        """Delete item from inventory"""
        query = "DELETE FROM inventory WHERE item_id = %s"
        success, result = self.db.execute_query(query, (item_id,))

        if success:
            return True, "Item deleted successfully!"
        return False, f"Error deleting item: {result}"

    def get_item(self, item_id):
        """Get item by ID"""
        query = "SELECT * FROM inventory WHERE item_id = %s"
        return self.db.fetch_one(query, (item_id,))

    def get_all_items(self):
        """Get all items"""
        query = "SELECT * FROM inventory ORDER BY item_id"
        return self.db.fetch_all(query)

    def search_items(self, search_term):
        """Search items by name or category"""
        query = """
            SELECT *
            FROM inventory
            WHERE name LIKE %s
               OR category LIKE %s
            ORDER BY item_id
        """
        search_pattern = f"%{search_term}%"
        return self.db.fetch_all(query, (search_pattern, search_pattern))

    def get_low_stock_items(self):
        """Get items with quantity at or below minimum stock"""
        query = "SELECT * FROM inventory WHERE quantity <= min_stock ORDER BY quantity ASC"
        return self.db.fetch_all(query)

    def get_items_by_category(self, category):
        """Get all items in a specific category"""
        query = "SELECT * FROM inventory WHERE category = %s ORDER BY name"
        return self.db.fetch_all(query, (category,))

    def get_categories(self):
        """Get all unique categories"""
        query = "SELECT DISTINCT category FROM inventory ORDER BY category"
        results = self.db.fetch_all(query)
        return [row['category'] for row in results]

    def update_quantity(self, item_id, quantity_change):
        """Update item quantity (add or subtract)"""
        item = self.get_item(item_id)
        if not item:
            return False, "Item not found!"

        new_quantity = item['quantity'] + quantity_change

        if new_quantity < 0:
            return False, "Insufficient quantity!"

        query = "UPDATE inventory SET quantity = %s WHERE item_id = %s"
        success, result = self.db.execute_query(query, (new_quantity, item_id))

        if success:
            return True, f"Quantity updated! New quantity: {new_quantity}"
        return False, f"Error updating quantity: {result}"

    def item_name_exists(self, name):
        """Check if item name already exists"""
        query = "SELECT item_id FROM inventory WHERE name = %s"
        return self.db.fetch_one(query, (name,)) is not None

    def get_statistics(self):
        """Get inventory statistics"""
        query = """
            SELECT 
                COUNT(*) as total_items,
                SUM(CASE WHEN quantity <= min_stock THEN 1 ELSE 0 END) as low_stock_count,
                SUM(quantity * price) as total_value,
                SUM(quantity) as total_quantity
            FROM inventory
        """
        result = self.db.fetch_one(query)

        if result:
            return {
                'total_items': result['total_items'] or 0,
                'low_stock_count': result['low_stock_count'] or 0,
                'total_value': float(result['total_value'] or 0),
                'total_quantity': result['total_quantity'] or 0
            }

        return {
            'total_items': 0,
            'low_stock_count': 0,
            'total_value': 0.0,
            'total_quantity': 0
        }