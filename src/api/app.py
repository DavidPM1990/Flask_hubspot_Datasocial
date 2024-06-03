from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from database import db
from routes import webhook_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flask_project_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
migrate = Migrate(app, db)

CORS(app, supports_credentials=True, expose_headers='Authorization')

@app.route('/')
def hello():
    return "Technical Interview to DataSocial!, let's go hard coding!!"

@app.route('/api/<path:path>', methods=['OPTIONS'])
def options(path):
    response = jsonify({'message': 'success'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return response

app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    app.run(debug=True)