from Conection import *
import jwt
from datetime import date, timedelta


class Token:
    def __init__(self, fk = 0, key = 0):
        self.key = key
        self.fk = fk

    def cadastrarToken (self, email):
        # calculo de vencimento
        to_day = date.today()
        td = timedelta(7)

        encoder = {'user_id': self.fk, 'email': email}
        print(encoder)
        token = jwt.encode(encoder, self.key, algorithm='HS256')

        print(token)

        query = f"INSERT INTO Token (fk, code, vencimento) VALUES ('{self.fk}', '{token}', '{to_day + td}');"
        conexao = Conection()
        response = conexao.add_query(query)
        print(response)
        if response:
            resposta = {'key': token, 'down': to_day + td}
            return resposta
        return response

    def trazerCorrespondencias (self, code):
        query = f'SELECT code, vencimento, fk FROM `Token` WHERE code = "{code}";'
        conexao = Conection()
        exis = conexao.get_query(query)
        return exis

    def excluirToken (self, code):
        query = f'DELETE FROM `Token` WHERE code = "{code}";'
        conexao = Conection()
        response = conexao.add_query(query)
        return response