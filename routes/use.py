from flask import Blueprint, request, jsonify, make_response
from models import Use, Plant, db
from schemas import UseSchema

use_bp = Blueprint('uses', __name__)

"""
curl -X POST http://127.0.0.1:5000/uses/ \
-H "Content-Type: application/json" \
-d '{
    "id_plant": 3,
    "description": "ta mas bonito",
    "type_use": "diarre"   
}'
"""
@use_bp.route('/', methods=['POST'])
def create_use():
    data = request.json
    try:
        new_data = UseSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    plant = Plant.query.get(new_data['id_plant'])
    if not plant:
        return jsonify({'error': 'Invalid id_plant. Plant not found.'}), 404

    new_use = Use(**new_data)

    try:
        db.session.add(new_use)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    use_schema = UseSchema()
    use_json = use_schema.dump(new_use)
    return jsonify(use_json), 201

#curl -X DELETE http://127.0.0.1:5000/uses/1
@use_bp.route('/<int:id>', methods=['DELETE'])
def delete_use(id):
    use = Use.query.get(id)
    if use:
        db.session.delete(use)
        db.session.commit()
        return jsonify({'message': 'Use successfully deleted'}), 200
    else:
        return jsonify({'error': 'Use not found'}), 404

#curl -v http://127.0.0.1:5000/uses/all_uses
@use_bp.route('/all_uses', methods=['GET'])
def all_uses():
    try:
        get_uses = Use.query.all()
        use_schema = UseSchema(many=True)
        uses = use_schema.dump(get_uses)
        return make_response(jsonify({"uses": uses}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# curl -v http://127.0.0.1:5000/uses/3
@use_bp.route('/<int:id>', methods=['GET'])
def get_use(id):
    use = Use.query.get(id)
    if use:
        use_schema = UseSchema()
        use_json = use_schema.dump(use)
        return jsonify(use_json), 200
    else:
        return jsonify({'message': 'Use not found'}), 404


'''
 Route to update a plant by ID
 curl -X PUT http://127.0.0.1:5000/previous_researches/4 \
      -H "Content-Type: application/json" \
      -d '{
            "id_plant": 3,
            "description": "ta mas bonito",
            "type_use": "diarre" 
        }'
'''
@use_bp.route('/<int:id>', methods=['PUT'])
def update_use(id):
    use = Use.query.get(id)
    if use:
        data = request.get_json()

        new_plant_id = data.get('id_plant')
        if new_plant_id:
            plant = Plant.query.get(new_plant_id)
            if not plant:
                return jsonify({'error': 'Invalid id_plant. Plant not found.'}), 400
        use.id_plant = new_plant_id if new_plant_id else use.id_plant
        use.description = data.get('description', use.description)
        use.type_use = data.get('type_use', use.type_use)

        # Realiza el commit para guardar los cambios
        db.session.commit()

        return jsonify({'message': 'Use updated successfully'}), 200
    else:
        return jsonify({'message': 'Use not found'}), 404
