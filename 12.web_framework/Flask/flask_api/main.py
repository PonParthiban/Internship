from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/videodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class VideoModel(db.Model):
    __tablename__ = "video_model"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    likes = db.relationship('Like', backref='video', lazy=True)
    views = db.relationship('View', backref='video', lazy=True)


class Like(db.Model):
    __tablename__ = "like"

    id = db.Column(db.Integer, primary_key=True)

    video_id = db.Column(
        db.Integer,
        db.ForeignKey("video_model.id"),
        nullable=False
    )

    user_name = db.Column(db.String(100))


class View(db.Model):
    __tablename__ = "view"

    id = db.Column(db.Integer, primary_key=True)

    video_id = db.Column(
        db.Integer,
        db.ForeignKey("video_model.id"),
        nullable=False
    )

    viewed_at = db.Column(db.DateTime, default=db.func.now())

def get_active_video(vid_id):
    return VideoModel.query.filter_by(id=vid_id, is_deleted=False).first()

vid_put_args = reqparse.RequestParser()
vid_put_args.add_argument("name", type=str, required=True)

vid_patch_args = reqparse.RequestParser()
vid_patch_args.add_argument("name", type=str)

like_args = reqparse.RequestParser()
like_args.add_argument("user_name", type=str, required=True)

resource_fields = {
    "id": fields.Integer,
    "name": fields.String
}

class Video(Resource):

    def get(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")

        like_count = Like.query.filter_by(video_id=vid_id).count()
        view_count = View.query.filter_by(video_id=vid_id).count()

        return {
            "id": video.id,
            "name": video.name,
            "likes": like_count,
            "views": view_count
        }


    @marshal_with(resource_fields)
    def put(self, vid_id):
        args = vid_put_args.parse_args()
        existing = VideoModel.query.get(vid_id)

        if existing and not existing.is_deleted:
            abort(409, message="Video already exists")

        if existing and existing.is_deleted:
            existing.name = args["name"]
            existing.is_deleted = False
            existing.deleted_at = None
            db.session.commit()
            return existing, 200

        video = VideoModel(id=vid_id, name=args["name"])
        db.session.add(video)
        db.session.commit()
        return video, 201


    @marshal_with(resource_fields)
    def patch(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")

        args = vid_patch_args.parse_args()

        if args["name"]:
            video.name = args["name"]

        db.session.commit()
        return video


    def delete(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404)

        video.is_deleted = True
        video.deleted_at = datetime.utcnow()
        db.session.commit()

        return {"message": "Soft deleted"}, 200

class AddLike(Resource):
    def post(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404)

        args = like_args.parse_args()

        # prevent duplicate like
        existing = Like.query.filter_by(
            video_id=vid_id,
            user_name=args["user_name"]
        ).first()

        if existing:
            return {"message": "Already liked"}, 200

        like = Like(video_id=vid_id, user_name=args["user_name"])
        db.session.add(like)
        db.session.commit()

        return {"message": "Liked"}, 201

class AddView(Resource):
    def post(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404)

        view = View(video_id=vid_id)
        db.session.add(view)
        db.session.commit()

        return {"message": "Viewed"}, 201

api.add_resource(Video, "/video/<int:vid_id>")
api.add_resource(AddLike, "/video/<int:vid_id>/like")
api.add_resource(AddView, "/video/<int:vid_id>/view")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)