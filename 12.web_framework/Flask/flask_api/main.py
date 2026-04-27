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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    likes_data = db.relationship('Like', backref='video', lazy=True)
    views_data = db.relationship('View', backref='video', lazy=True)

def get_active_video(vid_id):
    return VideoModel.query.filter_by(id=vid_id, is_deleted=False).first()

vid_put_args = reqparse.RequestParser()
vid_put_args.add_argument("name", type=str, required=True)
vid_put_args.add_argument("views", type=int, required=True)
vid_put_args.add_argument("likes", type=int, required=True)

vid_patch_args = reqparse.RequestParser()
vid_patch_args.add_argument("name", type=str)
vid_patch_args.add_argument("views", type=int)
vid_patch_args.add_argument("likes", type=int)

like_args = reqparse.RequestParser()
like_args.add_argument("user_name", type=str, required=True, help="User name is required")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    video_id = db.Column(
        db.Integer,
        db.ForeignKey("video_model.id"),
        nullable=False
    )
    user_name = db.Column(db.String(100))

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    video_id = db.Column(
        db.Integer,
        db.ForeignKey("video_model.id"),
        nullable=False
    )
    viewed_at = db.Column(db.DateTime, default=db.func.now())

class Video(Resource):

    @marshal_with(resource_fields)
    def get(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")
        return video


    @marshal_with(resource_fields)
    def put(self, vid_id):
        args = vid_put_args.parse_args()
        existing = VideoModel.query.get(vid_id)

        # If exists and active → conflict
        if existing and not existing.is_deleted:
            abort(409, message="Video already exists")

        # If exists but soft deleted → restore + update
        if existing and existing.is_deleted:
            existing.name = args["name"]
            existing.views = args["views"]
            existing.likes = args["likes"]
            existing.is_deleted = False
            existing.deleted_at = None
            db.session.commit()
            return existing, 200

        # Else create new
        video = VideoModel(
            id=vid_id,
            name=args["name"],
            views=args["views"],
            likes=args["likes"]
        )

        db.session.add(video)
        db.session.commit()
        return video, 201


    @marshal_with(resource_fields)
    def patch(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")

        args = vid_patch_args.parse_args()

        if args["name"] is not None:
            video.name = args["name"]
        if args["views"] is not None:
            video.views = args["views"]
        if args["likes"] is not None:
            video.likes = args["likes"]

        db.session.commit()
        return video, 200


    def delete(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")

        video.is_deleted = True
        video.deleted_at = datetime.utcnow()

        db.session.commit()
        return {"message": "Soft deleted successfully"}, 200

class VideoHardDelete(Resource):
    def delete(self, vid_id):
        video = VideoModel.query.get(vid_id)

        if not video:
            abort(404, message="Video not found")

        # Only allow hard delete if already soft deleted
        if not video.is_deleted:
            abort(400, message="Soft delete first before permanent deletion")

        db.session.delete(video)
        db.session.commit()
        return {"message": "Permanently deleted"}, 200

class VideoRestore(Resource):
    def patch(self, vid_id):
        video = VideoModel.query.get(vid_id)

        if not video:
            abort(404, message="Video not found")

        if not video.is_deleted:
            abort(400, message="Video is not deleted")

        video.is_deleted = False
        video.deleted_at = None

        db.session.commit()
        return {"message": "Restored successfully"}, 200
    
class AddLike(Resource):
    def post(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")

        args = like_args.parse_args()

        like = Like(
            video_id=vid_id,
            user_name=args["user_name"]
        )

        db.session.add(like)
        db.session.commit()

        return {"message": "Liked"}, 201
    
class AddView(Resource):
    def post(self, vid_id):
        video = get_active_video(vid_id)
        if not video:
            abort(404, message="Video not found")

        view = View(video_id=vid_id)
        db.session.add(view)
        db.session.commit()

        return {"message": "Viewed"}, 201


api.add_resource(Video, "/video/<int:vid_id>")
api.add_resource(VideoHardDelete, "/video/<int:vid_id>/hard")
api.add_resource(VideoRestore, "/video/<int:vid_id>/restore")
api.add_resource(AddLike, "/video/<int:vid_id>/like")
api.add_resource(AddView, "/video/<int:vid_id>/view")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)