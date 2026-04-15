dict = { 
    'Hot coffee' : 200,
    'Cold coffe' : 300,
    'Mojito' : 190,
    'Pasta' : 200
}
print(f"Welcome to Kuhu Cafe")
print("Hot coffee : Rs200\nCold coffee : Rs300\nMojito : Rs190\nPasta : Rs200")
order_total = 0

user_1 = input('Please give your 1st order:')
if user_1 in dict:
    order_total += dict[user_1] 
    print(f"Your item {user_1} has been added to your order!")

else:
    print('Sorry,ordered item is not available')

another = input('Do you want anything else? (Yes/No)')
if another == "Yes":
    user_2 = input('Please give your 2nd order:')
    if user_2 in dict:
        order_total += dict[user_2]
        print(f"Your item {user_2} has been added to your order!")
    else:
        print('Sorry,ordered item is not available')

print(f"Total amount of item is {order_total}")
print('Thank You!,Visit again')