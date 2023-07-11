import numpy as np
import random
import pandas as pd
from datetime import datetime
from customer_class import Customer
from transition_matrix import transition_modified_animation

class Supermarket:
    """Manages multiple Customer instances that are currently in the market."""

    def __init__(self, name, opening, closing):
        self.name = name
        self.number_in_stock = {'dairy': 70, 'drinks': 100, 'fruit': 50, 'spices': 30}
        self.customers = []
        self.opening = opening
        self.closing = closing
        self.minutes = 0
        self.revenue = 0
        self.index = 0
        self.customer_index = 0
        self.d_time = pd.date_range(self.opening, self.closing, freq="T").time

    def is_open(self):
        return self.index <= len(self.d_time)-2
        
    def get_time(self):
        self.current_time = self.d_time[self.index]
        self.current_time = str(self.current_time)
        return self.current_time

    def print_customers(self):
        return self.customers

    def next_minute(self):
        self.index += 1
        if not self.is_open():
            return

        #next_time = self.d_time[self.index]

        for customer in self.customers:
            next_location = customer.next_locations(transition_modified_animation)
            customer.financial_status()
            if not customer.is_active(next_location):
                self.revenue += customer.receipt

    def add_new_customers(self):
        self.state = random.choices(['dairy', 'drinks', 'fruit', 'spices'])
        self.state = self.state[0]
        self.customer_index += 1
        new_customer = Customer(self.customer_index)
        self.customers.append(new_customer)

    def remove_existing_customers(self):
        self.customers = [customer for customer in self.customers if customer.is_active(customer.state)]

    def update_stock(self):
        for customer in self.customers:
            if customer.state in self.number_in_stock and self.number_in_stock[customer.state] > 0:
                self.number_in_stock[customer.state] -= 1
    
    def add_stock(self):
        for product, stock in self.number_in_stock.items():
            if stock < 10:
                print(f"Stock is low for {product}")
                self.number_in_stock[product] += 30


if __name__ == "__main__":
    supermarket = Supermarket('MarketRangers', '07:00:00', '08:30:00')
    market_rangers = pd.DataFrame(columns=['timestamp', 'customer_no', 'location'])

    while supermarket.is_open():
        supermarket.add_new_customers()
        for customer in supermarket.customers:
            market_rangers = market_rangers._append({'timestamp': supermarket.get_time(),
                                                    'customer_no': customer.name,
                                                    'location': customer.state},
                                                    ignore_index=True)

        supermarket.remove_existing_customers()
        supermarket.next_minute()
        supermarket.update_stock()
        supermarket.add_stock()

    market_rangers.set_index('timestamp', inplace=True)
    market_rangers.to_csv('./berkay_all/simulated_market_table.csv')