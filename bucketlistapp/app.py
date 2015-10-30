from flask.ext.api import FlaskAPI
from flask.ext.api.exceptions import \
    AuthenticationFailed, NotFound, NotAcceptable, ParseError
from exceptions.wailer import CredentialsRequired
from flask import request
from models import db, BucketList, BucketListItem
from transformers.transform_to_dict import list_object_transform
import decorators.enforce as enforce
import auth


def create_app(config_module="config.DevelopmentConfig"):
    '''Wraps the app with view functions decorated with routes into a single
     exportable function.
    '''
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config_module)
    db.init_app(app)

    @app.route("/auth/register", methods=["GET", "POST"])
    def register():
        '''Responds to /auth/register (GET request) by returning
         a JSON response containing instructions.
        It also returns a success message for a POST request to register a
         new user.
        '''
        if request.method == "GET":
            return {
                "message": "Welcome to the bucketlist service",
                "more": "To register make a POST request to /register ENDPOINT\
                with [username] and [password]"
            }, 200
        else:
            username = request.form.get("username")
            password = request.form.get("password")
            if username and password:
                return auth.register(username, password)
            else:
                raise ParseError()

    @app.route("/auth/login", methods=["GET", "POST"])
    def login():
        '''Responds to /auth/login (GET request) by raising a
         CredentialsRequired Exception.
        A valid POST request login a user and returns a token in
         the JSON response returned.
        '''
        if request.method == "GET":
            raise CredentialsRequired()
        username = request.form.get("username")
        password = request.form.get("password")

        if auth.check_auth(username, password):
            return {
                "message": [
                    auth.MESSAGES["login"],
                    {
                        "available endpoints":
                        app.config.get('AVAILABLE_ENDPOINTS')
                    }
                ],
                "token": auth.tokenize(username, password)
            }
        else:
            raise AuthenticationFailed()

    @app.route("/auth/logout", methods=["GET"])
    @enforce.requires_auth
    def logout():
        '''Responds to /auth/logout (GET request) and logout a user.
        '''
        if auth.logout():
            return {"message": auth.MESSAGES["logout"]}
        raise NotFound()

    @app.route("/bucketlists", methods=["POST", "GET"])
    @enforce.requires_auth
    def bucketlist():
        '''Retrieves all bucketlists for a logged in user and returns a
         JSON response for (GET request) to /bucketlists.
        POST requests to this route creates a bucketlist for the logged
         in user.
        '''
        user_id = auth.get_current_user_id()
        if request.method == "GET":
            query = BucketList.query.filter_by(
                created_by=user_id)
            limit = request.args.get('limit', 20)
            q = request.args.get('q')
            page = request.args.get('page', 1)
            result_data = None
            if query.all():
                if not 0 <= int(limit) <= 100:
                    raise NotAcceptable('Maximum limit per page is 100.')
                else:
                    result_data = query
                if q:
                    result_data = query.filter(
                        BucketList.name.ilike('%{0}%'.format(q))
                    )
                result_data = list_object_transform(
                        result_data.paginate(
                            page, int(limit), False
                        ).items)
                return {'message': result_data}
            raise NotFound('There are no bucketlist for this user')

        else:
            name = request.form.get("name")
            a_bucketlist = BucketList(created_by=user_id, name=name)
            a_bucketlist.save()
            return {
                "message": "Bucketlist was created successfully",
                "bucketlist": a_bucketlist.to_json()}, 201

    @app.route("/bucketlists/<int:id>", methods=["GET", "DELETE", "PUT"])
    @enforce.requires_auth
    @enforce.belongs_to_user
    def actionable_bucketlist(id, **kwargs):
        '''Deletes a specific bucketlist record with its bucketlist
         child items (DELETE request).
        Retrieves a specific bucketlist record with its bucketlist
         child items (GET request).
        Updates a specific bucketlist record with its bucketlist
         child items (UPDATE request).
        '''
        bucketlist = BucketList.query.get(id)
        if request.method == "DELETE":
            bucketlist.delete()
            return {"message": "Bucketlist was deleted successfully"}, 200

        elif request.method == "PUT":
            name = request.form.get("name")
            bucketlist.name = name
            bucketlist.save()
        return bucketlist.to_json(), 200

    @app.route("/bucketlists/<int:id>/items", methods=["POST"])
    @enforce.requires_auth
    @enforce.belongs_to_user
    def create_bucketlist_item(id, **kwargs):
        '''Creates a new bucketlist child item of a bucketlist.
        Returns a success message.
        '''
        name = request.form.get('name')
        done = request.form.get('done')
        bucketlistitem = BucketListItem(bucketlist_id=id, name=name, done=done)
        bucketlistitem.save()
        return {
            "message": "Bucketlist item was created successfully",
            "bucketlistitem": bucketlistitem.to_json()}, 201

    @app.route(
        "/bucketlists/<int:id>/items/<int:item_id>",
        methods=["GET", "PUT", "DELETE"])
    @enforce.requires_auth
    @enforce.belongs_to_user
    @enforce.belongs_to_bucketlist
    def actionable_bucketlist_item(id, item_id, **kwargs):
        '''Deletes a specific bucketlist child item (DELETE request).
        Retrieves a specific bucketlist child item (GET request).
        Updates a specific bucketlist child item (UPDATE request).
        '''
        bucketlistitem = kwargs.get('bucketlistitem')
        if request.method == "DELETE":
            bucketlistitem.delete()
            return {"message": "Bucketlist item was deleted successfully"}, 200

        elif request.method == "PUT":
            name = request.form.get("name")
            done = request.form.get("done")
            bucketlistitem.id = item_id
            bucketlistitem.extend(bucketlist_id=id, item_name=name, done=done)
        return bucketlistitem.to_json(), 200
    return app
