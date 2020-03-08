from flask import Flask
from flask_restful import Api
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.trip import Trip, MyTrips, AllTrips, TripSearch


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True

app.secret_key = 'mynameiskhan'
api = Api(app)




@app.before_first_request
def create_tables():
    db.create_all()



jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    return identity

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(UserRegister,'/register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(Trip,'/trip/<string:name>') #posting a trip POST
api.add_resource(MyTrips,'/mytrips')         #To see trips by a vendor GET
api.add_resource(AllTrips,'/alltrips')       #To see all the trips in the portal GET
api.add_resource(TripSearch,'/trip/<string:name>')  #To search trips for a place GET
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug = True)