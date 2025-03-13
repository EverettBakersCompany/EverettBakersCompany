from Conection import *
from Product import *

class Items ():
    def __init__(self, itens = ''):
        self.itens = itens

    def add_items (self, order_id):
        response = ''
        for i in self.itens:
            query = f"INSERT INTO Items (order_id, product_id) VALUES ({order_id}, {i});"
            conexao = Conection()
            response = conexao.add_query(query)
        return

    def getItem (self, orderId):
        query = f'SELECT product_id FROM `Items` WHERE order_id = {orderId};'
        conexao = Conection()
        exis = conexao.get_list(query)
        finalList = []
        for i in exis:
            finalList.append(i[0])
        print(finalList)
        return finalList

    def deleteItem (self, orderId):
        query = f"DELETE FROM `Items` WHERE order_id = {orderId};"
        conexao = Conection()
        response = conexao.add_query(query)
        return response