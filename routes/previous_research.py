from flask import Blueprint, request, jsonify, make_response
from models import PreviousResearch, Plant, db
from schemas import PreviousResearchSchema

previous_research_bp = Blueprint('previous_researches', __name__)

'''
curl -X POST http://127.0.0.1:5000/previous_researches/ \
-H "Content-Type: application/json" \
-d '{
    "id_plant": 5,
    "title": "elpepe",
    "link": "aldrinchp@gmail.com"
}'
'''
@previous_research_bp.route('/', methods=['POST'])
def create_previous_research():
    data = request.json
    try:
        new_data = PreviousResearchSchema().load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    plant = Plant.query.get(new_data['id_plant'])
    if not plant:
        return jsonify({'error': 'Invalid id_plant. Plant not found.'}), 404

    new_research = PreviousResearch(**new_data)

    try:
        db.session.add(new_research)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    previous_research_schema = PreviousResearchSchema()
    research_json = previous_research_schema.dump(new_research)
    return jsonify(research_json), 201


#curl -X DELETE http://127.0.0.1:5000/previous_researches/5
@previous_research_bp.route('/<int:id>', methods=['DELETE'])
def delete_previous_research(id):
    research = PreviousResearch.query.get(id)
    if research:
        db.session.delete(research)
        db.session.commit()
        return jsonify({'message': 'Previous research successfully deleted'}), 200
    else:
        return jsonify({'error': 'Previous research not found'}), 404

#curl -v http://127.0.0.1:5000/previous_researches/all_researches

@previous_research_bp.route('/all_researches', methods=['GET'])
def all_previous_researches():
    try:
        get_researches = PreviousResearch.query.all()
        research_schema = PreviousResearchSchema(many=True)
        researches = research_schema.dump(get_researches)
        return make_response(jsonify({"researches": researches}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
# curl -v http://127.0.0.1:5000/previous_researches/6
@previous_research_bp.route('/<int:id>', methods=['GET'])
def get_previous_research(id):
    research = PreviousResearch.query.get(id)
    if research:
        research_schema = PreviousResearchSchema()
        research_json = research_schema.dump(research)
        return jsonify(research_json), 200
    else:
        return jsonify({'message': 'Previous research not found'}), 404

'''
 Route to update a plant by ID
 curl -X PUT http://127.0.0.1:5000/previous_researches/4 \
      -H "Content-Type: application/json" \
      -d '{
            "id_plant": 5,
            "title": "elpepe",
            "link": "aldrinchp@gmail.com"
        }'
'''

@previous_research_bp.route('/<int:id>', methods=['PUT'])
def update_previous_research(id):
    research = PreviousResearch.query.get(id)
    if research:
        data = request.get_json()

        new_plant_id = data.get('id_plant')
        if new_plant_id:
            plant = Plant.query.get(new_plant_id)
            if not plant:
                return jsonify({'error': 'Invalid id_plant. Plant not found.'}), 400
        research.id_plant = new_plant_id if new_plant_id else research.id_plant
        research.title = data.get('title', research.title)
        research.link = data.get('link', research.link)

        # Realiza el commit para guardar los cambios
        db.session.commit()

        return jsonify({'message': 'Previous research updated successfully'}), 200
    else:
        return jsonify({'message': 'Previous research not found'}), 404
