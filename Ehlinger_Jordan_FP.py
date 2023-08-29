#Author: Jordan Ehlinger
#Assignment Number & Name: MIS380P Final Project Spring 2023
#Due Date: N/A
#Program Description: Accept and process orders for a baking shop. Able to receive multiple orders and will print out an invoice once the order is complete.


#declare tax rate constant
TAX_RATE = 0.085

#import classes
import inventory
import transactionitem
import validation
import sys
import os

def main():
    #open txt files
    inventory_file = open("Inventory.txt", 'r')
    updated_inventory_file = open("UpdatedInventory.txt", 'r')
    #method will copy contents of Inventory.txt into UpdatedInventory.txt
    copy_file()
    
    #creates list and inventory instances
    inventory_list = create_inventory_list(inventory_file)
    
    #displays inventory menu
    display_list(inventory_list)
    
    #initialize transaction list
    transaction_list = []
    #initialize variable used for searching for a product ID
    search_item_id = -1
    inv_activate = 10
        
    #init false value
    did_purchase = False
    #while loop to allow customer to exit when they enter 0
    while search_item_id != 0:
        
        #validates inputted search id as positive number/not text and matches item id in inventory
        search_item_id = validate_search_id(inventory_list)
        if search_item_id == 0 :
            break
        #checks list and stores attributes for the id that matches the one we are searching for
        for inventory_item in inventory_list:
            if inventory_item.get_id() == search_item_id:
                inv_obj = inventory_item

        #asks for how much they would like to buy and verifies it is a number
        qty_requested = get_quantity()
        #runs if loop to see if qty is being returned or purchased
        if qty_requested < 0:
            #if customer enters negative number runs restock method
            inv_obj.restock(qty_requested)
            #variables below trigger a transaction action was made
            did_purchase = True
            inv_activate = 10
        else:
            #if postive then runs purchase method; will return True if purchased
            did_purchase = inv_obj.purchase(qty_requested)
            if did_purchase == False:
                #if not enough inventory for purchase then will notify 
                print("There is not enough inventory to complete your order. Please try again.")
                print()
                #bad value to skip below steps that alter invoice
                inv_activate = -1
            else:
                inv_activate = 10

        #makes sure an attempt to buy too much stock doesn't alter invoice
        if inv_activate == -1:
            search_item_id = -1
        else:
            #initialize variable and calculate cost from this transaction
            transaction_cost = qty_requested * inv_obj.get_price()
            #creates object for transaction class and stores this transaction as an instance
            transaction_object = transactionitem.TransactionItem(inv_obj.get_id(), inv_obj.get_name(), qty_requested, inv_obj.get_price(), transaction_cost)
            #adds this instance to the transaction list
            transaction_list.append(transaction_object)

            #close file so I can write on temp and then delete original
            updated_inventory_file.close()
            #adds edits and writes over updated inventory txt file
            update_file(search_item_id, inv_obj.get_stock())
            #reopens file after updated
            updated_inventory_file = open("UpdatedInventory.txt", 'r')

        #show updated menu        
        display_list(inventory_list)

   
    #if purchase was made then display invoice. Otherwise display thank you message
    if did_purchase == True:
        display_invoice(transaction_list)
    else:
        print("No items purchased. Thank you for visiting!")


###BEGINNING OF METHODS
#reads in inventory.txt file, creates an instance of inventory class, and creates inventory list
def create_inventory_list(inventory_file):    
    #initialize inventory list
    inventory_list = []
    item_id = 0
    #while loop to read all the item's in the file
    while item_id != '':
        #reads in each line and creates variables for inventory list columns
        item_id = inventory_file.readline().rstrip('\n')
        if item_id == '':
            break
        item_name = inventory_file.readline().rstrip('\n')
        stock = inventory_file.readline().rstrip('\n')
        price = inventory_file.readline().rstrip('\n')
        #creates instance of inventory class
        item = inventory.Inventory(item_id,item_name,stock,price)
        #adds the item to inventory list
        inventory_list.append(item)
    return inventory_list

    #close inventory.txt file
    inventory_file.close()


#displays the menu, pulling the attributes from the inventory class
def display_list(inventory_list):
    print(format("ID", "6"),end='')
    print(format("Item", "22"),end='')
    print(format("Qty Available", "20"),end='')
    print("Price")
    print("----------------------------------------------------------")
    
    for num in inventory_list:
        print(format(num.get_id(),"<6"), end='')
        print(format(num.get_name(), "25"), end='')
        print(format(num.get_stock(),"<17"), end='')
        print("$",num.get_price(), sep='')
    

