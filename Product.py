from Conection import *

class Product:
    def getProducts(self):
        query = '''
        SELECT 
            Products.id, 
            Products.name, 
            Products.type, 
            Products.price, 
            Products.image, 
            Type.name as type_name
        FROM 
            Products
        INNER JOIN 
            Type ON Products.type = Type.id;
        '''

        conexao = Conection()
        exis = conexao.get_list(query)

        arrayObj = []
        for i in exis:
            objTransition = {
                'id': i[0],
                'name': i[1],
                'price': i[3],
                'imgSrc': i[4],
                'type': i[5]  # Adicionando o nome do tipo ao objeto
            }
            arrayObj.append(objTransition)

        print(arrayObj)
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