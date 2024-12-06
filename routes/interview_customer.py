from flask import Blueprint, request, jsonify, make_response
from models import InterviewCustomer, Location, db
from schemas import InterviewCustomerSchema

interview_customer_bp = Blueprint('interview_customers', __name__)

"""
Crear un nuevo registro en InterviewCustomer
curl -X POST http://127.0.0.1:5000/interview_customers/ \
-H "Content-Type: application/json" \
-d '{
    "id_location": 2,
    "link": "httt.com",
    "q1": "Respuesta 1",
    "q2": "Respuesta 2",
    "q3": "Respuesta 3",
    "q4": "Respuesta 4",
    "q5": "Respuesta 5",
    "q6": "Respuesta 2",
    "q7": "Respuesta 2",
    "q8": "Respuesta 2",
    "q9": "Respuesta 2",
    "q10": "Respuesta 2",
    "q11": "Respuesta 2",
    "q12": "Respuesta 2",
    "q13": "Respuesta 2",
    "q14": "Respuesta 2",
    "q15": "Respuesta 2",
    "q16": "Respuesta 2",    
    "q17": "Respuesta 2",
    "q17": "Respuesta 2",
    "q18": "Respuesta 2",
    "q19": "Respuesta 2",
    "q20": "Respuesta 2",
    "q21": "Respuesta 2",
    "q22": "Respuesta 2",
    "q23": "Respuesta 23",
    "q24": "Respuesta 23"
    
}'
"""
@interview_customer_bp.route('/', methods=['POST'])
def create_interview_customer():
    data = request.json
    try:
        new_data = InterviewCustomerSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Validar si la ubicación existe
    location = Location.query.get(new_data['id_location'])
    if not location:
        return jsonify({'error': 'Invalid id_location. Location not found.'}), 404

    new_interview_customer = InterviewCustomer(**new_data)

    try:
        db.session.add(new_interview_customer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    interview_customer_schema = InterviewCustomerSchema()
    interview_customer_json = interview_customer_schema.dump(new_interview_customer)
    return jsonify(interview_customer_json), 201


# Eliminar un registro por ID
# curl -X DELETE http://127.0.0.1:5000/interview_customers/1
@interview_customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_interview_customer(id):
    interview_customer = InterviewCustomer.query.get(id)
    if interview_customer:
        db.session.delete(interview_customer)
        db.session.commit()
        return jsonify({'message': 'InterviewCustomer successfully deleted'}), 200
    else:
        return jsonify({'error': 'InterviewCustomer not found'}), 404
    
# Obtener todos los registros
# curl -v http://127.0.0.1:5000/interview_customers/all_interview_customers
@interview_customer_bp.route('/all_interview_customers', methods=['GET'])
def all_interview_customers():
    try:
        interview_customers = InterviewCustomer.query.all()
        interview_customer_schema = InterviewCustomerSchema(many=True)
        result = interview_customer_schema.dump(interview_customers)
        return make_response(jsonify({"interview_customers": result}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    

# Obtener un registro por ID
# curl -v http://127.0.0.1:5000/interview_customers/3
@interview_customer_bp.route('/<int:id>', methods=['GET'])
def get_interview_customer(id):
    interview_customer = InterviewCustomer.query.get(id)
    if interview_customer:
        interview_customer_schema = InterviewCustomerSchema()
        result = interview_customer_schema.dump(interview_customer)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'InterviewCustomer not found'}), 404
    
# Actualizar un registro por ID
'''
curl -X PUT http://127.0.0.1:5000/interview_customers/1 \
-H "Content-Type: application/json" \
-d '{
    "id_location": 2,
    "link": "httt.com",
    "q1": "Respuesta 1",
    "q2": "Respuesta 2",
    "q3": "Respuesta 3",
    "q4": "Respuesta 4",
    "q5": "Respuesta 5",
    "q6": "Respuesta 2",
    "q7": "Respuesta 2",
    "q8": "Respuesta 2",
    "q9": "Respuesta 2",
    "q10": "Respuesta 2",
    "q11": "Respuesta 2",
    "q12": "Respuesta 2",
    "q13": "Respuesta 2",
    "q14": "Respuesta 2",
    "q15": "Respuesta 2",
    "q16": "Respuesta 2",    
    "q17": "Respuesta 2",
    "q17": "Respuesta 2",
    "q18": "Respuesta 2",
    "q19": "Respuesta 2",
    "q20": "Respuesta 2",
    "q21": "Respuesta 2",
    "q22": "Respuesta 2",
    "q23": "Respuesta 23",
    "q24": "Respuesta 23"
    
}'
'''
@interview_customer_bp.route('/<int:id>', methods=['PUT'])
def update_interview_customer(id):
    interview_customer = InterviewCustomer.query.get(id)
    if interview_customer:
        data = request.get_json()

        # Validar la nueva ubicación si se proporciona
        new_location_id = data.get('id_location')
        if new_location_id:
            location = Location.query.get(new_location_id)
            if not location:
                return jsonify({'error': 'Invalid id_location. Location not found.'}), 400

        # Actualizar campos
        interview_customer.id_location = new_location_id if new_location_id else interview_customer.id_location
        interview_customer.link = data.get('link', interview_customer.link)
        
        for i in range(1, 25):
            field_name = f"q{i}"
            setattr(interview_customer, field_name, data.get(field_name, getattr(interview_customer, field_name)))

        # Guardar cambios en la base de datos
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        return jsonify({'message': 'InterviewCustomer updated successfully'}), 200
    else:
        return jsonify({'message': 'InterviewCustomer not found'}), 404