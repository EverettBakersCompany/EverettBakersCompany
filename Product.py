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
                'rating': i[4],
                'imgSrc': i[5]
            }
            arrayObj.append(objTransition)
        return arrayObj