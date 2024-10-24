from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.cliente import (Clientes, Cliente, Update_Cliente, Cancels_Appointment,
                                DownloadClientes, Status_Clients)
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from resources.qrcode import ValidQrcode
from flask_jwt_extended import JWTManager
#from config import *
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco.db" #f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "JWT_SECRET_KEY"
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=5)
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Caminho do cookie
app.config['JWT_ACCESS_COOKIE_NAME'] = 'token'  # Nome do cookie
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Onde procurar o token
app.config['JWT_CSRF_PROTECT'] = False  # Ativa a proteção CSRF para rotas que utilizam cookies
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 

CORS(app, supports_credentials=True)
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.unauthorized_loader
def handle_unauthorized_loader(reason):
    return jsonify({
        "message": "Missing or invalid JWT token. Please provide a valid token.",
        "reason": reason
    }), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "message": "Token has expired, please log in again."
    }), 401

@jwt.revoked_token_loader
def token_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have benn logged out'}), 401


api.add_resource(Clientes, '/clientes')
api.add_resource(Cliente, '/cadcliente')
api.add_resource(Update_Cliente, '/cliente/<int:cliente_id>')
api.add_resource(Cancels_Appointment, '/cancellation/<int:cliente_id>')
api.add_resource(User, '/usuario')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(ValidQrcode, '/qrcode')
api.add_resource(DownloadClientes, '/clientes/download')
api.add_resource(Status_Clients, '/status')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5000)