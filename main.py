# def get_full_name(first_name: str, last_name: str):
#     full_name = first_name.title() + " " + last_name.title()
#     return full_name

# print(get_full_name("john", "doe"))

# The function does the following:

# Takes a first_name and last_name.
# Converts the first letter of each one to upper case with title().
# Concatenates them with a space in the middle.

# It's a different thing.

# We are using colons (:), not equals (=).

# And adding type hints normally doesn't change what happens from what would happen without them.

# But now, imagine you are again in the middle of creating that function, but with type hints.

# At the same point, you try to trigger the autocomplete with Ctrl+Space and you see:

# With that, you can scroll, seeing the options, until you find the one that "rings a bell":

def get_name_with_age(name: str, age: int):
    """Function showing error checking"""
    name_with_age = name + " is this old: " + age
    return name_with_age
