#Author: Jordan Ehlinger
#Assignment Number & Name: Validation
#Due Date: N/A
#Program Description: Validation class that holds method to validate integer


#create validation class
class ValidationClass:          
    #input validation function for checking an integer
    def checkInteger(self, input_value):
        try:
            integer_value = int(input_value)
        except:
            return -1

        #check if input is positive
        if integer_value < 0:
            return -1
        else:
            return integer_value
