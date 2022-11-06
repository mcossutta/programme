from app.api import bp

@bp.route("/users/<id>",methods=["GET"])
def get_user(id):
    pass
