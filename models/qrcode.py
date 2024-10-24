from sql_alchemy import banco

class QrCodeModel(banco.Model):
    __tablename__ = 'cliente'
    __table_args__ = {'extend_existing': True}
    codqr = banco.Column(banco.String(40))
    dataaute = banco.Column(banco.DateTime)
    status = banco.Column(banco.String(80))

    def __init__(self, codqr):
        self.codqr = codqr

    @classmethod
    def find_by_qrcode(cls, codqr):
        qrcode = cls.query.filter_by(codqr=codqr).first()
        if qrcode:
            return qrcode
        return None
    
    @classmethod
    def find_by_status(cls, codqr):
        qrcode = cls.query.filter_by(codqr=codqr,status="agendado").first()
        if qrcode:
            return qrcode
        return None
    
    def save_codqr(self):
        banco.session.add(self)
        banco.session.commit()

    def update_codqr(self,dataaute, status):
        self.dataaute = dataaute
        self.status = status
        
        
