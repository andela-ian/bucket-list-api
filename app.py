from flask import Flask, jsonify, make_response, request, session
from models import db
import auth


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module or 'config')
    db.init_app(app)

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')

        if auth.check_auth(username, password):
            session['user'] = [username, password]
            return make_response(
                jsonify({'message': 'Logged in successfully'}), 200)

    @app.route('/logout', methods=['GET'])
    @auth.requires_auth
    def logout():
        session.pop('user', None)
        return make_response(jsonify({'message': 'Logged out successfully'}))

    @app.route('/home', methods=['GET'])
    @auth.requires_auth
    def index():
        return make_response(jsonify({}), 200)

    return app

if __name__ == '__main__':
    bucket_list_app = create_app()
    bucket_list_app.run(debug=True)
