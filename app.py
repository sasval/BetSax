from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betsax.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    match = db.Column(db.String(100), nullable=False)
    tip = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(10), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    predictions = Prediction.query.all()
    return jsonify([{
        'id': p.id,
        'date': p.date,
        'match': p.match,
        'tip': p.tip,
        'result': p.result
    } for p in predictions])

@app.route('/api/predictions', methods=['POST'])
def add_prediction():
    data = request.json
    prediction = Prediction(
        date=data['date'],
        match=data['match'],
        tip=data['tip'],
        result=data.get('result')
    )
    db.session.add(prediction)
    db.session.commit()
    return jsonify({'message': 'Prediction added successfully!'}), 201

@app.route('/api/predictions/<int:id>', methods=['PUT'])
def update_prediction(id):
    prediction = Prediction.query.get(id)
    if not prediction:
        return jsonify({'message': 'Prediction not found'}), 404
    data = request.json
    prediction.date = data['date']
    prediction.match = data['match']
    prediction.tip = data['tip']
    prediction.result = data.get('result')
    db.session.commit()
    return jsonify({'message': 'Prediction updated successfully!'})

@app.route('/api/predictions/<int:id>', methods=['DELETE'])
def delete_prediction(id):
    prediction = Prediction.query.get(id)
    if not prediction:
        return jsonify({'message': 'Prediction not found'}), 404
    db.session.delete(prediction)
    db.session.commit()
    return jsonify({'message': 'Prediction deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

