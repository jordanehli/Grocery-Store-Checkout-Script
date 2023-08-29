#Author: Jordan Ehlinger
#Assignment Number & Name: TransactionItem
#Due Date: N/A
#Program Description: Holds the transaction item class


class TransactionItem:
    #initialize attributes to default values
    def __init__(self, item_id, name, qty, price, cost):
        self.__item_id = item_id
        self.__name = name
        self.__qty = qty
        self.__price = price
        self.__cost = cost

    #get functions for attributes
    def get_id(self):
        return self.__item_id
    def get_name(self):
        return self.__name
    def get_qty(self):
        return self.__qty
    def get_price(self):
        return self.__price

    #set functions for attributes
    def set_id(self, new_id):
        self.__item_id = new_id
    def set_name(self, new_name):
        self.__name = new_name
    def set_qty(self, new_qty):
        self.__qty = new_qty
    def set_price(self, new_price):
        self.__price = new_price


    #get function for cost
    def get_cost(self):
        return self.__cost
    
    #calculate cost method
    def calc_cost(self):
        self.__cost = self.__price * self.__qty

    #string method to display invoice
    def __str__(self):
        invoice = "Order Complete. See Invoice Below:\n"
        invoice += "ID\t" + "Name\t" + "Quantity\t" + "Price\t" + "Extended Price\n"
        invoice += str(self.__item_id) + str(self.__name) + str(self.__qty) + str(self.__price) + str(self.__cost)
        return invoice        
    
        
