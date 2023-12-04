import numpy as np
from transition_matrix import transition_modified_animation

class Customer:
    def __init__(self, name):    
        # Initialize customer attributes
        self.name = name
        self.locations = ['checkout', 'dairy', 'drinks', 'fruit', 'spices', 'entrance']
        self.budget = np.random.randint(50, 100)
        self.state = 'entrance'
        self.receipt = 0
        self.product_prices = {
            'dairy': [0.5, 1, 1.5, 2, 3, 4, 5],
            'drinks': [0.5, 1, 1.5, 2, 3, 4, 5],
            'fruit': [1, 2, 3, 4, 5],
            'spices': [1.5, 2, 3, 4.5, 5]
        }
    
    def next_location(self, matrix):
        # Determine next location based on the transition matrix
        if self.state != 'checkout':
            next_location = np.random.choice(self.locations, p=matrix.round(2).loc[self.state])
            print(f"Customer moves from {self.state} to {next_location}")
            self.state = next_location
        else:
            next_location = np.random.choice(self.locations, p=matrix.round(2).loc[self.state])
            print(f"Customer moves from {self.state} to {next_location}")
            self.state = next_location
        return next_location

    def is_active(self):
        # Check if the customer is still active (has not reached checkout)
        return self.state != 'checkout'

    def financial_status(self):
        # Handle financial status while shopping
        if self.state != 'checkout':
            price = np.random.choice(self.product_prices[self.state])
            self.receipt += price
            print(f"Customer is at {self.state} and continues to shop")
        else:
            print(f"Customer is at {self.state} and paid {self.receipt}")
            self.budget -= self.receipt


if __name__ == "__main__":
    customer_samples = ["19_monday", "10_monday", "40_monday"]  # Defining the customers to simulate

    customers = [Customer(f"customer_{i}") for i in customer_samples]

    # Simulate customer behavior in the supermarket
    while any(customer.is_active() for customer in customers):
        customers_to_remove = []

        for customer in customers:
            next_location = customer.next_location(transition_modified_animation)
            if next_location == 'checkout':
                customers_to_remove.append(customer)

            customer.financial_status()

        # Remove customers who reached checkout
        for customer in customers_to_remove:
            customers.remove(customer)
