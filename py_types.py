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

# def process_items(prices: dict[str, float]):
#     for item_name, item_price in prices.items():
#         print(item_name)
#         print(item_price)

# Dict: Python's efficient key/value hash table structure is called a "dict". The contents of a dict can be written as a series of key:value pairs within braces { }

# This means:
# The variable prices is a dict:
# The keys of this dict are of type str (let's say, the name of each item).
# The values of this dict are of type float (let's say, the price of each item).

# You can declare that a variable can be any of several types, for example, an int or a str.
# In Python 3.6 and above (including Python 3.10) you can use the Union type from typing and put inside the square brackets the possible types to accept.
# In Python 3.10 there's also a new syntax where you can put the possible types separated by a vertical bar (|).

# def process_item(item: int | str):
#     print(item)

# In both cases this means that item could be an int or a str.

# You can declare that a value could have a type, like str, but that it could also be None.
# In Python 3.6 and above (including Python 3.10) you can declare it by importing and using Optional from the typing module.

# from typing import Optional

# def say_hi(name: Optional[str] = None):
#     if name is not None:
#         print(f"Hey {name}!")
#     else:
#         print("Hello World")

# Using Optional[str] instead of just str will let the editor help you detecting errors where you could be assuming that a value is always a str, when it could actually be None too.
# Optional[Something] is actually a shortcut for Union[Something, None], they are equivalent.
# This also means that in Python 3.10, you can use Something | None:

# def say_hi(name: str | None = None):
#     if name is not None:
#         print(f"Hey {name}!")
#     else:
#         print("Hello World")


# say_hi("Noah")

# You can also declare a class as the type of a variable.
# Let's say you have a class Person, with a name:
# class Person:
#     def __init__(self, name: str):
#         self.name = name
# # Then you can declare a variable to be of type Person:

# def get_person_name(one_person: Person):
#     print(one_person.name)

# # And then, again, you get all the editor support

# # Notice that this means "one_person is an instance of the class Person".
# # It doesn't mean "one_person is the class called Person".

# Noah = Person("Noah")

# get_person_name(Noah)

# Pydantic is a Python library to perform data validation.
# You declare the "shape" of the data as classes with attributes.
# And each attribute has a type.
# Then you create an instance of that class with some values and it will validate the values, convert them to the appropriate type (if that's the case) and give you an object with all the data.
# And you get all the editor support with that resulting object.
# An example from the official Pydantic docs:

# from datetime import datetime

# from pydantic import BaseModel


# class User(BaseModel):
#     id: int
#     name: str = "John Doe"
#     signup_ts: datetime | None = None
#     friends: list[int] = []


# external_data = {
#     "id": "123",
#     "signup_ts": "2017-06-01 12:22",
#     "friends": [1, "2", b"3"],
# }
# user = User(**external_data)
# print(user)
# print(user.id)