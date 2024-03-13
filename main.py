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

# def get_name_with_age(name: str, age: int):
#     """Function showing error checking"""
#     name_with_age = name + " is this old: " + str(age)
#     return name_with_age


# print(
#     get_name_with_age("Noah Bruce", 27))

# def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
#     """Returning all item types"""
#     return item_a, item_b, item_c, item_d, item_d, item_e

# data = bytes([120, 110, 100, 97, 111])

# print(get_items("Noah", 27, 27.11, True, data))

# def process_items(items: list[str]):
#     for item in items:
#         print(item.title())

# That means: "the variable items is a list, and each of the items in this list is a str".
# By doing that, your editor can provide support even while processing items from the list:
# Without types, that's almost impossible to achieve.
# Notice that the variable item is one of the elements in the list items.
# And still, the editor knows it is a str, and provides support for that.

# def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
#     return items_t, items_s

# Tuple: Tuples are immutable, meaning they cannot be changed once they are created. This makes them ideal for storing data that should not be modified, such as database records.
# Sets: Set is a data type in python used to store several items in a single variable. It is a collection that is written with curly brackets and is both unindexed and unordered.

# To define a dict, you pass 2 type parameters, separated by commas.
# The first type parameter is for the keys of the dict.
# The second type parameter is for the values of the dict:

def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)

# Dict: Python's efficient key/value hash table structure is called a "dict". The contents of a dict can be written as a series of key:value pairs within braces { }

# This means:
# The variable prices is a dict:
# The keys of this dict are of type str (let's say, the name of each item).
# The values of this dict are of type float (let's say, the price of each item).