import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource 
from datetime import datetime
from auth_middleware import token_required
from model.pulses import Pulse
pulse_api = Blueprint('pulse_api', __name__,
                   url_prefix='/api/pulses')

api = Api(pulse_api)
class PulseyAPI:
    class _CRUD(Resource):  
        def post(self): 
            ''' Read data for json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
        
            Active = body.get('Active')
            if Active is None or len(Active) < 2:
                return {'message': f'Active is missing, or is less than 2 characters'}, 400
          
            Exercise = body.get('Exercise')
            if Exercise is None or Exercise < 0 :
                return {'message': f'Exercise has to be positive number'}, 400
            ''' #1: Key code block, setup USER OBJECT '''
            newPulse = Pulse(Active=Active,
                      Exercise=Exercise)
            ''' #2: Key Code block to add user to database '''
            just_added_pulse = newPulse.create()
            if just_added_pulse:
                return jsonify(just_added_pulse.read())
         
            return {'message': f'Processed {Active}, either a format error or it is duplicate'}, 400
        def get(self):
            pulses = Pulse.query.all()    
            json_ready = [pulse.read() for pulse in pulses]  
            return jsonify(json_ready)  
        def delete(self):  
            ''' Find user by ID '''
            body = request.get_json()
            del_pulse = body.get('Active')
            result = Pulse.query.filter(Pulse._Active == del_pulse).first()
            if result is None:
                 return {'message': f'pulse {del_pulse} not found'}, 404
            else:
                result.delete()
                print("delete")
    class _get(Resource):
        def get(self, lname=None):  
            print(lname)
            if lname:
                result = Pulse.query.filter_by(_Active=lname).first()
                print(result)
                if result:
                    print(result)
                    return jsonify([result.read()])  # Assuming you have a read() method in your PulseyApi model
                else:
                    return jsonify({"message": "Pulse not found"}), 404

    api.add_resource(_CRUD, '/')
    api.add_resource(_get, '/<string:lname>')