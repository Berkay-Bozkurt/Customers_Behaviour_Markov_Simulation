import random
import pandas as pd
from datetime import datetime
from customer_class import Customer

class Supermarket:
    """manages multiple Customer instances and inventory that are currently in the market."""

    def __init__(self, name, opening, closing):
        """Initialize the Supermarket instance with given parameters."""
        self.name = name
        self.inventory = {'dairy': 70, 'drinks': 100, 'fruit': 50, 'spices': 30}
        self.customers = []
        self.opening = opening
        self.closing = closing
        self.minutes = 0
        self.index = 0
        self.customer_index = 0
        self.revenue = 0
        self.time_range = pd.date_range(self.opening, self.closing, freq="T").time

    def __repr__(self):
        """String representation of the Supermarket instance."""
        return f'{len(self.time_range)}'

    def is_open(self):
        """Check if the supermarket is open based on the current time."""
        current_time = self.time_range[self.index]
        return datetime.strptime(self.opening, '%H:%M:%S') <= datetime.strptime(str(current_time), '%H:%M:%S') <= datetime.strptime(self.closing, '%H:%M:%S')

    def get_current_time(self):
        """Get the current time in HH:MM format."""
        return str(self.time_range[self.index])

    def get_active_customers(self):
        """Retrieve details of active customers."""
        return [customer.get_customer_details() for customer in self.customers if customer.is_active()]

    def move_customers_next_minute(self):
        """Move customers to the next state for the next minute."""
        self.index += 1
        for customer in self.customers:
            customer.move_to_next_location()

    def add_new_customer(self):
        """Add a new random customer to the supermarket."""
        self.customer_index += 1
        state = random.choice(['dairy', 'drinks', 'fruit', 'spices'])
        new_customer = Customer(self.customer_index, state)
        self.customers.append(new_customer)

    def remove_inactive_customers(self):
        """Remove inactive customers from the supermarket."""
        self.customers = [customer for customer in self.customers if customer.is_active()]

    def update_revenue(self):
        """Update supermarket revenue based on customers' transactions."""
        for customer in self.customers:
            if customer.state == "checkout":
                self.revenue += 100 - customer.budget
        return self.revenue

    def update_inventory(self):
        """Update inventory based on customers' purchases."""
        for customer in self.customers:
            if customer.state in self.inventory:
                self.inventory[customer.state] -= 1

    def add_to_inventory(self):
        """Check inventory levels and replenish low stock."""
        for category, stock_count in self.inventory.items():
            if stock_count < 10:
                print(f"Stock is low for {category}")
                self.inventory[category] += 30

if __name__ == "__main__":
    # Run a basic simulation of the supermarket
    market = Supermarket("Marketelli", "08:00:00", "20:00:00")
    market.add_new_customer()
    market.remove_inactive_customers()
    market.update_revenue()
    market.update_inventory()
    market.add_to_inventory()
