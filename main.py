from inventory import MENU
from artwork import logo

resources = {  # default global variable
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}

# TODO Prompt user until user gives valid answer
def prompt_customer():
    answer = ""
    while answer not in MENU:
        if answer != "":
            print("You chose an incorrect option. Please try again.")
        answer = input("What would you like? (espresso/latte/cappuccino): ")
    return answer

# TODO Turn off coffee machine
def turn_off():
    exit()

def get_drink(response: str):
    if response == "off":
        turn_off()
    elif response == "report":
        run_report()
    return MENU[response]

# TODO Print report
def run_report():
    pass

# TODO check for sufficient resources
def sufficient_inventory(ingredients: dict):
    for ingredient in ingredients:
        print(f"drink ingredient: {ingredients[ingredient]}, resources ingredient: {resources[ingredient]}")
        if resources[ingredient] < ingredients[ingredient]:



# TODO process coins

# TODO verify user gave enough money, calculate change and increase revenue

# TODO make the coffee, and accurate reduce inventory

# TODO Tell user to enjoy drink

print(logo)

drink_choice = prompt_customer()
drink_details = get_drink(drink_choice)
print(f"drink details: {drink_details}")
print(drink_details["ingredients"])
sufficient_inventory(drink_details["ingredients"])




#while True:
    #pass
