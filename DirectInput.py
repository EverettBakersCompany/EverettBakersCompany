from Conection import *

query = f"ALTER TABLE User DROP COLUMN user_name;"
conexao = Conection()
response = conexao.add_query(query)
print(response)
