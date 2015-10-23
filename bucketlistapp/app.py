from flask.ext.api import FlaskAPI
from flask.ext.api.exceptions import \
    AuthenticationFailed, NotFound, NotAcceptable, ParseError
from exceptions.wailer import CredentialsRequired
from flask import request
from models import db, BucketList, BucketListItem
from transformers.transform_to_dict import list_object_transform
from .decorators import auth


def create_app(config_module="config.DevelopmentConfig"):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config_module)
    db.init_app(app)

    @app.route("/auth/register", methods=["GET", "POST"])
    def register():
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
    @auth.requires_auth
    def logout():
        if auth.logout():
            return {"message": auth.MESSAGES["logout"]}
        raise NotFound()

    @app.route("/bucketlists", methods=["POST", "GET"])
    @auth.requires_auth
    def bucketlist():
        user_id = auth.get_current_user_id()
        if request.method == "GET":
            query = BucketList.query.filter(
                user_id == user_id)
            limit = request.args.get('limit')
            q = request.args.get('q')
            if query.all():
                if not limit:
                    result_data = list_object_transform(query.all())
                else:
                    if 0 <= int(limit) <= 100:
                        result_data = list_object_transform(
                            BucketListItem.query.paginate(
                                1, int(limit), False
                            ).items
                        )
                    else:
                        raise NotAcceptable()
                if q:
                    result_data = list_object_transform(
                        BucketList.query.filter(
                            BucketList.name.ilike('%{0}%'.format(q))
                        ).all()
                    )
                return {'message': result_data}
            raise NotFound()

        else:
            name = request.form.get("name")
            a_bucketlist = BucketList(created_by=user_id, name=name)
            db.session.add(a_bucketlist)
            db.session.commit()
            return {
                "message": "Bucketlist was created successfully",
                "bucketlist": a_bucketlist.to_json()}, 201

    @app.route("/bucketlists/<int:id>", methods=["GET", "DELETE", "PUT"])
    @auth.requires_auth
    @auth.belongs_to_user
    def actionable_bucketlist(id, **kwargs):
        bucketlist = BucketList.query.get(id)
        if request.method == "DELETE":
            db.session.delete(bucketlist)
            db.session.commit()
            return {"message": "Bucketlist was deleted successfully"}, 200

        elif request.method == "PUT":
            name = request.form.get("name")
            bucketlist.name = name
            db.session.commit()
        return bucketlist.to_json(), 200

    @app.route("/bucketlists/<int:id>/items", methods=["POST"])
    @auth.requires_auth
    @auth.belongs_to_user
    def create_bucketlist_item(id, **kwargs):
        name = request.form.get('name')
        done = request.form.get('done')
        bucketlistitem = BucketListItem(bucketlist_id=id, name=name, done=done)
        db.session.add(bucketlistitem)
        db.session.commit()
        return {
            "message": "Bucketlist item was created successfully",
            "bucketlistitem": bucketlistitem.to_json()}, 201

    @app.route(
        "/bucketlists/<int:id>/items/<int:item_id>",
        methods=["GET", "PUT", "DELETE"])
    @auth.requires_auth
    @auth.belongs_to_user
    @auth.belongs_to_bucketlist
    def actionable_bucketlist_item(id, item_id, **kwargs):
        bucketlistitem = kwargs.get('bucketlistitem')
        if request.method == "DELETE":
            db.session.delete(bucketlistitem)
            db.session.commit()
            return {"message": "Bucketlist item was deleted successfully"}, 200

        elif request.method == "PUT":
            name = request.form.get("name")
            done = request.form.get("done")
            bucketlistitem.name = name
            bucketlistitem.done = done
            bucketlistitem.id = item_id
            bucketlistitem.bucketlist_id = id
            db.session.commit()
        return bucketlistitem.to_json(), 200
    return app
