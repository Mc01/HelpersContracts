import json
import secrets
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from web3 import Web3, HTTPProvider
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

ACCOUNT = '0x6178923f53573Ef3f7ABda09498e53023A82ae31'
ADDRESS = '0x6bBE47c3d5E82e0Fc0CB5523B0c75A6787f2274B'
 
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

    columns_to_serialize = (
        'id',
        'username',
        'rating',
        'token',
        'reviews_number',
    )

    @property
    def reviews_number(self):
        return charity_profile.functions.profiles__last_review_no(self.token).call()

    @property
    def rating(self):
        return self.rating_points / self.rating_number if self.rating_number > 0 else 0.0

    def __init__(self, *args, **kwargs):
        # kwargs['token'] = secrets.token_bytes(32)
        charity_profile.functions.create_profile(
            kwargs['username'].encode(),
            kwargs['token'].encode(),
        ).transact({'from': ACCOUNT})
        return super().__init__(*args, **kwargs)


class Help(SerializableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, default='', nullable=False)
    categories = db.Column(db.Text, default='[]', nullable=False)
    start_data = db.Column(db.DateTime(), unique=False, nullable=True, default=datetime.utcnow)
    accepted_data = db.Column(db.DateTime(), unique=False, nullable=True, default=datetime.utcnow)
    end_data = db.Column(db.DateTime(), unique=False, nullable=True, default=datetime.utcnow)

    helper_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    requester_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)

    finished = db.Column(db.Boolean, default=False)
    review_id = db.Column(db.String(32), default=None, nullable=True)

    columns_to_serialize = (
        'id',
        'start_data',
        'accepted_data',
        'end_data',
        'helper_id',
        'requester_id',
        'finished',
        'review_id'
    )

db.create_all()

if User.query.count() == 0:
    db.session.add(
        User(username='user1', password='test', token='sec1')
    )
    db.session.add(
        User(username='user2', password='test', token='sec2')
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

@app.route('/create', methods=['POST'])
@jwt_required()
def create_request():
    data = request.get_json()
    mode = data.pop('mode')
    if mode == 'get':
        data['requester_id'] = current_identity.id
    elif mode == 'give':
        data['helper_id'] = current_identity.id
    help = Help(**data)
    db.session.add(help)
    db.session.commit()
    return help.as_dict()



@app.route('/accept/<request_id>')
@jwt_required()
def accept(request_id):
    help = Help.query.get(request_id)
    if help.requester_id == None:
        help.requester_id = current_identity.id
        help.accepted_data = datetime.utcnow()
    elif help.helper_id == None:
        help.helper_id = current_identity.id
        help.accepted_data = datetime.utcnow()
    db.session.commit()
    return help.as_dict()


@app.route('/finish_help/<help_id>')
@jwt_required()
def finish_help(help_id):
    help = Help.query.get(help_id)
    if help.requester_id == current_identity.id:
        help.finished = True
        help.end_data = datetime.utcnow()
        db.session.commit()
    return help.as_dict()


def _add_review(rated_user_id, score=1, brief='', url=''):
    token = User.query.get(1).token
    reviewer_name = current_identity.username
    charity_profile.functions.add_review(
        token,
        reviewer_name.encode(),
        score,
        brief.encode(),
        url.encode(),
    ).transact({'from': ACCOUNT})


@app.route('/add_review/<help_id>', methods=['POST'])
@jwt_required()
def add_review(help_id):
    return str(charity_profile.functions.add_review(
        current_identity.token.encode(),
        "sratatata".encode(),
        [1,2,3,4,5,5],
        "note".encode(),
        "url".encode(),
    ).transact({'from': ACCOUNT}))
    # help = Help.query.get(help_id)
    # data = request.get_json()
    # # if (help.requester_id == current_identity.id and help.finished):
    # _add_review(
    #     help.helper_id,
    #     data['score'],
    #     data['review']
    # )
    # db.session.commit()
    # return help.as_dict()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')