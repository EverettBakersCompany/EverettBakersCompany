from Conection import *
from Items import *

class Orders ():
    def __init__(self, address = '', schedule = '', idUser = ''):
        self.address = address
        self.schedule = schedule
        self.idUser = idUser

    def addOrder (self, items):
        query = f"INSERT INTO Orders (user_id, address, schedule) VALUES ({self.idUser}, '{self.address}', '{self.schedule}');"
        conexao = Conection()
        responseOrder = conexao.query_last_id(query)
        if responseOrder:
            iten = Items(items)
            responseIten = iten.add_items(responseOrder)
            return responseIten
        return responseOrder

    def getOrders(self):
        # Consulta SQL atualizada com JOIN para pegar o nome do usuário
        query = """SELECT Orders.*, User.name AS customer_name, GROUP_CONCAT(Items.product_id) AS product_ids FROM Orders LEFT JOIN User ON Orders.user_id = User.id LEFT JOIN Items ON Orders.id = Items.order_id GROUP BY Orders.id"""

        # Conectar ao banco e buscar os dados
        conexao = Conection()
        exis = conexao.get_list(query)

        # Lista final para armazenar os pedidos processados
        finalL = []

        # Processar cada pedido
        for order in exis:
            order_id, user_id, address, schedule, customer_name, product_ids = order[:6]  # Pegando os campos relevantes

            # Converter a string de IDs de produtos para uma lista de inteiros
            product_ids_array = [int(product_id) for product_id in product_ids.split(',')] if product_ids else []

            # Criar nova estrutura de pedido com o nome do usuário incluso
            new_order = (order_id, customer_name, address, schedule, product_ids_array)  # Substituí user_id pelo nome

            # Adicionar o pedido modificado à lista final
            finalL.append(new_order)

        # Exibir a lista final para depuração
        print("Pedidos com produtos e nome do cliente:", finalL)

        # Retornar a lista modificada
        return finalL

    def deleteOrders(self, orderId):
        query = f"DELETE FROM Orders WHERE id = {orderId};"
        conexao = Conection()
        response = conexao.add_query(query)
        if response:
            item = Items().deleteItem(orderId)
            return item
        return response

