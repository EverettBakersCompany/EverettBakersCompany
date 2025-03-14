from Conection import *

class Messages ():
    def addMessageUser (self, message, user_id):
        query = f"INSERT INTO Messages (sender_id, to_id, message, type) VALUES ({user_id}, 4, '{message}', 'user');"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

    def addMessageAdm (self, message, user_id):
        query = f"INSERT INTO Messages (sender_id, to_id, message, type) VALUES ({user_id}, {4}, '{message}', 'adm');"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

    def deleteMessage (self, user_id):
        query = f"DELETE FROM Messages WHERE sender_id = {user_id};"
        conexao = Conection()
        response = conexao.add_query(query)
        return response

    def getMessages(self):
        # Consulta SQL para obter todas as mensagens, incluindo o tipo
        query = """
            SELECT Messages.id, Messages.sender_id, User.name, Messages.to_id, Messages.message, Messages.type
            FROM Messages
            INNER JOIN User ON Messages.sender_id = User.id
            ORDER BY Messages.id ASC
        """

        # Conectar ao banco e buscar os dados
        conexao = Conection()
        messages = conexao.get_list(query)

        # Dicionário para agrupar mensagens pelo sender_id
        grouped_messages = {}

        for msg in messages:
            msg_id, sender_id, sender_name, to_id, message, msg_type = msg

            # Criar objeto da mensagem
            message_obj = {
                "id": msg_id,
                "sender_id": sender_id,
                "sender_name": sender_name,
                "to_id": to_id,
                "message": message,
                "type": msg_type
            }

            # Criar chave única baseada apenas no sender_id
            key = sender_id

            # Criar lista para armazenar mensagens desse usuário se ainda não existir
            if key not in grouped_messages:
                grouped_messages[key] = []

            # Adicionar a mensagem ao grupo correspondente
            grouped_messages[key].append(message_obj)

        # Converter os valores do dicionário para uma lista e ordenar cada grupo por ID
        grouped_list = [sorted(msgs, key=lambda x: x["id"]) for msgs in grouped_messages.values()]

        print(grouped_list)

        # Retornar a lista de grupos organizados
        return grouped_list

    def getMessagesID(self, user_id):
        # Consulta SQL para obter todas as mensagens do usuário específico
        query = f"""
            SELECT Messages.id, Messages.sender_id, User.name, Messages.to_id, Messages.message, Messages.type
            FROM Messages
            INNER JOIN User ON Messages.sender_id = User.id
            WHERE Messages.sender_id = {user_id}
            ORDER BY Messages.id ASC
        """

        # Conectar ao banco e buscar os dados
        conexao = Conection()
        messages = conexao.get_list(query)

        # Lista para armazenar as mensagens do usuário
        user_messages = []

        for msg in messages:
            msg_id, sender_id, sender_name, to_id, message, msg_type = msg

            # Criar objeto da mensagem
            message_obj = {
                "id": msg_id,
                "sender_id": sender_id,
                "sender_name": sender_name,
                "to_id": to_id,
                "message": message,
                "type": msg_type
            }

            # Adicionar à lista apenas se o sender_id for igual ao user_id
            user_messages.append(message_obj)

        # Ordenar as mensagens pelo ID em ordem crescente
        user_messages.sort(key=lambda x: x["id"])

        print(user_messages)

        # Retornar apenas as mensagens do usuário
        return user_messages


