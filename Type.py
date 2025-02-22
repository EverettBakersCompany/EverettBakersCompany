from Conection import *

class Type():
    def __init__(self, id):
        self.id = id

    def getTypeId (self):
        query = f'SELECT name FROM `Type` WHERE id = {self.id};'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis[0]