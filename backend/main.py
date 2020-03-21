import json
import secrets
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from web3 import Web3, HTTPProvider
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

PK = '0x133ddc5032a64f4047a7359741fb8560c1dfd31e077ccf4073421cb5d995911b'
AA = '0x05FE43dddAaC4201978550Fd25c69bBea48Ba230'
ADDRESS = '0xDf41f24cF1da31BF4510B5879e1659a39D178034'
 
# ------------ SETUP PART ---------------------------------

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '!@#$%^1234567abcde'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
w3 = Web3(HTTPProvider('http://ganache:7545'))
with open('/app/abi.json') as f:
    abi = json.load(f)['abi']
charity_profile = w3.eth.contract(
    address=ADDRESS,
    abi=abi
)

class SerializableMixin:
    def as_dict(self):
       return {column: getattr(self, column) for column in self.columns_to_serialize}

class User(SerializableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    token = db.Column(db.String(70), unique=True, nullable=False)
    rating_number = db.Column(db.Integer, default=0)
    rating_points = db.Column(db.Integer, default=0)

    columns_to_serialize = ('id', 'username', 'rating')

    @property
    def rating(self):
        return self.rating_points / self.rating_number if self.rating_number > 0 else 0.0

    def __init__(self, *args, **kwargs):
        kwargs['token'] = secrets.token_bytes(32)
        print(charity_profile.functions.create_profile(
            kwargs['username'].encode(),
            kwargs['token']
        ).transact({'from': AA}))
        return super().__init__(*args, **kwargs)


class Help(SerializableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_data = db.Column(db.DateTime(), unique=False, nullable=True, default=datetime.utcnow)
    name = db.Column(db.String(150), unique=False, nullable=False)

    helper_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    finished_by_helper = db.Column(db.Boolean, default=False)
    finished_by_receiver = db.Column(db.Boolean, default=False)

    review_id = db.Column(db.String(32), default=None, nullable=True)

    columns_to_serialize = ('id', 'start_data', 'helper_id', 'receiver_id', 'finished_by_helper', 'finished_by_receiver', 'review_id')

class Offer(SerializableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    columns_to_serialize = ('id', 'name', 'user_id')

class Request(SerializableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    columns_to_serialize = ('id', 'name', 'user_id')

db.create_all()

if User.query.count() == 0:
    db.session.add(
        User(username='user1', password='test')
    )
    db.session.add(
        User(username='user2', password='test')
    )
    db.session.commit()

def authenticate(username, password):
    users = User.query.filter_by(username=username, password=password)
    return users.first() if users.count() == 1 else None

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(app, authenticate, identity)

# ------------ MAIN PART ---------------------------------
 

@app.route('/health')
def health_check(): return "OK"


@app.route('/profile')
@jwt_required()
def profile():
    return current_identity.as_dict()


@app.route('/web3')
def web3():

    return str(charity_profile.functions.owner().call())


@app.route('/create_request', methods=['POST'])
@jwt_required()
def create_request():
    data = request.get_json()
    data['user_id'] = current_identity.id
    request = Offer(**data)
    db.session.add(request)
    db.session.commit()
    return request.as_dict()


@app.route('/create_offer', methods=['POST'])
@jwt_required()
def create_offer():
    data = request.get_json()
    data['user_id'] = current_identity.id
    offer = Offer(**data)
    db.session.add(offer)
    db.session.commit()
    return offer.as_dict()


@app.route('/offer_help/<request_id>')
@jwt_required()
def offer_help(request_id):
    request = Request.query.get(request_id)
    help = Help(
        helper_id=current_identity.id,
        receiver_id=request.user_id,
        name=request.name,
    )
    db.session.add(help)
    db.session.delete(request)
    db.commit()
    return help.as_dict()


@app.route('/receive_help/<offer_id>')
@jwt_required()
def receive_help(offer_id):
    offer = Offer.query.get(offer_id)
    help = Help(
        helper_id=offer.user_id,
        receiver_id=current_identity.id,
        name=offer.name,
    )
    db.session.add(help)
    db.session.delete(offer)
    db.session.commit()
    return help.as_dict()


@app.route('/finish_help/<help_id>')
@jwt_required()
def finish_help(help_id):
    help = Help.query.get(help_id)
    if help.receiver_id == current_identity.id:
        help.finished_by_receiver = True
    elif help.helper_id == current_identity.id:
        help.finished_by_helper = True
    db.session.commit()
    return help.as_dict()


def add_review(rated_user_id, score=1, brief='', url=''):
    token = User.query.get(rated_user_id).token
    reviewer_name = current_identity.username
    charity_profile.functions.add_review(
        token,
        reviewer_name.encode(),
        score,
        brief.encode(),
        url.encode()
    ).transact({'from': AA})


@app.route('/give_review/<help_id>', methods=['POST'])
@jwt_required()
def give_review(help_id):
    help = Help.query.get(help_id)
    data = request.get_json()
    if (help.receiver_id == current_identity.id and 
    help.finished_by_helper and help.finished_by_receiver):
        add_review(
            help.helper_id,
            data['score'],
            data['review']
        )
        db.session.commit()
    return help.as_dict()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')