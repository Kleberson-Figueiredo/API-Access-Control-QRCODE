from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import (get_jwt,create_access_token, 
    jwt_required, get_jwt_identity, unset_jwt_cookies
)
from werkzeug.security import safe_join
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank")
args.add_argument('senha', type=str, required=True,
                       help="The field 'senha' cannot be left blank")
args.add_argument("nome", type=str, required=True, 
                       help="The field 'nome' cannot be left blank")
args.add_argument("perfil",type=int, required=True, 
                       help="The field 'perfil' cannot be left blank")

class User(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity() 
        user = UserModel.find_user(user_id)  
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        permission = UserModel.Checking_Permission(user_id)
        if permission:
            
            data = args.parse_args()

            if UserModel.find_by_login(data['login']):
                return {"message": f"The login '{(data['login'])}' already exists"},400 

            user = UserModel(**data)
            user.save_user()
            return {"message": "User created succesfully"}, 201
        else:
            return {"message": "user does not have permission"}, 403


class UserLogin(Resource):
    args = reqparse.RequestParser()
    args.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank")
    args.add_argument('senha', type=str, required=True,
                       help="The field 'senha' cannot be left blank")

    @classmethod
    def post(cls):
        data = UserLogin.args.parse_args()
        user = UserModel.find_by_login(data["login"])

        if user and safe_join(user.senha, data['senha']): 
            access_token = create_access_token(identity=user.usuario_id)
            response = make_response(jsonify(user.json()))
            response.set_cookie('token', access_token, httponly=True, path="/", secure=True, samesite="None")
            return response
        return {"message": "The username or password is incorrect."}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        response = jsonify({"message": "Logged out successfull!y"}, 200)
        BLACKLIST.add(jwt_id)
        unset_jwt_cookies(response)
        return response