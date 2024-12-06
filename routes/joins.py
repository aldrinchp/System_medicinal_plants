from flask import Blueprint, request, jsonify, make_response
from models import Image, Plant,Location, PreviousResearch,Use,Toponimo, InterviewCustomer,InterviewVendor,db
from sqlalchemy.orm import joinedload



join_bp = Blueprint('join', __name__)

# Ruta para obtener las imágenes con sus respectivas plantas
#curl -X GET http://127.0.0.1:5000/images_with_plants
@join_bp.route('/images_with_plants', methods=['GET'])
def get_images_with_plants():
    try:
        # Realizar el inner join entre Image y Plant
        results = db.session.query(Image, Plant).join(Plant, Image.plant_id == Plant.id).all()

        # Construir una lista para almacenar los resultados
        output = []
        for image, plant in results:
            output.append({
                "image_id": image.id,
                "plant_id": plant.id,
                "image_date": image.date,
                "image_place": image.place,
                "plant_current_name": plant.current_name,
                "plant_scientific_name": plant.scientific_name
            })

        return jsonify({"images_with_plants": output}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#curl -X GET http://127.0.0.1:5000/images_with_plants_and_locations
@join_bp.route('/images_with_plants_and_locations', methods=['GET'])
def get_images_with_plants_and_locations():
    try:
        # Realizar el INNER JOIN entre las tablas
        results = db.session.query(
            Image.id.label("image_id"),
            Image.date,
            Image.place,
            Plant.id.label("plant_id"),
            Plant.current_name,
            Plant.scientific_name,
            Location.id.label("location_id"),
            Location.city_name.label("location_name")
        ).join(Plant, Plant.id == Image.plant_id) \
         .join(Location, Location.id == Plant.location_id).all()

        # Crear la estructura de respuesta
        data = []
        for row in results:
            data.append({
                "image_id": row.image_id,
                "date": row.date.isoformat(),
                "place": row.place,
                "plant_id": row.plant_id,
                "current_name": row.current_name,
                "scientific_name": row.scientific_name,
                "location_id": row.location_id,
                "location_name": row.location_name
            })

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#curl -X GET http://127.0.0.1:5000/plants_with_research
@join_bp.route('/plants_with_research', methods=['GET'])
def get_plants_with_research():
    try:
        # Consulta INNER JOIN entre plants y previous_researches
        results = (
            db.session.query(
                Plant.id.label('plant_id'),
                Plant.current_name,
                Plant.scientific_name,
                PreviousResearch.id.label('research_id'),
                PreviousResearch.title,
                PreviousResearch.link
            )
            .join(PreviousResearch, Plant.id == PreviousResearch.id_plant)
            .all()
        )

        # Convertir resultados a JSON
        data = [
            {
                "plant_id": result.plant_id,
                "current_name": result.current_name,
                "scientific_name": result.scientific_name,
                "research_id": result.research_id,
                "title": result.title,
                "link": result.link,
            }
            for result in results
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#curl -X GET http://127.0.0.1:5000/plants_with_uses
@join_bp.route('/plants_with_uses', methods=['GET'])
def get_plants_with_uses():
    try:
        # Consulta INNER JOIN entre plants y uses
        results = (
            db.session.query(
                Plant.id.label('plant_id'),
                Plant.current_name,
                Plant.scientific_name,
                Use.id.label('use_id'),
                Use.description,
                Use.type_use
            )
            .join(Use, Plant.id == Use.id_plant)  # Relación entre Plant y Use
            .all()
        )

        # Convertir resultados a JSON
        data = [
            {
                "plant_id": result.plant_id,
                "current_name": result.current_name,
                "scientific_name": result.scientific_name,
                "use_id": result.use_id,
                "description": result.description,
                "type_use": result.type_use,
            }
            for result in results
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#curl -X GET http://127.0.0.1:5000/plants_with_toponimos
@join_bp.route('/plants_with_toponimos', methods=['GET'])
def get_plants_with_toponimos():
    try:
        # Consulta INNER JOIN entre plants y toponimos
        results = (
            db.session.query(
                Plant.id.label('plant_id'),
                Plant.current_name,
                Plant.scientific_name,
                Toponimo.id.label('toponimo_id'),
                Toponimo.origin,
                Toponimo.comercial_distribution,
                Toponimo.distribution
            )
            .join(Toponimo, Plant.id == Toponimo.id_plant)  # Relación entre Plant y Toponimo
            .all()
        )

        # Convertir resultados a JSON
        data = [
            {
                "plant_id": result.plant_id,
                "current_name": result.current_name,
                "scientific_name": result.scientific_name,
                "toponimo_id": result.toponimo_id,
                "origin": result.origin,
                "comercial_distribution": result.comercial_distribution,
                "distribution": result.distribution,
            }
            for result in results
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#curl -X GET http://127.0.0.1:5000/plants_with_locations
@join_bp.route('/plants_with_locations', methods=['GET'])
def get_plants_with_locations():
    try:
        # INNER JOIN entre `plants` y `locations`
        results = (
            db.session.query(
                Plant.id.label('plant_id'),
                Plant.current_name,
                Plant.scientific_name,
                Location.id.label('location_id'),
                Location.city_name,
                Location.id_province
            )
            .join(Location, Plant.location_id == Location.id)  # Relación entre Plant y Location
            .all()
        )

        # Convertir resultados a JSON
        data = [
            {
                "plant_id": result.plant_id,
                "current_name": result.current_name,
                "scientific_name": result.scientific_name,
                "location_id": result.location_id,
                "city_name": result.city_name,
                "id_province": result.id_province,
            }
            for result in results
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#curl -X GET http://127.0.0.1:5000/locations_with_interviews_customers

@join_bp.route('/locations_with_interviews_customers', methods=['GET'])
def get_locations_with_interviews():
    try:
        # Realizar el INNER JOIN entre locations e interview_customers
        results = (
            db.session.query(
                Location.id.label('location_id'),
                Location.city_name,
                Location.id_province,
                InterviewCustomer.id.label('interview_id'),
                InterviewCustomer.link,
                InterviewCustomer.q1,
                InterviewCustomer.q2,
                InterviewCustomer.q3,
                InterviewCustomer.q4,
                InterviewCustomer.q5,
                InterviewCustomer.q6,
                InterviewCustomer.q7,
                InterviewCustomer.q8,
                InterviewCustomer.q9,
                InterviewCustomer.q10,
                InterviewCustomer.q11,
                InterviewCustomer.q12,
                InterviewCustomer.q13,
                InterviewCustomer.q14,
                InterviewCustomer.q15,
                InterviewCustomer.q16,
                InterviewCustomer.q17,
                InterviewCustomer.q18,
                InterviewCustomer.q19,
                InterviewCustomer.q20,
                InterviewCustomer.q21,
                InterviewCustomer.q22,
                InterviewCustomer.q23,
                InterviewCustomer.q24
            )
            .join(InterviewCustomer, Location.id == InterviewCustomer.id_location)  # Relación entre Location e InterviewCustomer
            .all()
        )

        # Convertir los resultados a formato JSON
        data = [
            {
                "location_id": result.location_id,
                "city_name": result.city_name,
                "id_province": result.id_province,
                "interview_id": result.interview_id,
                "link": result.link,
                "q1": result.q1,
                "q2": result.q2,
                "q3": result.q3,
                "q4": result.q4,
                "q5": result.q5,
                "q6": result.q6,
                "q7": result.q7,
                "q8": result.q8,
                "q9": result.q9,
                "q10": result.q10,
                "q11": result.q11,
                "q12": result.q12,
                "q13": result.q13,
                "q14": result.q14,
                "q15": result.q15,
                "q16": result.q16,
                "q17": result.q17,
                "q18": result.q18,
                "q19": result.q19,
                "q20": result.q20,
                "q21": result.q21,
                "q22": result.q22,
                "q23": result.q23,
                "q24": result.q24
            }
            for result in results
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#curl -X GET http://127.0.0.1:5000/locations_with_interviews_vendors
@join_bp.route('/locations_with_interviews_vendors', methods=['GET'])
def get_locations_with_interviews_vendors():
    try:
        # Realizar el INNER JOIN entre locations e interview_vendors
        results = (
            db.session.query(
                Location.id.label('location_id'),
                Location.city_name,
                Location.id_province,
                InterviewVendor.id.label('interview_id'),
                InterviewVendor.link,
                InterviewVendor.q1,
                InterviewVendor.q2,
                InterviewVendor.q3,
                InterviewVendor.q4,
                InterviewVendor.q5,
                InterviewVendor.q6,
                InterviewVendor.q7,
                InterviewVendor.q8,
                InterviewVendor.q9,
                InterviewVendor.q10,
                InterviewVendor.q11,
                InterviewVendor.q12,
                InterviewVendor.q13,
                InterviewVendor.q14,
                InterviewVendor.q15,
                InterviewVendor.q16,
                InterviewVendor.q17,
                InterviewVendor.q18,
                InterviewVendor.q19,
                InterviewVendor.q20,
                InterviewVendor.q21,
                InterviewVendor.q22,
                InterviewVendor.q23
                # Agregar más preguntas (q6 a q23) si es necesario
            )
            .join(InterviewVendor, Location.id == InterviewVendor.id_location)  # Relación entre Location e InterviewVendor
            .all()
        )

        # Convertir los resultados a formato JSON
        data = [
            {
                "location_id": result.location_id,
                "city_name": result.city_name,
                "id_province": result.id_province,
                "interview_id": result.interview_id,
                "link": result.link,
                "q1": result.q1,
                "q2": result.q2,
                "q3": result.q3,
                "q4": result.q4,
                "q5": result.q5,
                "q6": result.q6,
                "q7": result.q7,
                "q8": result.q8,
                "q9": result.q9,
                "q10": result.q10,
                "q11": result.q11,
                "q12": result.q12,
                "q13": result.q13,
                "q14": result.q14,
                "q15": result.q15,
                "q16": result.q16,
                "q17": result.q17,
                "q18": result.q18,
                "q19": result.q19,
                "q20": result.q20,
                "q21": result.q21,
                "q22": result.q22,
                "q23": result.q23
            }
            for result in results
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500