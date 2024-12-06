from flask import Blueprint, request, jsonify, make_response
from models import Location, db
from schemas import LocationSchema

location_bp = Blueprint('locations', __name__)

'''
curl -X POST http://127.0.0.1:5000/locations/ \
-H "Content-Type: application/json" \
-d '{
    "city_name": "Ambato",
    "id_province": 146
}'
'''

@location_bp.route('/',methods=['GET','POST'])
def create_location():
    #Parse   JSON data from the  request
    data =   request.json
    #validateand  deserialize JSON  data  using   LocationSchema
    try:
        new_data= LocationSchema().load(data)
    except Exception as e:
        return  jsonify({'error':str(e)}),400

    #Create a location instance using the deserialized  data
    new  =  Location(**new_data)
    #Add the  new  location  to thedatabase
    try:
        db.session.add(new)
        db.session.commit()
    except Exception  as e:
        db.session.rollback()
        return jsonify({'error': str(e)}),  500

    #Serialize the created location and return the response
    location = LocationSchema()
    location_json = location.dump(new)
    return jsonify (location_json), 201


#curl -X DELETE http://127.0.0.1:5000/locations/1
#Route to delete an author by ID
@location_bp.route('/<int:id>',methods = ['DELETE'])
def delete_location(id):
    location = Location.query.get(id)
    if location:
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message':'Location and related plants successfully deleted'})
    else:
        return jsonify({'error':'location not found'}), 404 


#Retrieve all the registers of a table
#curl -v http://127.0.0.1:5000/locations/all_locations
@location_bp.route('/all_locations', methods = ['GET'])
def all_locations():
    try:
        get_locations = Location.query.all()
        location_schema = LocationSchema(many = True)
        locations = location_schema.dump(get_locations)
        return make_response(jsonify({"locations": locations}),200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
#Retrieve an register  by ID
#curl -v http://127.0.0.1:5000/locations/1
@location_bp.route('/<int:id>',methods = ['GET'])
def get_location(id):
    location = Location.query.get(id)
    if location:
        location_schema = LocationSchema()
        location_json = location_schema.dump(location)
        return jsonify(location_json), 200
    else:
        return jsonify({'message': 'Location not found'}), 404
    
#Route to update an register by ID
'''
curl -X PUT http://127.0.0.1:5000/locations/4 \
     -H "Content-Type: application/json" \
     -d '{"city_name": "Ambato", 
          "id_province": 564
          }'
'''
@location_bp.route('/<int:id>', methods = ['PUT'])
def update_location(id):
    location =  Location.query.get(id)
    if location:
        data = request.get_json()
        location.city_name = data.get('city_name', location.city_name)
        location.id_province= data.get('id_province', location.id_province)

        db.session.commit()
        return jsonify({'message':'Location update successfully'}),200
    else: 
        return jsonify({'message':'Location not found'}), 404

    