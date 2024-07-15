# [] create list-o-matic as a function and call it
# [] be sure to include your spelled-out name in the welcome prompt
# [] you are welcome to use any list you like for list-o-matic, does not have to be animals 

# Define the list-o-matic function
def list_o_matic(item, lst):
    if item == "":
        if len(lst) > 0:
            removed_item = lst.pop()
            return removed_item + " popped from list"
        else:
            return "The list is already empty"
    elif item in lst:
        lst.remove(item)
        return "1 instance of " + item + " removed from list"
    else:
        lst.append(item)
        return "1 instance of " + item + " appended to list"

# Initialize a list with several strings
animals = ['cat', 'goat', 'cat']

# Welcome message with your full name
print("Welcome, Aayush Patel. Look at all the animals " + str(animals))

while True:
    # Prompt the user to enter the name of an animal
    animal = input("Enter the name of an animal (or 'quit' to end): ").strip()

    # Check if the user wants to quit
    if animal.lower() == "quit":
        print("Goodbye!")
        break

    # Call the list-o-matic function and print the result
    result = list_o_matic(animal, animals)
    print(result)

    # Print the updated list of animals
    print("Look at all the animals " + str(animals))

    # End the program if the list is empty
    if len(animals) == 0:
        print("Goodbye!")
        break


