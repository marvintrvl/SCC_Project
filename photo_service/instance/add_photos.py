import sys
sys.path.append('..')

from models import db, Photo, Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Configure the database connection
engine = create_engine('sqlite:///photos.db')
Session = sessionmaker(bind=engine)
session = Session()

# Function to add a category
def add_category(name):
    category = Category(name=name)
    session.add(category)
    session.commit()

# Function to add a photo
def add_photo(name, description, size, price, category_name, image_path):
    # Check if the category exists, if not, create it
    category = session.query(Category).filter_by(name=category_name).first()
    if not category:
        add_category(category_name)
        category = session.query(Category).filter_by(name=category_name).first()

    # Add the photo
    photo = Photo(
        name=name,
        description=description,
        size=size,
        small_price=price,
        category_id=category.id,
        image=image_path
    )
    session.add(photo)
    session.commit()

# Add the three categories
add_category('Cities')
add_category('Landscapes')
add_category('Street Photography')

# Example usage
add_photo('Sunset at the Maria Gern church', 'adventure, ancient, architecture, beauty in nature, belief, building, building exterior, built structure, cityscape, cloud, countryside, environment, greenery, heavenly, hill, history, land, landscape, morning, nature, no people, place of worship, plant, religion, rural area, scenics - nature, sky, the past, travel destinations, tree, berchtesgaden, alps, alpen, bayern, bavaria, maria gern, curch, sunset', 'S', 20.00, 'Landscapes', 'images/DSC04373-Edit_IdKP2qR.jpg')
add_photo('Dresden skyline during sunset', 'architecture, building, building exterior, built structure, city, cityscape, cloud, downtown, dusk, evening, faith, historic, history, landmark, metropolis, night, place of worship, reflection, religion, river, scenic, sky, skyline, sundown, sunset, the past, tourism, travel, travel destinations, water, elbe, dresden, altstadt, old town, sachsen, saxony', 'S', 20.00, 'Cities', 'images/DSC01893-HDR_nYG0rt8.jpg')
add_photo('Winter morning in the streets of Dresden', 'architecture, blurred motion, building exterior, built structure, city, city life, city street, cold temperature, darkness, downtown, full length, illuminated, light, metropolis, mode of transportation, motion, movement, night, on the move, one person, people, person, road, snow, street, transportation, urban, urban development, walking, winter, dresden, street photography', 'S', 20.00, 'Street Photography', 'images/_DSC6505_rmDg9T0.JPG')
add_photo('Sunrise at the Hintersee', 'adventure, beauty in nature, calm, clouds, environment, forest, fresh air, greenery, lake, land, landscape, morning, mountain, mountain range, nature, no people, ocean, outdoors, peaceful, plant, reflection, river, rock, scenics - nature, sky, tranquil scene, tranquility, tree, water, wilderness, berchtesgaden, hintersee, alpls, bavaria, bayern', 'S', 20.00, 'Landscapes', 'images/DSC04443.jpg')
add_photo('Frauenkirche Dresden during sunset', 'altstadt, ancient, architecture, belief, belief system, building, building exterior, built structure, city, cityscape, dome, downtown, dresden, dresden altstadt, dusk, evening, faith, frauenkirche, historic, history, landmark, metropolis, place of worship, religion, sky, skyline, sunset, tourism, tower, travel, travel destinations, urban skyline', 'S', 20.00, 'Cities', 'images/DJI_0221.jpg')
add_photo('Sunrise near Pfaffenstein', 'autumn, beauty in nature, countryside, dawn, dusk, environment, field, fog, forest, fresh, golden, green, land, landscape, leaf, mist, morning, nature, no people, plant, scenics - nature, sky, sun, sunbeam, sunlight, sunrise, tranquil scene, tranquility, tree, twilight', 'S', 20.00, 'Landscapes', 'images/DSC02712-Edit.jpg')
add_photo('Bastei bridge during sunrise', 'autumn, beauty in nature, cloud, environment, fall, foliage, forest, land, landscape, leaf, morning, nature, no people, outdoors, plant, scenics - nature, sky, travel destinations, tree, wilderness, sächsiche schweiz, sachsen, bastei bridge, saxonys switzerland', 'S', 20.00, 'Landscapes', 'images/_DSC3089-Edit.jpg')
add_photo('Stara Plynarna in Hrensko', 'architecture, building, building exterior, built structure, empty, exterior, flora, forest, jungle, nature, no people, outdoor, plant, tree, hrensko, czech republic, landscape, moody', 'S', 20.00, 'Landscapes', 'images/1_-_Copy.jpg')
add_photo('Tranquil morning mist over dark forest', 'atmosphere, beauty in nature, calm, cloud, environment, fog, forest, greenery, land, landscape, mist, morning, nature, no people, outdoors, plant, scenics - nature, tranquility, tree, fog', 'S', 20.00, 'Landscapes', 'images/DSC05914.jpg')
add_photo('Röthbachfall long exposure', 'beauty in nature, body of water, creek, environment, flowing water, forest, green, land, landscape, long exposure, motion, natural environment, nature, no people, non-urban scene, outdoors, plant, rainforest, river, scenics - nature, stream, tranquility, travel destinations, tree, water, water feature, watercourse, waterfall, wilderness, woodland', 'S', 20.00, 'Landscapes', 'images/DSC06682.jpg')
add_photo('Sunset view over Budapest', 'architecture, building, building exterior, built structure, city, cityscape, high angle view, historic, history, landmark, no people, scenic, sky, skyline, the past, tourism, town, travel, travel destinations, urban, budapest, europe, fishermans bastion, parliament building', 'S', 20.00, 'Cities', 'images/DSC08778.jpg')
add_photo('Residenzschloss Dresden', 'architecture, black, building, building exterior, built structure, city, darkness, dusk, focus on background, light, metropolis, night, nighttime, reflection, skyscraper, tourism, tower, travel, travel destinations, urban, dresden, residenzschloss, bell tower', 'S', 20.00, 'Cities', 'images/_DSC3738-HDR.jpg')
add_photo('Winter night in Dresden', 'architecture, building exterior, built structure, chilly, city, cold temperature, downtown, dusk, frosty, group, group of people, illuminated, lights, night, people, snow, snowing, walking, wet, winter, dresden, street photography, zwinger, semperoper, opera', 'S', 20.00, 'Street Photography', 'images/_DSC7319.JPG')
add_photo('The escaping pigeon', 'animal, animal themes, bird, black, city, cityscape, crowd, footwear, human leg, individual, individuals, low section, one animal, one person, people, person, single animal, urban, pigeon, taube, dresden', 'S', 20.00, 'Street Photography', 'images/DSC00525.jpg')
# Add more photos as needed

# Close the session
session.close()
