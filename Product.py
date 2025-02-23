from Conection import *

class Product:
    def getProducts (self):
        query = f'SELECT * FROM `Products`;'
        conexao = Conection()
        exis = conexao.get_list(query)

        arrayObj = []
        objTransition = {}
        for i in exis:
            objTransition = {
                'id': i[0],
                'name': i[1],
                'type': i[2],
                'price': i[3],
                'imgSrc': i[4]
            }
            arrayObj.append(objTransition)
        return arrayObj

    def getProductName (self, name):
        query = f'SELECT id FROM `Products` WHERE name = "{name}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis

    def cadProduct (self, name, type, price, image):
        query = f"INSERT INTO `Products` (name, type, price, image) VALUES ('{name}', {type}, {price}, '{image}');"
        conexao = Conection()
        exis = conexao.add_query(query)
        return exis