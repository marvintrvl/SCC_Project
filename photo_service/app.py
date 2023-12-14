from flask import Flask, jsonify, request, send_file
from models import db, Photo, Category
from database import db
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5003"}}, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = 'C:/Users/menzm/Desktop/SCC_Project/photo_service/images'

db_name = 'photos.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_db():
    with app.app_context():
        db.create_all()
 
if __name__ == "__main__":
    from models import Photo

    create_db()

@app.route('/images/<filename>')
def get_image(filename):
    return send_file(app.config['UPLOAD_FOLDER'] + '/' + filename)

@app.route('/', methods=['GET'])
def index():
    recent_pictures = Photo.query.order_by(Photo.id.desc()).limit(6).all()
    picture_data = [
        {
            'id': photo.id,
            'url': f'/images/{photo.image}' if photo.image else None,
            'name': photo.name
        } for photo in recent_pictures
    ]

    return jsonify(pictures=picture_data)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '')
    # Implement search logic based on the description field in the database
    # Fetch photos with descriptions containing the search query
    search_results = Photo.query.filter(Photo.description.ilike(f'%{search_query}%')).all()

    result_data = [
        {
            'id': photo.id,
            'url': f'http://127.0.0.1:5001/{photo.image}',
            'name': photo.name,
        } for photo in search_results
    ]

    return jsonify(results=result_data)

@app.route('/categories/<category_name>', methods=['GET'])
def get_category_photos(category_name):
    print("Received category_name:", category_name)
    
    try:
        # Fetch category by name
        category = Category.query.filter_by(name=category_name).first()
        
        if category is None:
            raise Exception("Category not found")

        # Fetch photos in the specified category
        photos_in_category = Photo.query.join(Category).filter(Category.name == category_name).all()

        category_data = {
            "category": category.serialize(),
            "photos": [photo.serialize() for photo in photos_in_category]
        }
        return jsonify(category_data)
    except Exception as e:
        # Handle exceptions, log them, and return an error response
        print("Error fetching category data:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/photos', methods=['GET'])
def get_all_photos():
    try:
        # Implement logic to fetch all photos
        photos = Photo.query.all()
        # Convert to JSON or manipulate as needed
        return jsonify({"photos": [photo.serialize() for photo in photos]})
    except Exception as e:
        # Handle exceptions, log them, and return an error response
        return jsonify({"error": str(e)}), 500

@app.route('/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    # Implement logic to fetch a specific photo
    photo = Photo.query.get(photo_id)
    # Check if the photo exists
    if photo:
        # Convert to JSON or manipulate as needed
        return jsonify({"photo": photo.serialize()})
    else:
        # Return a 404 response if the photo is not found
        return jsonify({"error": "Photo not found"}), 404

def get_photo_details(photo_id):
    # Implement logic to fetch photo details
    photo_data = get_photo(photo_id)
    photo = photo_data['photo']
    name = photo['name']
    url = f'http://127.0.0.1:5001/{photo["image"]}' if photo['image'] else None
    return {
        "photo": photo,
        "name": name,
        "url": url
    }

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
    response.headers['Access-Control-Allow-Credentials'] = 'true'  
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
