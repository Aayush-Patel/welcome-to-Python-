def cheese_order(max_order=100.0, min_order=1.0, price_per_pound=8.99):
    enter_name = ("Aayush Patel")
    order_amount = float(input(enter_name + ", enter weight for cheese in numbers: "))
    if order_amount > max_order:
        print(str(order_amount) + "is more than maxmium order reguired: ")
    elif order_amount < min_order:
        print(str(order_amount) + "is less than minimun order required: ")
    else:
        total_order_cost = str (order_amount * price_per_pound)
        print(str(order_amount) + " costs $" + (str(total_order_cost)) )
        
cheese_order()