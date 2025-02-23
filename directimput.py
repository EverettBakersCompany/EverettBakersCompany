from Conection import *
query = f"ALTER TABLE Products DROP COLUMN rating;"
conexao = Conection()
response = conexao.add_query(query)
