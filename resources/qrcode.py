from flask_restful import Resource, reqparse, request
from models.qrcode import QrCodeModel
from models.cliente import ClienteModel
from flask import send_file
import qrcode
import io
from datetime import datetime

args = reqparse.RequestParser()
args.add_argument('qrcode', type=str, required=True,
                       help="The field 'codqr' cannot be left blank")

class ValidQrcode(Resource):
    def post(self):
        data = args.parse_args()
        found_qr = QrCodeModel.find_by_qrcode(data['qrcode'])
        if not found_qr:
            return {"message": "Qrcode not found"},400
        qrcode = QrCodeModel.find_by_status(data["qrcode"])
        if qrcode:
            qrcode.update_codqr(datetime.now().replace(microsecond=0), status="atendido")
            qrcode.save_codqr()
            return{"message": "QRcode valid"},200
        return {"message": "QRcode invalid"}, 400
    
class DownloadQrcode(Resource):
    def post(self, codqr):     
        codqr_enc = QrCodeModel.find_by_qrcode(codqr)
        if codqr_enc:
            codqr_enc = codqr_enc.json()
            codqr = codqr_enc["codqr"]
            data = codqr  
            
            # Gerar o QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Criar imagem do QR code e armazenar em um buffer de memória
            img = qr.make_image(fill="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Enviar o QR code como um arquivo para download
            return send_file(buffer, as_attachment=True, download_name="qrcode.png", mimetype='image/png')
        
        return {'message': 'Qrcode not found'}, 404