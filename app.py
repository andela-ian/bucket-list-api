from flask import Flask, jsonify, make_response, request, session
from flask_restful import Resource, Api
from models import db, BucketList, User
import auth


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module or 'config')
    db.init_app(app)
    api = Api(app)

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

    class BucketListMaster(Resource):
        def get(self):
            user_id = auth.get_current_user_id()
            return {'data': db.session
                              .query(BucketList)
                              .filter(user_id == user_id)
                              .all()}

        def post(self):
            user_id = auth.get_current_user_id()
            todo = request.form.get('todo')
            db.session.add(BucketList(user_id, todo))
            db.session.commit()
            return {'data': 'hello'}, 201

    api.add_resource(BucketListMaster, '/bucketlists')

    return app


if __name__ == '__main__':
    bucket_list_app = create_app()
    bucket_list_app.run(debug=True)
