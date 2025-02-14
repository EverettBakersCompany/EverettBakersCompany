from flask import Flask,request, jsonify
from flask_cors import CORS
import os
import smtplib
import smtplib
import email.message
import jwt
import json
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from datetime import date, timedelta, datetime
from dateutil import parser as date_parser
import hashlib
import random


from User import *
from Token import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#constantes
secretKey = '711641683'

@app.route('/')
def init ():
    return jsonify({'init': 'init test'})

@app.route('/register', methods=['POST'])
def register ():
    name = request.json.get('name')
    Email = request.json.get('email')
    Password = request.json.get('password')
    # consumer = request.json.get('consumer')
    # delivery = request.json.get('delivery')
    # store = request.json.get('store')
    # driverLicence = request.json.get('driverLicence')
    # birth = request.json.get('birth')
    # userId = request.json.get('userId')
    # storeRegister = request.json.get('storeRegister')

    print(name, Email, Password)

    # verificando se o cadastro já existe
    user = User(Email)
    check = user.checkUser()
    print(check)
    if check:
        return jsonify({"status": "usuário já cadastrado"})
    else:
        # cadastrando usuário
        # user.add_user()
        # id = user.checkUser()[0]
        # config = Config(user.checkUser()[0])
        # config.criarCampos()

        # gerar token para verificação de email
        # gerar code
        code = random.randint(1000, 100000)
        print(code)

        # enviar email
        corpo_email = f"<p>Olá, esse é seu código de verificação é <b>{code}</b>, ele vai expirar em 5 minutos</p>"

        msg = email.message.Message()
        print(msg)
        msg['Subject'] = "Código Everett"
        msg['From'] = 'everettbakersco@gmail.com'
        msg['To'] = f'{Email}'
        password = 'dhly dmqw hhgk ddvc'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # entrando com as credenciais
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        global secretKey
        payload = {'code': code, 'nome': name, 'email': Email, 'senha': Password}
        token = jwt.encode(payload, secretKey, algorithm='HS256')

        # calculo de vencimento
        to_day = datetime.now()
        td = timedelta(minutes=5)

        print(to_day + td)

        print({'status': True, 'resp': {'key': token, 'down': to_day + td}})
        return jsonify({'status': True, 'resp': {'key': token, 'down': to_day + td}})


@app.route('/confirmRegister', methods=['POST'])
def confirmRegister ():
    code = request.json.get('code')
    tok = request.json.get('token')

    payload = jwt.decode(tok['key'], secretKey, algorithms=['HS256'])
    print(payload)
    print(type(payload['code']),type(code))

    code = int(code)
    if payload['code'] == code:
        #hash senha
        intergerSenha = random.randint(10000, 1000000)
        print(intergerSenha)
        passwordInteger = payload['senha'] + str(intergerSenha)
        password = hash_string(passwordInteger)
        print(password)

        user = User(payload['email'], password, payload['nome'], 'test', intergerSenha)
        user.add_user()
        id = user.checkUser()[0]

        resp = Token(id, secretKey)
        resposta = resp.cadastrarToken(payload['email'])

        return jsonify({'status': True, 'resp': resposta})
    else:
        return jsonify({'status': 'código errado'})

@app.route('/login', methods=['POST'])
def login ():
    Email = request.json.get('email')
    Password = request.json.get('password')

    print(Email, Password)
    user = User(Email, Password)
    check = user.loginUser()
    print(check)

    if check:
        # gerar token
        global secretKey
        # resp = Token(check[0], secretKey)
        # resposta = resp.cadastrarToken(check[1])

        #gerar código de login
        code = random.randint(1000, 100000)
        print(code)

        # enviar email
        corpo_email = f"<p>Olá, seu código de verificação é <b>{code}</b>, ele vai expirar em 5 minutos</p>"

        msg = email.message.Message()
        print(msg)
        msg['Subject'] = "Código Everett"
        msg['From'] = 'everettbakersco@gmail.com'
        msg['To'] = f'{Email}'
        password = 'dhly dmqw hhgk ddvc'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # entrando com as credenciais
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        global secretKey
        payload = {'code': code, 'id': check[0], 'email': check[1]}
        token = jwt.encode(payload, secretKey, algorithm='HS256')

        # calculo de vencimento
        to_day = datetime.now()
        td = timedelta(minutes=5)

        print(to_day + td)

        print({'status': True, 'resp': {'key': token, 'down': to_day + td}})
        return jsonify({'status': True, 'resp': {'key': token, 'down': to_day + td}})

    return jsonify({"status": "o usuário ou a senha estão incorretos"})

