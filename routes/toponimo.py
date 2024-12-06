from flask import Blueprint, request, jsonify, make_response
from models import Toponimo, Plant, db
from schemas import ToponimoSchema

toponimo_bp = Blueprint('toponimos', __name__)


"""
curl -X POST http://127.0.0.1:5000/toponimos/ \
-H "Content-Type: application/json" \
-d '{
    "id_plant": 3,
    "origin": "guayakill",
    "comercial_distribution": "mercado amazonas" ,
    "distribution":"los andes"  
}'
"""
@toponimo_bp.route('/', methods=['POST'])
def create_toponimo():
    data = request.json
    try:
        new_data = ToponimoSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    plant = Plant.query.get(new_data['id_plant'])
    if not plant:
        return jsonify({'error': 'Invalid id_plant. Plant not found.'}), 404

    new_toponimo = Toponimo(**new_data)

    try:
        db.session.add(new_toponimo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    toponimo_schema = ToponimoSchema()
    toponimo_json = toponimo_schema.dump(new_toponimo)
    return jsonify(toponimo_json), 201


#curl -X DELETE http://127.0.0.1:5000/toponimos/1
@toponimo_bp.route('/<int:id>', methods=['DELETE'])
def delete_toponimo(id):
    toponimo = Toponimo.query.get(id)
    if toponimo:
        db.session.delete(toponimo)
        db.session.commit()
        return jsonify({'message': 'Toponimo successfully deleted'}), 200
    else:
        return jsonify({'error': 'Toponimo not found'}), 404

#curl -v http://127.0.0.1:5000/toponimos/all_toponimos
@toponimo_bp.route('/all_toponimos', methods=['GET'])
def all_toponimos():
    try:
        get_toponimos = Toponimo.query.all()
        toponimo_schema = ToponimoSchema(many=True)
        toponimos = toponimo_schema.dump(get_toponimos)
        return make_response(jsonify({"toponimos": toponimos}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# curl -v http://127.0.0.1:5000/toponimos/3
@toponimo_bp.route('/<int:id>', methods=['GET'])
def get_toponimo(id):
    toponimo = Toponimo.query.get(id)
    if toponimo:
        toponimo_schema = ToponimoSchema()
        toponimo_json = toponimo_schema.dump(toponimo)
        return jsonify(toponimo_json), 200
    else:
        return jsonify({'message': 'Toponimo not found'}), 404

'''
 Route to update a plant by ID
 curl -X PUT http://127.0.0.1:5000/toponimos/4 \
      -H "Content-Type: application/json" \
      -d '{
            "id_plant": 3,
            "origin": "Quitusss",
            "comercial_distribution": "mercado tuti" ,
            "distribution":"coordillera" 
        }'
'''
@toponimo_bp.route('/<int:id>', methods=['PUT'])
def update_toponimo(id):
    toponimo = Toponimo.query.get(id)
    if toponimo:
        data = request.get_json()

        new_plant_id = data.get('id_plant')
        if new_plant_id:
            plant = Plant.query.get(new_plant_id)
            if not plant:
                return jsonify({'error': 'Invalid id_plant. Plant not found.'}), 400
        toponimo.id_plant = new_plant_id if new_plant_id else toponimo.id_plant
        toponimo.origin = data.get('origin', toponimo.origin)
        toponimo.comercial_distribution = data.get('comercial_distribution', toponimo.comercial_distribution)
        toponimo.distribution = data.get('distribution', toponimo.distribution)

        # Realiza el commit para guardar los cambios
        db.session.commit()

        return jsonify({'message': 'Toponimo updated successfully'}), 200
    else:
        return jsonify({'message': 'Toponimo not found'}), 404
