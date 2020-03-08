from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.trip import TripModel



class Trip(Resource):
    _trip_parser = reqparse.RequestParser()
    #_trip_parser.add_argument('location',type = str, help = 'This field cannot be blank', required = True)
    _trip_parser.add_argument('price',type = int, help = 'This field cannot be blank', required = True)
    _trip_parser.add_argument('days',type = int, help = 'This field cannot be blank', required = True)
    

    @jwt_required
    def post(self,name):
        claims = get_jwt_claims()
        data = Trip._trip_parser.parse_args()
        trip = TripModel(name,data['price'],data['days'],claims)
        trip.save_to_db()
        return {'trip': trip.json(),'message':'trip has been added to database'}


class TripSearch(Resource):
    def get(self,name):
        trips = [trip.json() for trip in TripModel.find_by_location(name)]
        if trips:
            return trips
        return {'message':'No trip found on this location'}


class MyTrips(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        trips = [trip.json() for trip in TripModel.find_my_trips(claims)]
        return {'trips':trips}

    
class AllTrips(Resource):
    def get(self):
        trips = [trip.json() for trip in TripModel.all_trips()]
        return trips

    