from Conection import *

class Type():
    def __init__(self, id = 0):
        self.id = id

    def getTypeId (self):
        query = f'SELECT name FROM `Type` WHERE id = {self.id};'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis[0]

    def getTypeName (self, name):
        query = f'SELECT id FROM `Type` WHERE name = "{name}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis[0]

    def getTypeNames (self):
        query = f'SELECT name FROM `Type` ;'
        conexao = Conection()
        exis = conexao.get_list(query)

        passList = []
        for i in exis:
            passList.append(i[0])
        return passList