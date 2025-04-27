RED = 0
BLACK = 1

def new_node(key, value, color=RED):
    node = {
        "key": key,
        "value": value,
        "size": 1,
        "left": None,
        "right": None,
        "color": color,
        "type": "RBT",
    }

    return node

def is_red(my_node):
    red = False
    if my_node != None:
        red = my_node["color"] == RED
    return red

def get_value(my_node):
    value = None
    if my_node is not None:
        value = my_node["value"]
    return value

def get_key(my_node):
    key = None
    if my_node is not None:
        key = my_node["key"]
    return key

def change_color(my_node, color):
    my_node["color"] = color

