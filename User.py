from Conection import *
import hashlib

class User:
    def __init__(self,email, password ='', name = '', user = 'test', authentic = 0):
        self.name = name
        self.user = user
        self.password = password
        self.email = email
        self.authentic = authentic

    def checkUser (self):
        query = f'SELECT id FROM `User` WHERE email = "{self.email}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis

    def checkUserName (self):
        query = f'SELECT Name FROM `User` WHERE Email = "{self.email}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis

    def checkUserPermission (self):
        query = f'SELECT permission FROM `User` WHERE Email = "{self.email}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis

    def add_user (self):
        query = f"INSERT INTO User (name, permission, password, email, authentic) VALUES ('{self.name}', '{self.user}', '{self.password}', '{self.email}', '{self.authentic}');"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

    def loginUser (self):
        query = f'SELECT authentic FROM `User` WHERE email = "{self.email}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        password = self.password + str(exis[0])
        print(password)
        password = hash_string(password)
        print(exis[0])
        print(password)
        query = f'SELECT id, email FROM `User` WHERE email = "{self.email}" && password = "{password}";'
        exis = conexao.get_query(query)
        return exis

    def mudarSenha (self, novaSenha, auti):
        query = f"UPDATE `User` SET Password = '{novaSenha}', Authentic = '{auti}' WHERE Email = '{self.email}'"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

    def mudarNome (self, novoNome):
        query = f"UPDATE `User` SET Name = '{novoNome}' WHERE Email = '{self.email}'"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

    def getSenha (self):
        query = f'SELECT Password FROM `User` WHERE Email = "{self.email}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis

    def setEmail (self, novoEmail):
        query = f"UPDATE `User` SET Email = '{novoEmail}' WHERE Email = '{self.email}'"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

def hash_string(string):
    hash_object = hashlib.sha256(string.encode())
    return hash_object.hexdigest()