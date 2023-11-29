from inventory import MENU
from artwork import logo
from itertools import chain

resources = {  # default global variable
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}

# STATIC VARIABLES
MENU_OPTIONS = list(MENU.keys())
SECRET_OPTIONS = list(('report', 'off'))
REFILL_ERROR_MSG = ("You have used the refill option incorrectly.\n"
                    "Either enter the keyword refill by itself, or enter the keyword followed "
                    "by a number to specify how much to refill the inventory.")

# Values of coins
QUARTER_VALUE = .25
DIME_VALUE = .1
NICKEL_VALUE = .05
PENNY_VALUE = .01


# Prompt user until user gives valid answer
def prompt_customer():
    answer = ""
    valid_options = list(chain.from_iterable((MENU_OPTIONS, SECRET_OPTIONS)))
    while answer not in valid_options and not answer.startswith("refill"):  # verify user gave valid answer
        if answer != "":
            print("You chose an incorrect option. Please try again.")
        answer = input("What would you like? (espresso/latte/cappuccino): ")
    return answer


# create one long list from multiple lists
def flatten_list(matrix):
    return list(chain.from_iterable(matrix))


# Turn off coffee machine
def turn_off():
    exit()


# Refill resources
def refill(inventory: dict, response: str):
    param_list = response.split(" ")
    num_of_param = len(param_list)
    if num_of_param not in [1, 2]:  # Verify response only contains 1 or 2 strings
        print(REFILL_ERROR_MSG)
        return -1

    if num_of_param == 1:  # default to 100 if no number is given
        refill_amount = 100
    else:
        try:
            refill_amount = int(param_list[1])  # make sure second string param can be int
        except ValueError:
            print(REFILL_ERROR_MSG)
            return -1
    for item in inventory:
        if item == "money":  # don't make any changes to money on hand
            continue
        inventory[item] += refill_amount  # refill each inventory by refill amount specified
    print(f"Inventory has been refilled by {refill_amount}.")
    return inventory


# check user option and do the appropriate action
def get_drink(response: str):
    if response == "off":
        turn_off()
    elif response == "report":
        run_report()
        return -1
    elif response.startswith("refill"):
        global resources
        new_resources = refill(resources, response)
        if new_resources != -1:  # if there was an issue with the user input for refill
            resources = new_resources.copy()
        return -1
    return MENU[response]


# Print report
def run_report():
    print(f"""
    | Water: {resources["water"]}ml
    | Milk: {resources["milk"]}ml
    | Coffee: {resources["coffee"]}ml
    | Money: ${'{:.2f}'.format(resources["money"])}
    """)


# check for sufficient resources
def sufficient_inventory(ingredients: dict):
    for ingredient in ingredients:
        if resources[ingredient] < ingredients[ingredient]:
            return ingredient


# process coins
def get_money(cost_of_drink: float):
    print(f"Please insert coins. Your drink costs ${'{:.2f}'.format(cost_of_drink)}.")
    quarters_input = int(input("How many quarters? "))
    dimes_input = int(input("How many dimes? "))
    nickels_input = int(input("How many nickels? "))
    pennies_input = int(input("How many pennies? "))
    return dict(quarters=quarters_input, dimes=dimes_input, nickels=nickels_input, pennies=pennies_input)


# verify user gave enough money, calculate change and increase revenue
def calculate_money(coins: dict):
    payment_total = coins["quarters"] * QUARTER_VALUE
    payment_total += coins["dimes"] * DIME_VALUE
    payment_total += coins["nickels"] * NICKEL_VALUE
    payment_total += coins["pennies"] * PENNY_VALUE
    return payment_total


# Make sure user gave enough money
def check_money(payment, cost):
    if payment < cost:
        print("Sorry that's not enough money. Money refunded.")
        return -1
    else:
        return payment - cost  # return amount of change


# Tell user how much change they get back
def give_change(change):
    assert change >= 0
    if change > 0:
        print(f"Here is ${'{:.2f}'.format(change)} in change.")


# make the coffee, and accurate reduce inventory
def adjust_inventory(ingredients_used: dict, inventory: dict):
    for ingredient in ingredients_used:
        inventory[ingredient] -= ingredients_used[ingredient]
    return inventory


# Tell user to enjoy drink
def enjoy_drink(drink):
    print(f"Here is your {drink} ☕. Enjoy!")


print(logo)

while True:  # continue running until user turns off coffee machine
    drink_choice = prompt_customer()
    drink_details = get_drink(drink_choice)
    if drink_details == -1:  # if user made choice besides drink, ask for new choice
        continue

    missing_ingredient = sufficient_inventory(drink_details["ingredients"])
    if missing_ingredient:
        print(f"Sorry there is not enough {missing_ingredient}.")
        continue

    customer_payment = calculate_money(coins=get_money(drink_details["cost"]))
    customer_change = check_money(customer_payment, drink_details["cost"])
    if customer_change == -1:  # if user didn't give enough money, ask for new choice
        continue

    resources["money"] += drink_details["cost"]
    give_change(customer_change)
    resources = adjust_inventory(drink_details["ingredients"], resources)

    enjoy_drink(drink_choice)
