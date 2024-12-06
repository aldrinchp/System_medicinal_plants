from flask import Blueprint, request, jsonify, make_response
from models import Plant, Location, db
from schemas import PlantSchema

plant_bp = Blueprint('plants', __name__)

'''
curl -X POST http://127.0.0.1:5000/plants/ \
-H "Content-Type: application/json" \
-d '{
    "location_id": 4,
    "current_name": "Planta Nueva",
    "scientific_name": "PlantaNuevaScientific"
}'
'''
@plant_bp.route('/', methods=['GET', 'POST'])
def create_plant():
    # Parsear los datos JSON de la solicitud
    data = request.json

    # Validar y deserializar los datos usando PlantSchema
    try:
        new_data = PlantSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Verificar que el `site_origin_id` existe en la tabla `site_origin`
    location = Location.query.get(new_data['location_id'])
    if not location:
        return jsonify({'error': 'Invalid Location_id. Location not found.'}), 404

    # Crear una nueva instancia de Plant usando los datos deserializados
    new_plant = Plant(**new_data)

    # Agregar el nuevo registro a la base de datos
    try:
        db.session.add(new_plant)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    # Serializar la nueva planta creada y devolver la respuesta
    plant_schema = PlantSchema()
    plant_json = plant_schema.dump(new_plant)
    return jsonify(plant_json), 201

#curl -X DELETE http://127.0.0.1:5000/plants/1
@plant_bp.route('/<int:id>', methods=['DELETE'])
def delete_plant(id):
    # Buscar la planta por su ID
    plant = Plant.query.get(id)
    
    if plant:
        # Eliminar la planta de la base de datos
        db.session.delete(plant)
        db.session.commit()
        return jsonify({'message': 'Plant successfully deleted'}), 200
    else:
        # Si la planta no existe, retornar un error
        return jsonify({'error': 'Plant not found'}), 404

#curl -v http://127.0.0.1:5000/plants/all_plants
@plant_bp.route('/all_plants', methods=['GET'])
def all_plants():
    try:
        # Obtener todos los registros de la tabla Plant
        get_plants = Plant.query.all()
        
        # Crear un esquema para serializar los datos de la tabla Plant
        plant_schema = PlantSchema(many=True)
        
        # Serializar los datos obtenidos
        plants = plant_schema.dump(get_plants)
        
        # Retornar los registros serializados en formato JSON
        return make_response(jsonify({"plants": plants}), 200)
    
    except Exception as e:
        # Manejo de errores
        return make_response(jsonify({"error": str(e)}), 500)

# Retrieve a plant by ID
# curl -v http://127.0.0.1:5000/plants/6
@plant_bp.route('/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)  # Busca la planta por el ID
    if plant:
        plant_schema = PlantSchema()  # Usa el esquema de planta para serializar la planta
        plant_json = plant_schema.dump(plant)  # Serializa el objeto plant
        return jsonify(plant_json), 200  # Retorna la planta como respuesta en formato JSON
    else:
        return jsonify({'message': 'Plant not found'}), 404  # Si no se encuentra la planta, devuelve un error

'''
 Route to update a plant by ID
 curl -X PUT http://127.0.0.1:5000/plants/4 \
      -H "Content-Type: application/json" \
      -d '{"id_location": 6,
            "current_name": "Margarita", 
           "scientific_name": "Margaritus"
           }'
'''
@plant_bp.route('/<int:id>', methods=['PUT'])
def update_plant(id):
    plant = Plant.query.get(id)  # Busca la planta por ID
    if plant:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud

        new_location_id = data.get('location_id')
        if new_location_id:
            site_origin = Location.query.get(new_location_id)
            if not site_origin:
                return jsonify({'error': 'Invalid location_id. Location not found.'}), 400

        # Actualiza los atributos de la planta con los valores proporcionados
        plant.location_id = new_location_id if new_location_id else plant.location_id
        plant.current_name = data.get('current_name', plant.current_name)
        plant.scientific_name = data.get('scientific_name', plant.scientific_name)

        # Realiza el commit para guardar los cambios
        db.session.commit()

        return jsonify({'message': 'Plant updated successfully'}), 200
    else:
        return jsonify({'message': 'Plant not found'}), 404  # Si no se encuentra la planta, devuelve error
