# [ ] create, call and test the str_analysis() function  



def str_analysis(input_string):
    if input_string.isdigit():
        number = int(input_string)
        if number > 99:
            return str(number) + " is a big number"
        else:
            return str(number) + " is a small number"
    elif input_string.isalpha():
        return '"' + input_string + '" is all alphabetical characters'
    else:
        return '"' + input_string + '" contains multiple character types'

full_name = "Aayush Patel"
while True:
    user_input = input(full_name + ", enter word or integer")
    if user_input:
        break 
print(str_analysis(user_input))
