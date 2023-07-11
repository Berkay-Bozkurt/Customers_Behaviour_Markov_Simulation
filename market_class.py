import random
import pandas as pd
import numpy as np
from datetime import datetime
from customer_class import Customer

class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self, name, opening, closing):
        self.name=name        
        self.number_in_stock={'dairy':70, 'drinks':100, 'fruit':50, 'spices':30}
        self.customers = []
        self.opening = opening
        self.closing = closing
        self.minutes = 0
        self.revenue=0
        self.index = 0
        self.customer_index = 0
        self.dti = pd.date_range(self.opening, self.closing, freq="T").time


    def __repr__(self):
        return f'{len(self.dti)}'
    
    def is_open(self):
        if self.index <= len(self.dti)-2:
            return datetime.strptime(self.opening, '%H:%M:%S') <= datetime.strptime(self.get_time(), '%H:%M:%S') <= datetime.strptime(self.closing, '%H:%M:%S')


    def get_time(self):
        """current time in HH:MM format,"""
        self.current_time = self.dti[self.index]
        self.current_time = str(self.current_time)
        return self.current_time

    def print_customers(self):
        """print all customers with the current time and id in CSV format.
        """
        return self.customers

    def next_minute(self):
        """"propagates all customers to the next state."""

        self.index += 1
        next_time = self.dti[self.index]

        for customer in self.customers:
            customer.Customer.next_locatons()
    
    def add_new_customers(self):
        """randomly creates new customers.
        """
        self.state = random.choices(['dairy', 'drinks', 'fruit', 'spices'])
        self.state = self.state[0]
        self.customer_index += 1
        new_customer = Customer(self.customer_index, self.state)
        self.customers.append(new_customer)

    def remove_exitsting_customers(self):
        """removes every customer that is not active any more.
        """
        for customer in self.customers:
            if customer.is_active():
                self.customers.remove(customer)
    
    def updated_revenue(self):
        if Customer.self.state=="checkout":
            self.revenue=self.revenue+100-Customer.self.budget
        return self.revenue 
        
    
    def in_stock(self):
        if Customer.self.state=="dairy":
            self.number_in_stock[list(self.number_in_stock.keys())[0]]-=1
        elif Customer.self.state=="drinks":
            self.number_in_stock[list(self.number_in_stock.keys())[1]]-=1
        elif Customer.self.state=="fruit":
            self.number_in_stock[list(self.number_in_stock.keys())[2]]-=1
        elif Customer.self.state=="spices":
            self.number_in_stock[list(self.number_in_stock.keys())[3]]-=1
        return self.number_in_stock
    
    def add_stock(self):
        for i in self.number_in_stock.keys():
            if i<10:
                print(f"stock is low at {i}")
                self.number_in_stock[list(self.number_in_stock.keys())[1]]+=30    
    

if __name__=="__main__":
        Market=Supermarket("Marketelli")
        Market.add_new_customers()
        Market.remove_exitsting_customers()
        Market.updated_revenue()
        Market.in_stock()