#validates inputted search id as positive number and matches item id in inventory
def validate_search_id(inventory_list):
    #calls validation class
    validation_class = validation.ValidationClass()
    #init variables
    search_item_id = -1
    found = False
    #validation loop to make sure input is positive
    while search_item_id == -1:
        search_item_id_input = input("Which product ID would you like to purchase? Enter 0 to exit. ")
        search_item_id = validation_class.checkInteger(search_item_id_input)
        #if user enters 0 then they will exit the program
        if search_item_id == 0:
            return search_item_id
        #for loop to check if input matches valid item id
        for num in inventory_list:
            search_item_id = str(search_item_id)
            if search_item_id == num.get_id():
                found = True
        #if id is found then return it from this function, otherwise re-run loop
        if found == True:
            return search_item_id
        else:
            search_item_id = -1
        #catches invalid inputs to restart loop
        if search_item_id == -1:
            print("That ID does not match item ID currently in stock. Please try again")


#gets quantity for purchase and validates it is a number
def get_quantity():
    qty_requested = ""
    #while loop to make sure there is an input
    while qty_requested == "":
        #try/except to verify the input is a valid integer
        try:
            qty_requested = int(input("How many items would you like to purchase? Enter a negative number for a return. "))
            if qty_requested == 0:
                print("That is not a valid quantity. Please try again")
                qty_requested = ""
            else:
                return qty_requested
        except ValueError:
            print("That is not a valid integer. Please try again")
            qty_requested = ""
            

#creates updated inventory file as an exact copy of inventory.txt  
def copy_file():  
    #open files
    inventory_file = open("Inventory.txt", 'r')
    temp_file = open('UpdatedInventory.txt', 'w')
    #read in first line
    item_id = inventory_file.readline().rstrip('\n')
    #while loop to read the entire file
    while item_id != '':

        #strip the newline fr
        item_name = inventory_file.readline().rstrip('\n')
        stock = inventory_file.readline().rstrip('\n')
        price = inventory_file.readline().rstrip('\n')

        #write in data to file since these will remain the same
        temp_file.write(item_id + '\n')
        temp_file.write(item_name + '\n')
        temp_file.write(stock + '\n')
        temp_file.write(price + '\n')

        #read in next line
        item_id = inventory_file.readline().rstrip('\n')

    #close both files
    inventory_file.close()
    temp_file.close()


#writes over the updated inventory file while overwriting the updated inventory after a transaction   
def update_file(search_item_id, new_quantity):  
    #open files
    inventory_file = open("UpdatedInventory.txt", 'r')
    temp_file = open('temp.txt', 'w')
    #read in first line
    item_id = inventory_file.readline().rstrip('\n')
    #while loop to read the entire file
    while item_id != '':

        #strip the newline fr
        item_name = inventory_file.readline().rstrip('\n')
        stock = inventory_file.readline().rstrip('\n')
        price = inventory_file.readline().rstrip('\n')
        

        #print item id and name to file since these will remain the same
        temp_file.write(item_id + '\n')
        temp_file.write(item_name + '\n')

        #see if this is the desired value and either write or update as needed
        if item_id == search_item_id:
            #write new stock quantity
            temp_file.write(str(new_quantity) + '\n')
            #writes in same price either way since this doesn't change
            temp_file.write(price + '\n')
        else:
            temp_file.write(stock + '\n')
            temp_file.write(price + '\n')

        #read in next line
        item_id = inventory_file.readline().rstrip('\n')

    #close both files
    inventory_file.close()
    temp_file.close()
    
    #delete orginal file
    os.remove('UpdatedInventory.txt')
    #rename temp file back to correct name
    os.rename('temp.txt', 'UpdatedInventory.txt')

#displays the final invoice, pulling in the attributes from the transaction item class
def display_invoice(transaction_list):
    #initialize invoice variables
    total_qty = 0
    subtotal = 0

    print("\nOrder Complete. See Invoice Below:")
    print(format("ID", "6"),end='')
    print(format("Item", "22"),end='')
    print(format("Quantity", "12"),end='')
    print(format("Price", "12"),end='')
    print("Extended Price")
    print("--------------------------------------------------------------------")

    for num in transaction_list:
        print(format(num.get_id(),"<6"), end='')
        print(format(num.get_name(), "25"), end='')
        print(format(num.get_qty(),"<9"), end='')
        #creates running total for quantity
        total_qty += num.get_qty()
        print("$",format(num.get_price(),"<11"), sep='', end='')
        print("$",format(num.get_cost(), '.2f'), sep='')
        #creates running total for subtotal
        subtotal += num.get_cost()

    #calculates the cost of tax
    tax_total = TAX_RATE*subtotal
    #gets the total cost
    grand_total = subtotal + tax_total
    print("\nTotal Items: ", total_qty)
    print("Subtotal: $", format(subtotal, '.2f'), sep='')
    print("Sales Tax: $", format(tax_total, '.2f'), sep='')
    print("Grand Total: $", format(grand_total, '.2f'), sep='')


#call main
main()
