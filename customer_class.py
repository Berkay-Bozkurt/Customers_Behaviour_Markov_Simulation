from transition_matrix import transition_modified_animation
import numpy as np

class Customer:

    def __init__(self, name):    
        self.name = name
        self.locations =['checkout', 'dairy', 'drinks', 'fruit', 'spices', "entrance"]
        self.budget=np.random.randint(50,100)
        self.state = "entrance"
        self.receipt=0
        self.produckt_prices={'dairy':[0.5,1,1.5,2,3,4,5], 'drinks':[0.5,1,1.5,2,3,4,5], 'fruit':[1,2,3,4,5], 'spices':[1.5,2,3,4.5,5]}
    
    def next_locations(self ,matrix):
        self.matrix=matrix
        if self.state!="checkout":
            next_location=np.random.choice(self.locations, p=self.matrix.round(2).loc[self.state])
            print(f"Customers moves from {self.state} to {next_location}")
            self.state = next_location

        else:
            next_location=np.random.choice(self.locations, p=self.matrix.round(2).loc[self.state])
            print(f"Customers moves from {self.state} to {next_location}")
            self.state = next_location

        return next_location

    def is_active(self, next_lacation):
        """Returns True if the customer has not reached the checkout yet."""
        if next_lacation == "checkout":
            return False
        else:
            return True
        
    def financial_status(self):
        if self.state!="checkout":
            price=np.random.choice(list(self.produckt_prices[f"{self.state}"]))
            self.receipt+=price
            print(f"Customer is at {self.state} and continue to shop")
        else:
            print(f"Customer is at {self.state} and {self.receipt} is paid")
            self.budget-=self.receipt 


        
if __name__ == "__main__":
    customer_sample = ["19_monday", "10_monday", "40_monday"]  # Define the customers you want to simulate

    customers = []
    for i in customer_sample:
        customer = Customer(f"customer_{i}")
        customers.append(customer)

    while any(customer.is_active(customer.state) for customer in customers):
        customers_to_remove = []  # List to store customers that need to be removed
        for customer in customers:
            next_location = customer.next_locations(transition_modified_animation)
            location_status = customer.is_active(next_location)
            financial_status = customer.financial_status()
            if next_location == "checkout":
                customers_to_remove.append(customer)  # Add customer to the removal list

        for customer in customers_to_remove:
            customers.remove(customer)  # Remove customers outside the loop
