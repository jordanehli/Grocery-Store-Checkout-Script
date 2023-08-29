#Author: Jordan Ehlinger
#Assignment Number & Name: Inventory
#Due Date: N/A
#Program Description: Holds the inventory class

class Inventory:
    #initialize the inventory attributes
    def __init__(self, item_id, name, stock, price):
        self.__item_id = item_id
        self.__name = name
        self.__stock = int(stock)
        self.__price = float(price)

    #get functions for attributes
    def get_id(self):
        return self.__item_id
    def get_name(self):
        return self.__name
    def get_stock(self):
        return self.__stock
    def get_price(self):
        return self.__price
    

    #restock function adds to inventory if return
    def restock(self, new_stock):
        new_stock = abs(new_stock)
        self.__stock += new_stock


    #purchase function adjusts stock if there is enough stock
    def purchase(self, purch_qty):
        if purch_qty <= self.__stock:
            self.__stock -= purch_qty
            return True
        else:
            return False

    #string function to display entire inventory menu
    def __str__(self):
        inv_output = "ID\t" + "Item\t" + "Qty Available\t" + "Price"
        inv_output += "----------------------------------------------------------"
        inv_output += self.__item_id + self.__name + self.__stock + self.__price
        return inv_output
