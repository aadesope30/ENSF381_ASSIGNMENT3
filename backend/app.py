from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)


#Registration API
@app.route('/signup', methods=['POST'])

def registration():
    data = request.get_json
    username = data.get('username')
    email = data.get('email')
    plain_password = data.get('password')














if __name__ == '__main__':
    app.run()