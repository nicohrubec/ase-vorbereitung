from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_user:test_user@localhost:5432/test'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))

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


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'message': 'Item not found'}), 404


@app.route('/users', methods=['POST'])
def create_item():
    data = request.json
    new_user = Users(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
