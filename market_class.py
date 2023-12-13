import random
import pandas as pd
from datetime import datetime
from customer_class import Customer
from matrix_transition import transition_modified_animation

class Supermarket:
    """Manages multiple Customer instances and inventory that are currently in the market."""

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

    def is_open(self):
        """Check if the supermarket is open based on the current time."""
        current_time = self.time_range[self.index]
        return datetime.strptime(self.opening, '%H:%M:%S') <= datetime.strptime(str(current_time), '%H:%M:%S') <= datetime.strptime(self.closing, '%H:%M:%S')

    def get_current_time(self):
        """Get the current time in HH:MM format."""
        return str(self.time_range[self.index])

    def move_customers_next_minute(self):
        """Move customers to the next state for the next minute."""
        self.index += 1
        print(f"\nCurrent Time: {self.get_current_time()}")
        for customer in self.customers:
            next_location = customer.next_location(transition_modified_animation)
            print(f"Customer {customer.name} moves to {next_location}")

    def add_new_customer(self):
        """Add a new random customer to the supermarket."""
        self.customer_index += 1
        state = 'entrance'
        new_customer = Customer(f"customer_{self.customer_index}")
        self.customers.append(new_customer)
        print(f"\nNew Customer Added: {new_customer.name}, State: {state}")

    def remove_inactive_customers(self):
        """Remove inactive customers from the supermarket."""
        inactive_customers = [customer for customer in self.customers if not customer.is_active()]
        self.customers = [customer for customer in self.customers if customer.is_active()]
        for customer in inactive_customers:
            print(f"\nCustomer Removed: {customer.name}")

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

    def record_customer_behavior(self):
        """Records customer behavior at each timestamp"""
        behavior = []
        for customer in self.customers:
            behavior.append({
                "timestamp": self.get_current_time(),
                "customer_no": customer.name,
                "location": customer.state
            })
        return behavior

    def create_simulated_market_table(self, duration_minutes):
        """Creates a simulated market table for a given duration"""
        market_table = []
        while self.is_open() and duration_minutes > 0:
            self.add_new_customer()
            self.move_customers_next_minute()
            self.remove_inactive_customers()
            self.update_revenue()
            self.update_inventory()
            self.add_to_inventory()
            behavior = self.record_customer_behavior()
            market_table.extend(behavior)
            duration_minutes -= 1
        return pd.DataFrame(market_table)

if __name__ == "__main__":
    market = Supermarket("Marketelli", "08:00:00", "20:00:00")
    simulated_market_table = market.create_simulated_market_table(duration_minutes=720)  # Set the desired duration
    simulated_market_table.to_csv('simulated_market_table.csv', index=False)
