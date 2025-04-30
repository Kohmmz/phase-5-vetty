from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from marshmallow import ValidationError
from app import db
from app.models.Payment import Payment
from app.schemas.Payment_schemas import PaymentSchema
from app.utils.payment_util import process_payment

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')
api = Api(payment_bp)

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

class PaymentResource(Resource):
    def get(self, payment_id):
        payment = Payment.query.get_or_404(payment_id)
        return payment_schema.dump(payment), 200

    def post(self):
        data = request.get_json()
        try:
            payment = payment_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # Process payment
        payment_status = process_payment(data)
        payment.status = payment_status

        db.session.add(payment)
        db.session.commit()
        return payment_schema.dump(payment), 201

api.add_resource(PaymentResource, '/<int:payment_id>')