from flask_restful import Resource, reqparse
from models.qrcode import QrCodeModel
from datetime import datetime

args = reqparse.RequestParser()
args.add_argument('qrcode', type=str, required=True,
                       help="The field 'codqr' cannot be left blank")

class ValidQrcode(Resource):
    def post(self):
        data = args.parse_args()
        found_qr = QrCodeModel.find_by_qrcode(data['qrcode'])
        if not found_qr:
            return {"message": "QRcode not found"},400
        qrcode = QrCodeModel.find_by_status(data["qrcode"])
        if qrcode:
            qrcode.update_codqr(datetime.now().replace(microsecond=0), status="atendido")
            qrcode.save_codqr()
            return{"message": "QRcode valid"},200
        return {"message": "QRcode invalid"}, 400