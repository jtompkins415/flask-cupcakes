"""Flask app for Cupcakes"""

import re
from flask import Flask, render_template, redirect, session, flash, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'seCreETCUpcake234'

connect_db(app)

def serialize_cupcake(cupcake):
    '''Serialize a cupcake SQLAlchemy obj to dictionary'''

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route('/', methods=['GET'])
def cupcake_homepage():
    '''Render home page'''

    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    '''Return JSON data of all cupcakes'''

    cakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_single_cupcake(cupcake_id):
    '''Return JSON data of a single cupcake'''

    cake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Create new instance of Cupcake'''

    '''Returns JSON data of new cupcake'''
    # import pdb
    # pdb.set_trace()

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = None

    if 'image' in request.json:
        image = request.json['image']
    

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    

    return jsonify(cupcake=serialize_cupcake(new_cupcake)), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''Update Cupcake instance and return JSON data'''

    cake = Cupcake.query.get_or_404(cupcake_id)

    cake.flavor = request.json.get('flavor', cake.flavor)
    cake.size = request.json.get('size', cake.size)
    cake.rating = request.json.get('rating', cake.rating)
    
    
    db.session.add(cake)
    db.session.commit()

    return jsonify(cupcake=serialize_cupcake(cake)), 200

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id): 
    '''Delete Cupcake instance from DB'''

    cake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cake)
    db.session.commit()

    return jsonify(message = 'Cupcake deleted!')