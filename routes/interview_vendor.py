from flask import Blueprint, request, jsonify, make_response
from models import InterviewVendor, Location, db
from schemas import InterviewVendorSchema

interview_vendor_bp = Blueprint('interview_vendors', __name__)

"""
Crear un nuevo registro en InterviewVendor
curl -X POST http://127.0.0.1:5000/interview_vendors/ \
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
    "q23": "Respuesta 23"    
}'
"""
@interview_vendor_bp.route('/', methods=['POST'])
def create_interview_vendor():
    data = request.json
    try:
        new_data = InterviewVendorSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Validar si la ubicación existe
    location = Location.query.get(new_data['id_location'])
    if not location:
        return jsonify({'error': 'Invalid id_location. Location not found.'}), 404

    new_interview_vendor = InterviewVendor(**new_data)

    try:
        db.session.add(new_interview_vendor)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    interview_vendor_schema = InterviewVendorSchema()
    interview_vendor_json = interview_vendor_schema.dump(new_interview_vendor)
    return jsonify(interview_vendor_json), 201


#curl -X DELETE http://127.0.0.1:5000/interview_vendors/1
@interview_vendor_bp.route('/<int:id>', methods=['DELETE'])
def delete_interview_vendor(id):
    interview_vendor = InterviewVendor.query.get(id)
    if interview_vendor:
        db.session.delete(interview_vendor)
        db.session.commit()
        return jsonify({'message': 'InterviewVendor successfully deleted'}), 200
    else:
        return jsonify({'error': 'InterviewVendor not found'}), 404

# curl -v http://127.0.0.1:5000/interview_vendors/all_interview_vendors
@interview_vendor_bp.route('/all_interview_vendors', methods=['GET'])
def all_interview_vendors():
    try:
        interview_vendors = InterviewVendor.query.all()
        interview_vendor_schema = InterviewVendorSchema(many=True)
        result = interview_vendor_schema.dump(interview_vendors)
        return make_response(jsonify({"interview_vendors": result}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# curl -v http://127.0.0.1:5000/interview_vendors/2
@interview_vendor_bp.route('/<int:id>', methods=['GET'])
def get_interview_vendor(id):
    interview_vendor = InterviewVendor.query.get(id)
    if interview_vendor:
        interview_vendor_schema = InterviewVendorSchema()
        result = interview_vendor_schema.dump(interview_vendor)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'InterviewVendor not found'}), 404

'''
curl -X PUT http://127.0.0.1:5000/interview_vendors/1 \
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
    "q23": "Respuesta 23"    
}'
'''
@interview_vendor_bp.route('/<int:id>', methods=['PUT'])
def update_interview_vendor(id):
    interview_vendor = InterviewVendor.query.get(id)
    if interview_vendor:
        data = request.get_json()

        # Validar la nueva ubicación si se proporciona
        new_location_id = data.get('id_location')
        if new_location_id:
            location = Location.query.get(new_location_id)
            if not location:
                return jsonify({'error': 'Invalid id_location. Location not found.'}), 400

        # Actualizar los campos
        interview_vendor.id_location = new_location_id if new_location_id else interview_vendor.id_location
        interview_vendor.link = data.get('link', interview_vendor.link)
        
        for i in range(1, 24):
            field_name = f"q{i}"
            setattr(interview_vendor, field_name, data.get(field_name, getattr(interview_vendor, field_name)))

        # Guardar cambios en la base de datos
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        return jsonify({'message': 'InterviewVendor updated successfully'}), 200
    else:
        return jsonify({'message': 'InterviewVendor not found'}), 404