@app.route('/confereLog', methods=['POST'])
def confereLog ():
    code = request.json.get('code')
    tok = request.json.get('token')

    payload = jwt.decode(tok['key'], secretKey, algorithms=['HS256'])
    print(payload)
    print(type(payload['code']),type(code))

    code = int(code)
    if payload['code'] == code:
        #definir login
        resp = Token(payload['id'], secretKey)
        resposta = resp.cadastrarToken(payload['email'])

        return jsonify({'status': True, 'resp': resposta})
    else:
        return jsonify({'status': 'código errado'})

@app.route('/confirmAdm', methods=['POST'])
def confirmAdm ():
    pack = request.json.get('token')
    token = pack['key']

    # descriptografando o token de acesso
    global secretKey
    try:
        payload = jwt.decode(token, secretKey, algorithms=['HS256'])  # Token válido, realizar ações necessárias

        user = User(payload['email'])
        permission = user.checkUserPermission()

        print(payload)
        print(permission[0])

        if permission[0] == 'admin':
            return jsonify({'status': True})
        return jsonify({'status': False })
    except ExpiredSignatureError:  # Token expirado, tratar de acordo com as regras da aplicação
        return jsonify({'status': False})
    except InvalidSignatureError:  # Token inválido, tratar de acordo com as regras da aplicação
        return jsonify({'status': False})


@app.route('/verificaToken', methods=['POST'])
def verificaToken ():
    code = request.json.get('token')
    token = Token()
    response = token.trazerCorrespondencias(code)
    print(response[1],date.today())
    if response:
        if response[1] < date.today():
            token.excluirToken(response[0])
            return jsonify({'status': False})

        return jsonify({'status': True})
    return jsonify({'status': False})

@app.route('/deleteToken', methods=['POST'])
def excluiToken ():
    code = request.json.get('key')
    print(code)
    token = Token()
    response = token.excluirToken(code)

    if response:
        return jsonify({'status': True})
    return jsonify({'status': False})


@app.route('/code', methods=['POST'])
def code ():
    emailFront = request.json.get('Email')
    #conferir emai
    user = User(emailFront)
    exist = user.checkUser()

    if exist:
        #gerar code
        code = random.randint(1000, 100000)
        print(code)

        #enviar email
        corpo_email = f"<p>Olá, esse é seu código de verificação é <b>{code}</b>, ele vai expirar em 5 minutos</p>"

        msg = email.message.Message()
        print(msg)
        msg['Subject'] = "Código Adapt.AI"
        msg['From'] = 'adapt.AiEducation@gmail.com'
        msg['To'] = f'{emailFront}'
        password = 'yxfi sovv kztw tgml'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # entrando com as credenciais
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        global secretKey
        payload = {'code': code}
        token = jwt.encode(payload, secretKey, algorithm='HS256')

        # calculo de vencimento
        to_day = datetime.now()
        td = timedelta(minutes=5)

        print(to_day + td)

        print({'status': True, 'resp': {'key': token, 'down': to_day + td}})
        return jsonify({'status': True, 'resp': {'key': token, 'down': to_day + td}})

    return jsonify({'status': 'email não encontrado'})

@app.route('/verifica', methods=['POST'])
def verifica ():
    global secretKey
    code = request.json.get('code')
    code = int(code)
    validation = request.json.get('validation')
    token = validation['key']
    payload = jwt.decode(token, secretKey, algorithms=['HS256'])

    if payload['code'] == code:
        to_day = datetime.now()
        td = timedelta(minutes=5)
        return jsonify({'status': True, 'resp': to_day + td})
    else:
        return jsonify({'status': False, 'resp': 'código espirado ou incorreto'})

