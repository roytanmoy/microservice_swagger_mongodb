
TOKENS = {
    '123': 'jdoe',
    '456': 'rms'
}


def token_info(access_token) -> dict:

    uid = TOKENS.get(access_token)
    if not uid:
        return None
    return {'uid': uid, 'scope': ['uid']}















#import cryptography.hazmat.backends.openssl.rsa
#import jwt
#import json
#import requests
#import connexion
#from connexion import request
#from functools import lru_cache

"""
#from app import injector
#from injector import inject
#from services.mongodb import MongoCollection
from flask import Flask, abort, request, jsonify, g, url_for
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

class User():
    #__tablename__ = 'users'
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(32), index=True)
    #password_hash = db.Column(db.String(64))

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

"""

"""
def basic_auth1(username, password, required_scopes=None):
    import pdb; pdb.set_trace()
    if username == 'admin' and password == 'secret':
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None


def get_secret(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)

"""

"""
def get_secret(user) -> str:
    import pdb;
    pdb.set_trace()
    return 'You are: {uid}'.format(uid=user)

# our hardcoded mock "Bearer" access tokens
TOKENS = {
    '123': 'jdoe',
    '456': 'rms'
}

def checktoken(access_token) -> dict:
    import pdb; pdb.set_trace()
    try:
        token = access_token
    except Exception:
        access_token = ''

    uid = TOKENS.get(token)

    if not uid:
        return 'No such token', 401

    return {'uid': uid, 'scope': ['uid']}



def checktoken(access_token) -> dict:

  try:
    decoded_token = decode_token(access_token, 'https://api.d10l.de')
  except:
      raise Exception('decode error')

  decoded_token['uid'] = decoded_token['sub']
  return decoded_token


def decode_token(token: str, oauth_client_id: str):
    token_signing_key_id = _get_token_signing_key_id(token)
    keys = _get_public_keys()
    # TODO if the key ID is not in the set, return 401.
    token_key = keys[token_signing_key_id]

    return jwt.decode(
        token,
        key=token_key,
        audience=oauth_client_id)


def _get_token_signing_key_id(token: str) -> str:

    parse_token_output = jwt.PyJWS()._load(token)
    # the outputs are payload, signing_input, header, signature
    token_header = parse_token_output[2]
    return token_header['kid']


@lru_cache(maxsize=1)
def _get_public_keys() -> dict:

    public_keys_url = 'https://d10l.eu.auth0.com/.well-known/jwks.json'
    jwk_set = requests.get(public_keys_url).json()
    print(jwk_set)
    public_keys = {}
    for key_dict in jwk_set['keys']:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
        public_keys[key_dict['kid']] = public_key
    return public_keys
"""