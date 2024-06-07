from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from src.api.routes import webhook_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flask_project_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'


CORS(app, supports_credentials=True, expose_headers='Authorization')

@app.route('/')
def hello():
    message = """
    <html>
    <head>
        <title>DataSocial Technical Interview</title>
    </head>
    <body>
        <h1>Welcome to DataSocial Technical Interview!</h1>
        <p>To begin using the integration with HubSpot, follow these steps:</p>
        <ol>
            <li><strong>Create a HubSpot Account:</strong>
                <p>If you don't have a HubSpot account yet, you need to create one before proceeding. You can sign up for a free account <a href="https://app.hubspot.com/signup/crm/step/user-info?hubs_signup-url=www.hubspot.es%2F&hubs_signup-cta=homepage-nav1&hubs_content=www.hubspot.es%2F&hubs_content-cta=homepage-nav1&__hstc=246515761.27f75c9dbf79bc47e8884e48c40607b8.1633185813785.1633185813785.1633185813785.1&__hssc=246515761.1.1633185813785&__hsfp=2753136826&_ga=2.44693689.756705304.1633185814-237201934.1633185814">here</a>.</p>
            </li>
            <li><strong>Login to Postman:</strong>
                <p>If you haven't already, log in to your Postman account <a href="https://identity.getpostman.com/login">here</a>.</p>
            </li>
            <li><strong>Authorization:</strong>
                <p>Go to the link below to obtain HubSpot authorization:</p>
                <p><a href="https://datasocial-dot-hubspot-flask-project.uc.r.appspot.com/authorize">Authorize HubSpot</a></p>
                <p>This will return an authorization page to select your account and your project. You will then receive an informative message back in Postman with further instructions.</p>
            </li>
            <li><strong>Contact Update:</strong>
                <p>After authorization, make a POST request to the following URL in Postman to update the contact details:</p>
                <pre><code>POST https://datasocial-dot-hubspot-flask-project.uc.r.appspot.com/webhook</code></pre>
                <p>The body of the request should be a JSON object with the following structure:</p>
                <pre><code>{
    "email": "example@example.com",
    "name": "example"
}</code></pre>
                <p>Make sure to replace "example@example.com" and "example" with the appropriate values. Once the data is sent, the contact update will be complete.</p>
            </li>
        </ol>
    </body>
    </html>
    """
    return message

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
