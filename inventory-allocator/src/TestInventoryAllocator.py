import unittest
from InventoryAllocator import InventoryAllocator

class TestInventoryAllocator(unittest.TestCase):
    #order can be shipped using one warehouse
    def test_one_warehouse_fulfillment(self):
        order = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 1 } }]
        answer = [{'owd': { 'apple': 1 } }]

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #order can be shipped using multiple warehouses
    def test_multiple_warehouse_fulfillment(self):
        order = {'apple': 10}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5} }, 
                       {'name': 'dm', 'inventory': {'apple': 5} }]
        answer = [{'dm': { 'apple': 5 } }, 
                  {'owd': { 'apple': 5}}]

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    # order cannot be shipped because there is not enough inventory
    def test_insufficient_inventory_1(self): 
        order = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 0 } }]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    def test_insufficient_inventory_2(self): 
        order = {'apple': 2}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 1 } }]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #the order is empty and the warehouses is
    def test_empty_order_warehouses(self):
        order = {}
        warehouses = []
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #the order and inventory is empty
    def test_empty_order_inventory(self):
        order = {}
        warehouses = [{'name': 'owd', 'inventory': {} }]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #the order is empty but inventory is not
    def test_empty_order(self):
        order = {}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5} }, 
                      {'name': 'dm', 'inventory': {'apple': 5} }]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #the order is not empty but inventory is
    def test_empty_inventory(self):
        order = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {} }]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())
    
    #the order is not empty but warehouses is
    def test_empty_warehouses(self):
        order = {'apple': 1}
        warehouses = []
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #multiple orders fulfilled by one warehouse
    def test_multiple_orders_fulfillment(self):
        order = {'apple': 4, 'banana': 3, 'jackfruit': 100000}
        warehouses = [{'name': 'wh1', 'inventory': { 'apple': 4, 'banana': 3, 'jackfruit': 100000} }]
        answer = [{'wh1': { 'apple': 4, 'banana': 3, 'jackfruit': 100000} }]

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #multiple orders fulfilled multiple warehouses
    def test_multiple_orders_warehouses_fulfillment(self):
        order = {'apple': 4, 'banana': 3, 'jackfruit': 100000}
        warehouses = [{'name': 'wh1', 'inventory': {'apple': 2, 'banana': 1, 'jackfruit': 100000}}, \
                      {'name': 'wh2', 'inventory': {'apple': 21, 'banana': 200, 'jackfruit': 0}}]
        answer = [{'wh1': { 'apple': 2, 'banana': 1, 'jackfruit': 100000}}, \
                  {'wh2': {'apple': 2, 'banana': 2}}]

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #multiple orders but some of the orders is 0
    def test_multiple_orders_partial_items_zero(self):
        order = {'apple': 10, 'orange': 0, 'banana': 0}
        warehouses = [{'name': 'wh2', 'inventory': {'apple': 6, 'banana': -2}},
                     {'name': 'wh1', 'inventory': {'apple': 5}}]
        answer = [{'wh1': {'apple': 4}}, 
                  {'wh2': {'apple': 6}}]

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #multiple orders not fulfilled (not enough inventory)
    def test_multiple_insufficient_inventory(self):
        order = {'apple': 4, 'banana': 3, 'jackfruit': 100001}
        warehouses = [ { 'name': 'wh1', 'inventory': { 'apple': 2, 'banana': 1, 'jackfruit': 100000}},
                       { 'name': 'wh2', 'inventory': {'apple': 21, 'banana': 200, 'jackfruit': 0}}]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #FAQ case: multiple orders fulfilled multiple warehouses but one warehouse is able to fulfill it
    def test_multiple_orders_warehouses_one_fulfillment(self):
        order = {'apple': 4, 'banana': 3, 'jackfruit': 100000}
        warehouses = [ { 'name': 'wh1', 'inventory': { 'apple': 2, 'banana': 1, 'jackfruit': 100000}},
                       { 'name': 'wh2', 'inventory': {'apple': 4, 'banana': 4, 'jackfruit': 200000}}]
        answer = [ { 'wh2': {'apple': 4, 'banana': 3, 'jackfruit': 100000}}]

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    
    #order cannot be shipped because the item isn't supplied by the warehouses
    def test_unsupplied_orders(self):
        order = {'firefruit': 1, 'waterfruit': 1, 'earthfruit': 1, 'airfruit': 1}
        warehouses = [{'name': 'thespiritrealm', 'inventory': {'starfruit': 420}}]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    #order has negative numbers
    def test_order_negative_number(self):
        order = {'fruit': -1}
        warehouses = [{'name': 'thespiritrealm', 'inventory': {'starfruit': 420}}]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())

    # negative numbers for inventories
    def test_inventories_negative_number(self):
        order = {'fruit': 1}
        warehouses = [{'name': 'wh1', 'inventory': {'fruit': -1}}]
        answer = []

        self.assertEqual(answer, InventoryAllocator(order, warehouses).optimizeOrder())
            

if __name__ == '__main__':
    unittest.main()