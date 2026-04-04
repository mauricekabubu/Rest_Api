from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, UserMixin, login_manager, login_required, logout_user
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
api = Api(app)

#Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#Environment variables
secret_key = os.getenv("SECRET_KEY")

#Database models
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video[name={self.name}, views={self.views}, likes={self.likes}]"

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=True, unique=True)
    email = db.Column(db.String(200), nullable=True)


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_update_args.add_argument("views", type=int, help="Views of the video", required=True)
video_update_args.add_argument("likes", type=int, help="Likes of the video", required=True)


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video_obj = VideoModel.query.filter_by(id=video_id).first()
        if not video_obj:
            abort(404, message="Video not found")
        return video_obj, 200

    #Error put should be update not create
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video_obj = VideoModel.query.filter_by(id=video_id).first()
        if video_obj:
            abort(409, message="Video already exists")
        video_obj = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video_obj)
        db.session.commit()
        return video_obj, 201

<<<<<<< HEAD
    #201 -->created successfully
    #200 --> OK
    #500 -->Internal server error

=======
    #Put should be update
>>>>>>> 323912d (Final commit)
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        
        if not result:
            abort(http_status_code=404, message="Video does not exist, cannot update")
            
        if args["name"]:
            result.name = args["name"]
            
        if args["views"]:
            result.views = args["views"]
            
        if args["likes"]:
            result.likes = args["likes"]
            
        db.session.commit()
        
        return result
    
    
    def delete(self, video_id):
        video_obj = VideoModel.query.filter_by(id=video_id).first()
        if not video_obj:
            abort(404, message="Video not found")
        db.session.delete(video_obj)
        db.session.commit()
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
