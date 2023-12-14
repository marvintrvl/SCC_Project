from database import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Photo(db.Model):
    __tablename__ = 'photo'
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=True)
    size = db.Column(db.String(1))
    small_price = db.Column(db.Numeric(6, 2), default=20.00)
    medium_price = db.Column(db.Numeric(6, 2), default=40.00)
    large_price = db.Column(db.Numeric(6, 2), default=60.00)
    image = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.CheckConstraint(size.in_([choice[0] for choice in SIZE_CHOICES]), name='check_size'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'size': self.size,
            'small_price': float(self.small_price),
            'medium_price': float(self.medium_price),
            'large_price': float(self.large_price),
            'image': self.image,
        }