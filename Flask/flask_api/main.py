from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)
     views = db.Column(db.Integer, nullable=False)
     likes = db.Column(db.Integer, nullable=False)
     
     def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"    
     

vid_put_args = reqparse.RequestParser()
vid_put_args.add_argument("name", type=str, help="name of the video",required=True)
vid_put_args.add_argument("views", type=int, help="views of the video",required=True)
vid_put_args.add_argument("likes", type=int, help="likes of the video",required=True)

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

class Video(Resource):

    @marshal_with(resource_fields)
    def get(self, vid_id):
        video = VideoModel.query.filter_by(id=vid_id).first()

        if not video:
            abort(404, message="Video not found")
        return video
    
    @marshal_with(resource_fields)
    def put(self, vid_id):
        args = vid_put_args.parse_args()
        video = VideoModel(id=vid_id, name=args["name"], views=args["views"], likes=args["likes"])

        if VideoModel.query.get(vid_id):
            abort(409, message="Video already exists")

        db.session.add(video)
        db.session.commit()

        return video, 201   
    def delete(self, vid_id):
        video = VideoModel.query.get(vid_id)

        if not video:
            abort(404, message="Video not found")

        db.session.delete(video)
        db.session.commit()

        return {"message": "Deleted successfully"}
                
api.add_resource(Video, "/video/<int:vid_id>")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)