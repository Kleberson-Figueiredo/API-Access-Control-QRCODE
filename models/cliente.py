from sql_alchemy import banco
from datetime import datetime, timedelta
data_atual = datetime.now()
data_limite = data_atual + timedelta(days=-1)

class ClienteModel(banco.Model):
    __tablename__ = 'cliente'

    cliente_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    cpf = banco.Column(banco.String(80))
    datager = banco.Column(banco.DateTime, default=datetime.now().replace(microsecond=0))
    datavis = banco.Column(banco.DateTime)
    codqr = banco.Column(banco.String(40))
    dataaute = banco.Column(banco.DateTime)
    codusuario = banco.Column(banco.Integer, banco.ForeignKey('usuario.usuario_id'))
    status = banco.Column(banco.String(80))

    def __init__(self, nome,cpf, datavis, codqr, codusuario, status):
        self.nome = nome
        self.cpf = cpf
        self.datavis = datavis
        self.codqr = codqr
        self.codusuario = codusuario
        self.status = status

    def json(self):
        return {
            'cliente_id': self.cliente_id,
            'nome': self.nome,
            "cpf": self.cpf,
            'datager': self.datager.strftime("%d/%m/%Y %H:%M:%S"),
            'datavis': self.datavis.strftime("%d/%m/%Y"),
            'codqr': self.codqr,
            'dataaute': self.dataaute.strftime("%d/%m/%Y %H:%M:%S") if self.dataaute else None,
            "codusuario": self.codusuario,
            "status": self.status
        }

    @classmethod
    def find_cliente_by_cpf(cls, cpf_cliente):
        cliente = cls.query.filter_by(cpf=cpf_cliente).first()
        if cliente:
            return cliente
        return None
    
    @classmethod
    def find_datavis(cls,cpf, datavis):
        datavis = cls.query.filter_by(cpf=cpf, datavis=datavis).first()
        if datavis:
            return datavis
        return None
    
    @classmethod
    def find_cliente_by_id(cls, cliente_id):
        cliente_id = cls.query.filter_by(cliente_id=cliente_id).first()
        if cliente_id:
            return cliente_id
        return None
    
    @classmethod
    def find_customer_status(cls,cliente_id, status):
        status = cls.query.filter_by(cliente_id=cliente_id, status=status).first()
        if status:
            return status
        return None
    
    @classmethod
    def checks_date(cls):
        clientes_para_atualizar = cls.query.filter(cls.datavis < data_limite, cls.status == 'agendado').all()
        for cliente in clientes_para_atualizar:
            cliente.status = 'omisso'
        banco.session.commit()
        return len(clientes_para_atualizar)
    

    @classmethod
    def checks_status(cls, codusuario):
        if not codusuario:
            status = cls.query.filter_by(status="agendado").all()
            return status
        return cls.query.filter_by(codusuario=codusuario, status="agendado").all()

    def save_cliente(self):
        banco.session.add(self)
        banco.session.commit()

    def update_cliente(self,datavis):
        self.datavis = datavis

    def update_appointment(self, status):
        self.status = status

"""     def delete_cliente(self):
        banco.session.delete(self)
        banco.session.commit()
        
 """