from flask import Blueprint, request, jsonify, make_response
from models import Image, Plant, db
from schemas import ImageSchema

image_bp = Blueprint('images', __name__)

'''
curl -X POST http://127.0.0.1:5000/images/ \
-H "Content-Type: application/json" \
-d '{
    "plant_id": 5,
    "date": "2024-11-27",
    "place": "Manabi"
}'
'''
@image_bp.route('/', methods=['POST'])
def create_image():
    data = request.json
    try:
        new_data = ImageSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    plant = Plant.query.get(new_data['plant_id'])
    if not plant:
        return jsonify({'error': 'Invalid plant_id. Plant not found.'}), 404

    new_image = Image(**new_data)

    try:
        db.session.add(new_image)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

   
    image_schema = ImageSchema()
    image_json = image_schema.dump(new_image)
    return jsonify(image_json), 201

#curl -X DELETE http://127.0.0.1:5000/images/5
@image_bp.route('/<int:id>', methods=['DELETE'])
def delete_image(id):
    image = Image.query.get(id)
    if image:
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': 'Image successfully deleted'}), 200
    else:
        return jsonify({'error': 'Image not found'}), 404

#curl -v http://127.0.0.1:5000/images/all_images
@image_bp.route('/all_images', methods=['GET'])
def all_images():
    try:
        get_images = Image.query.all()
        image_schema = ImageSchema(many=True)
        images = image_schema.dump(get_images)
        return make_response(jsonify({"images": images}), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# curl -v http://127.0.0.1:5000/images/6
@image_bp.route('/<int:id>', methods=['GET'])
def get_image(id):
    image = Image.query.get(id) 
    if image:
        image_schema = ImageSchema() 
        image_json = image_schema.dump(image)  
        return jsonify(image_json), 200  
    else:
        return jsonify({'message': 'Image not found'}), 404  
    
    
'''
 Route to update a plant by ID
 curl -X PUT http://127.0.0.1:5000/images/4 \
      -H "Content-Type: application/json" \
      -d '{
            "plant_id": 5,
            "date": "2024-11-27",
            "place": "Manabi"
        }'
'''
@image_bp.route('/<int:id>', methods=['PUT'])
def update_image(id):
    image = Image.query.get(id)  
    if image:
        data = request.get_json()

        new_plant_id = data.get('plant_id')
        if new_plant_id:
            plant = Plant.query.get(new_plant_id)
            if not plant:
                return jsonify({'error': 'Invalid plant_id. Plant not found.'}), 400
        image.plant_id = new_plant_id if new_plant_id else image.plant_id
        image.plant_id = data.get('plant_id',image.plant_id)
        image.date = data.get('date', image.date)
        image.place = data.get('place', image.place)

        # Realiza el commit para guardar los cambios
        db.session.commit()

        return jsonify({'message': 'Image updated successfully'}), 200
    else:
        return jsonify({'message': 'Image not found'}), 404  

