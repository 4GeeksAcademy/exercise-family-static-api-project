"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body =members
    return jsonify(response_body), 200
   
@app.route('/members', methods=['POST'])
def add_members():
    body = request.json
    member={
        "first_name":body["first_name"],
        "age":body["age"], 
        "lucky_numbers":body["lucky_numbers"]
    }
      
    jackson_family.add_member(member)
    return jsonify(member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_members(member_id):
    sucess = jackson_family.delete_member(member_id)
    if sucess:
        return jsonify({"msg":"member delete succesfully"}),200
    return jsonify({"error":"member no se ha encontrado "}),400


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    sucess = jackson_family.get_member(member_id)
    if sucess:
        return jsonify({"SUCCESS":sucess}),200
    return jsonify({"error":"member no se ha encontrado"}),404
   
  
    
 


    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
           