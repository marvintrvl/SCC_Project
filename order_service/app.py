# app.py

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from models import Order, OrderDetail
from database import db
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uewqriughbrepighrrupqeghrtoubq34t'
app.config['JWT_SECRET_KEY'] = 'uewqriughbrepighrrupqeghrtoubq34t'
db.init_app(app)

jwt = JWTManager(app)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/place-order', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    print('Received order data:', data)

    app.logger.info(f"Received place_order request: {data}")

    # Extract order data
    total_price = data.get('total_price')
    shipping_address = data.get('shipping_address')
    bank_info = data.get('bank_info')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Create a new Order
    order = Order(user_id=user_id, total_price=total_price, shipping_address=shipping_address, bank_info=bank_info, first_name=first_name, last_name=last_name)
    db.session.add(order)
    db.session.commit()

    # Extract and save order details
    order_details = data.get('order_details', [])

    print('Extracted order details:', order_details)

    for detail in order_details:
        order_detail = OrderDetail(
            order_id=order.id,
            quantity=detail['quantity'],
            size=detail['size'],
            photo_name=detail['photo_name'],
            photo_id=detail['photo_id'],
            subtotal=detail['subtotal']
        )
        db.session.add(order_detail)

    db.session.commit()

    return jsonify(message="Order placed successfully", order_id=order.id), 201

@app.route('/get-order/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()

    if order:
        order_data = {
            'id': order.id,
            'date_created': order.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'total_price': order.total_price,
            # Add other fields you want to include in the response
        }
        return jsonify(order_data), 200
    else:
        return jsonify(message="Order not found"), 404
    
@app.route('/view-orders', methods=['GET']) 
@jwt_required()
def get_user_orders():
  user_id = get_jwt_identity()
  
  orders = Order.query.filter_by(user_id=user_id).all()
  
  order_data = []
  for order in orders:
    data = {
      'id': order.id,
      'date_created': order.date_created, 
      'total_price': order.total_price,
      'details': get_order_details(order.id) 
    }
    order_data.append(data)

  return jsonify(order_data)

def get_order_details(order_id):
  details = OrderDetail.query.filter_by(order_id=order_id).all()
  
  detail_data = []
  for d in details:
    data = {
      'id': d.id,
      'quantity': d.quantity,
      'size': d.size,
      'photo_name': d.photo_name,
      'subtotal': d.subtotal
    }
    detail_data.append(data)
  
  return detail_data

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'  
    response.headers['Access-Control-Allow-Credentials'] = 'true' 
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5004, debug=True)
