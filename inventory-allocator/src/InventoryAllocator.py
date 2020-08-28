from typing import Dict, List, Any
import copy

from Warehouse import Warehouse

#goal: produce cheapest shipment given the orders and warehouses' inventory

'''
This class provides the functions to find the cheapest shipments given an inventory distribution
Methods:
    1. __init(self, order, warehouses) - initializes the attributes of the class
    2. optimizeOrder(self) - calculates the cheapest shipment of goods

Attributes:
    1.  _order - the current order that determines what will be ordered from the warehouses
    2. _warehouses - the list of warehouse objects that contains items that can potentially fulfill the order
'''
class InventoryAllocator:


    # This function initializes the attributes (_order, _warehouses) of the class
    # @param order - type Dict[string, integer]
    # @param warehouses - type List[Dict[str, Any]]
    # returns nothing
    def __init__(self, order: Dict[str, int], warehouses: List[Dict[str, Any]]):
        self._order = order
        self._warehouses = []

        #Fill the _warehouses attribute with Warehouse objects
        for warehouse_dict in warehouses:
            self._warehouses.append(Warehouse(warehouse_dict))

    # This function uses the attributes of its parent class to calculate the most optimal shipment goods
    # returns List[Dict[string, Any]]
    def optimizeOrder(self) -> List[Dict[str, Any]]:
        #simply the names of the attributes
        order = self._order
        warehouses = self._warehouses

        #return empty array if order and/or warehouses is empty or if order has negative values
        if len(order) == 0 or len(warehouses) == 0 or not all(val >= 0 for val in order.values()):
            return []

        #save  the original order because it will be changed
        origin_order = copy.copy(order) 

        #count of items that has been fulfilled by the inventory distribution
        order_items_fulfilled = 0

        #count of items with 0 as values to accomodate for the case when one of the orders has the value of 0
        order_items_zeros = sum(1 for i in order.values() if i == 0) 

        #list of dictionaries of the warehouses and the quantity to be ordered from them.
        #This is the variable that is returned unless one warehouse is able to fully fulfill the entire order
        order_shipment = []

        for warehouse in warehouses:
            #the current shipment of items that warehouses can provide for the orders
            warehouse_shipment = {} 
            warehouse_shipment[warehouse._name] = dict()
            
            #keeps track of the number of items the warehouse can fulfill from the original, unmodified order
            origin_items_fulfilled = 0 

            for item, stock in warehouse._inventory.items():
                #if an item in the warehouse inventory is not wanted in the order, then move to the next item
                if item not in order:
                    continue
                
                #if current warehouse can fulfill an item shipment from the original, unmodified order, then increment origin_items_fulfilled
                if stock >= origin_order[item]:
                    origin_items_fulfilled += 1

                #if the quantities of an item in both the warehouse and the order is not 0 then do logic
                if order[item] > 0 and stock > 0:                    
                    #if warehouse' stock is less than the order's request for that item, that means the warehouse will run out of that item to provide for the order
                    if stock < order[item]: 
                        order[item] -= stock
                        warehouse._inventory[item] = 0
                    #if warehouse' stock is greater than or equal to the order's request for that item, then that means the one item request on the order has been fulfilled
                    else:
                        warehouse._inventory[item] -= order[item]
                        order[item] = 0
                        order_items_fulfilled += 1

                    #save the item name and the quantity that the warehouse can provide
                    warehouse_shipment[warehouse._name][item] = stock - warehouse._inventory[item]
            
            #if current warehouse can fully fulfill the order, return original order with the warehouse's name
            if origin_items_fulfilled == len(origin_order):
                return [{warehouse._name: origin_order}]

            #if the current warehouse can provide some items for the shipments, then append those items to the resultant list
            if len(warehouse_shipment[warehouse._name]) > 0:
                order_shipment.append(warehouse_shipment)

        #sort alphabetically by warehouse name
        order_shipment.sort(key = lambda x: list(x.keys())[0])

        #if the total number of items fulfilled by the warehouses and the number of items that originally had 0 as their quantity requested is equal to the number of items
        #requested in the order, then return the derived shipment from the warehouses, else that means cases failed so return an empty
        order_shipment = order_shipment if (order_items_fulfilled + order_items_zeros) == len(order) else []

        return order_shipment