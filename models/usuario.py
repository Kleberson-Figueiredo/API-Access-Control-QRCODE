from sql_alchemy import banco
from datetime import datetime

class UserModel(banco.Model):
    __tablename__ = 'usuario'

    usuario_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    nome = banco.Column(banco.String(80))
    datacad = banco.Column(banco.DateTime, default=datetime.now().replace(microsecond=0))
    perfil = banco.Column(banco.Integer)

    def __init__(self, login, senha, nome, perfil):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.perfil = perfil

    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'nome': self.nome,
            'datacad': self.datacad.strftime("%d/%m/%Y %H:%M:%S"),
            'perfil': self.perfil
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(usuario_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def get_users(cls):
        user = cls.query.all()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        login = cls.query.filter_by(login=login).first()
        if login:
            return login
        return None
    
    @classmethod
    def Checking_Permission(cls, usuario_id):
        usuario_id = cls.query.filter_by(usuario_id=usuario_id, perfil=0).first()
        if usuario_id:
            return usuario_id
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def update_user(self,senha):
        self.senha = senha
    
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()