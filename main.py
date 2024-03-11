def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))

# The function does the following:

# Takes a first_name and last_name.
# Converts the first letter of each one to upper case with title().
# Concatenates them with a space in the middle.