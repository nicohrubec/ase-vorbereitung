from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_user:test_user@localhost:5432/test'
db = SQLAlchemy(app)

max_username_len = 50
max_email_len = 100

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(max_username_len))
    email = db.Column(db.String(max_email_len))

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.serialize() for user in users])


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # validation
    if type(user_id) != int:
        return jsonify({'message': 'Validation failed'}), 422

    user = Users.query.get(user_id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_item():
    data = request.json

    # validation
    if 'username' not in data or 'email' not in data:
        return jsonify({'message': 'Validation failed: Username or Email parameter missing'}), 422
    elif len(data['username']) == 0 or len(data['email']) == 0:
        return jsonify({'message': 'Validation failed: Username or Email parameter empty'}), 422
    elif len(data['username']) > max_username_len or len(data['email']) > max_email_len:
        return jsonify({'message': 'Validation failed: Username or Email too long'}), 422

    new_user = Users(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