@app.route('/changeWord', methods=['POST'])
def changeWord ():
    email = request.json.get('email')
    password  = request.json.get('senha')

    intergerSenha = random.randint(10000, 1000000)
    passwordInteger = password + str(intergerSenha)
    password = hash_string(passwordInteger)

    user = User(email)
    response = user.mudarSenha(password, intergerSenha)
    print(response)
    return jsonify({'status': response})

@app.route('/senhaCheck', methods=['POST'])
def senhaCheck ():
    senha = request.json.get('senha')
    token = request.json.get('token')

    if tokenValidation(token):
        email, id = tokenValidation(token, True)
        user = User(email)
        response = user.getSenha()

        print(response)
        print(senha)

        if response:
            print(response[0] == senha)
            if response[0] == senha:
                print('é igual')
                to_day = datetime.now()
                td = timedelta(minutes=5)
                return jsonify({'status': True, 'resp': to_day + td})
            return jsonify({'status': 'as senha não batem'})
        else:
            print('nn é')
            return jsonify({'status': response})
    else:
        return jsonify({'staus': 404, 'resp': 'token vencido ou inválido'})

@app.route('/geraCodeEmail', methods=['POST'])
def geraCodeEmail ():
    emailFront = request.json.get('email')
    # conferir emai
    user = User(emailFront)
    exist = user.checkUser()

    if exist:
        return jsonify({'status': 'esse email já está cadastrado em uma conta'})
    else:
        # gerar code
        code = random.randint(1000, 100000)
        print(code)

        # enviar email
        corpo_email = f"<p>Olá, esse é seu código de verificação é <b>{code}</b>, ele vai expirar em 5 minutos</p>"

        msg = email.message.Message()
        print(msg)
        msg['Subject'] = "Código Adapt.AI"
        msg['From'] = 'adapt.AiEducation@gmail.com'
        msg['To'] = f'{emailFront}'
        password = 'yxfi sovv kztw tgml'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # entrando com as credenciais
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        global secretKey
        payload = {'code': code, 'email': emailFront}
        token = jwt.encode(payload, secretKey, algorithm='HS256')

        # calculo de vencimento
        to_day = datetime.now()
        td = timedelta(minutes=5)

        print(to_day + td)

        print({'status': True, 'resp': {'key': token, 'down': to_day + td}})
        return jsonify({'status': True, 'resp': {'key': token, 'down': to_day + td}})

@app.route('/confereCodeEmail', methods=['POST'])
def confereCodeEmail ():
    global secretKey

    code = request.json.get('code')
    code = int(code)
    validation = request.json.get('token')
    userInfo = request.json.get('userInfo')
    token = validation['key']
    payload = jwt.decode(token, secretKey, algorithms=['HS256'])

    if payload['code'] == code and tokenValidation(userInfo):
        email, id = tokenValidation(userInfo, True)
        user = User(email)
        response = user.setEmail(payload['email'])

        if response:
            load = {'user_id': id, 'email': payload['email']}
            tokenuser = jwt.encode(load, secretKey, algorithm='HS256')

            # calculo de vencimento
            to_day = date.today()
            td = timedelta(7)

            return jsonify({'status': True, 'resp': {'key': tokenuser, 'down': to_day + td}})
        return jsonify({'status': response})
    else:
        return jsonify({'status': False, 'resp': 'código espirado ou incorreto'})

#funções avulsas
def tokenValidation (token, mandar=False):
    chave = token['key']
    vencimento = token['down']

    #checando data
    to_day = datetime.today()
    vence = date_parser.parse(vencimento)
    vence = datetime.date(vence)
    to_day = datetime.date(to_day)

    if to_day > vence:
        print('token vencido')
        return False
    else:
        print('token dentro da data')
        payload = jwt.decode(chave, secretKey, algorithms=['HS256'])
        user = User(payload['email'])
        if user.checkUser():
            if mandar:
                return payload['email'], payload['user_id']
            else:
                return True
        else:
            return False

def hash_string(string):
    hash_object = hashlib.sha256(string.encode())
    return hash_object.hexdigest()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))