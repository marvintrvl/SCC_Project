from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, Cart, CartItem
from database import db as cart_db
import requests
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import joinedload


app = Flask(__name__)
CORS(app, resources={
  r"/*": {
    "origins": "http://127.0.0.1:5003",
    "methods": ["GET", "POST", "PUT", "DELETE"] 
  }
})

db_name = 'cart.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uewqriughbrepighrrupqeghrtoubq34t'
app.config['JWT_SECRET_KEY'] = 'uewqriughbrepighrrupqeghrtoubq34t'

db.init_app(app)

# Initialize JWT extension
jwt = JWTManager(app)


# Cache for storing photo details to avoid redundant calls
photo_details_cache = {}


def get_photo_details(photo_id):
    # Check if photo details are already in the cache
    if photo_id in photo_details_cache:
        return photo_details_cache[photo_id]

    # If not in cache, fetch from Photo Service
    response = requests.get(f'http://127.0.0.1:5001/photos/{photo_id}')
    if response.status_code != 200:
        abort(404, description="Photo not found")

    photo_details = response.json()["photo"]

    # Cache the photo details
    photo_details_cache[photo_id] = photo_details

    return photo_details


# Routes
@app.route('/add-to-cart', methods=['OPTIONS', 'POST'])
@cross_origin(origin='http://127.0.0.1:5003', supports_credentials=True)
def add_to_cart_options():
    response = app.make_default_options_response()

    # Allow CORS on this route
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, HEAD'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response

@app.route('/add-to-cart/<int:photo_id>', methods=['POST'])
@jwt_required() 
def add_to_cart(photo_id):
    user_id = get_jwt_identity()
    
    data = request.get_json()
    quantity = data.get('quantity')
    size = data.get('size')

    # Log received data
    app.logger.info(f"Received add to cart request: {data}")

    photo_details = get_photo_details(photo_id)
    photo_url = data.get('url')

    # Create a new CartItem with the updated structure
    cart_item = CartItem(
        user_id=user_id,
        photo_id=photo_id,
        quantity=quantity,
        size=size,
        name=photo_details['name'],
        price=0.0,  # Set initial price to 0.0
        url=photo_url
    )

    # Set the price based on the selected size
    cart_item.calculate_price()

    # Add the cart item to the session
    db.session.add(cart_item)

    try:
        db.session.commit()
        app.logger.info(f"Added cart item: {cart_item.serialize()}")

        response = jsonify(message="Successfully added item", cart_item=cart_item.serialize())
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

    except Exception as e:
        app.logger.error(f"Error adding cart item: {str(e)}")
        db.session.rollback()
        return jsonify(error="Failed to add item"), 500

    # Update cart totals
    cart = Cart.query.filter_by(user_id=user_id).first()
    if cart is None:
        cart = Cart(user_id=user_id)
        db.session.add(cart)

    cart.total_items = CartItem.query.filter_by(user_id=user_id).count() 
    cart.total_price = sum(item.price for item in CartItem.query.filter_by(user_id=user_id).all())

    try:
        db.session.commit()  # Commit the cart totals update
    except Exception as e:
        app.logger.error(f"Error updating cart totals: {str(e)}")
        db.session.rollback()
        return jsonify(error="Failed to update cart totals"), 500

    return jsonify(message="Successfully added item", cart_item=cart_item.serialize()), 201

@app.route('/get-cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()

    # Fetch cart items for the user
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    # Calculate total items and total price
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.price for item in cart_items)
    subtotal = sum(item.price for item in cart_items)

    return jsonify({
        "cart_items": [item.serialize() for item in cart_items],
        "total_items": total_items,
        "total_price": str(total_price),
        "subtotal": str(subtotal)
    })

@app.route('/update-cart-item/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    # Assuming you have the CartItem model imported
    cart_item = CartItem.query.get_or_404(cart_item_id)

    # Update the quantity
    new_quantity = int(request.form.get('quantity', 1))
    cart_item.quantity = new_quantity
    cart_item.calculate_price()  # Recalculate the price based on the new quantity
    db.session.commit()

    # You may need to update the total_items and total_price in the Cart model here

    return jsonify({'message': 'Cart item quantity updated successfully'}), 200

@app.route('/delete-cart-item/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(cart_item_id):
    user_id = get_jwt_identity()

    # Check if the cart item belongs to the user
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=user_id).first()
    if not cart_item:
        abort(404, description="Cart item not found")

    db.session.delete(cart_item)
    db.session.commit()

    # Update total items and total price in the cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    cart.total_items = CartItem.query.filter_by(user_id=user_id).count()

    # Fetch cart items directly without using joinedload
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    cart.total_price = sum(item.calculate_price() for item in cart_items if item.price is not None)

    db.session.commit()

    return jsonify(message="Cart item deleted successfully"), 200

@app.route('/clear-cart', methods=['DELETE'],)
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()

    # Delete all cart items for the user
    CartItem.query.filter_by(user_id=user_id).delete()

    # Update total items and total price in the cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if cart:
        cart.total_items = 0
        cart.total_price = 0.00

    db.session.commit()

    return jsonify(message="Cart cleared successfully"), 200

@app.after_request
def after_request(response):
    if request.method == 'DELETE':
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, HEAD, PUT, DELETE, OPTIONS'
    return response


if __name__ == '__main__':
    with app.app_context():
        cart_db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)




