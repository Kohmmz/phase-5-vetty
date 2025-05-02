from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models.Payment import Payment
from app.schemas.Payment_schemas import PaymentSchema
from app.utils.payment_util import process_payment

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment_schema.dump(payment)), 200

@payment_bp.route('', methods=['POST'])
def create_payment():
    data = request.get_json()
    try:
        payment = payment_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Process payment
    payment_status = process_payment(data)
    payment.status = payment_status

    db.session.add(payment)
    db.session.commit()
    return jsonify(payment_schema.dump(payment)), 201