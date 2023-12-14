from database import db

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_items = db.Column(db.Integer, default=0)
    total_price = db.Column(db.Numeric(10, 2), default=0.00)

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    photo_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=0)

    # Additional fields from Photo model
    name = db.Column(db.String(255))
    size = db.Column(db.String(1))
    price = db.Column(db.Numeric(6, 2), default=0.00)  # Total price for the item
    url = db.Column(db.String(255))

    def __init__(self, user_id, photo_id, quantity, **kwargs):
        self.user_id = user_id
        self.photo_id = photo_id
        self.quantity = quantity

        # Set additional fields from Photo model
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Set the initial price based on the selected size
        self.calculate_price()

    def calculate_price(self):
        # Calculate price based on quantity and size
        if self.size == 'S':
            self.price = float(self.quantity) * 20.00
        elif self.size == 'M':
            self.price = float(self.quantity) * 40.00
        elif self.size == 'L':
            self.price = float(self.quantity) * 60.00
        else:
            self.price = 0.0

        return self.price if self.price is not None else 0.0

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'photo_id': self.photo_id,
            'quantity': self.quantity,
            'photo': {
                'name': self.name,
                'size': self.size,
                'price': float(self.price) if self.price is not None else 0.0,
                'url': self.url,
            },
        }