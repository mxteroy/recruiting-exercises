from typing import Dict, List, Any

'''
This class represents a warehouse

Attributes:
    1. name - the name of the warehouse
    2. inventory - the dictionary that contains the item name (key) and its quantity (value)
'''
class Warehouse:

    # This function initializes the attributes (_name, _inventory) of the class
    # @param warehouse_dict - type Dict[string, Any]
    # returns nothing
    def __init__(self, warehouse_dict: Dict[str, Any]):
        self._name = warehouse_dict['name']
        self._inventory = warehouse_dict['inventory']