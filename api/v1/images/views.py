from flask import Flask, request, jsonify, abort, make_response, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url

from api.v1.models import Image

passport_blueprint = Blueprint('passport', __name__)


class Images(MethodView):
    """
    Handles image uploading
    """
    @jwt_required
    def post(self):
        """
        Method to upload image to a remote server(Cloudinary)
        and save image url to the database
        """
        user_id = get_jwt_identity()
        data = request.files
        response = upload(data["image_url"], public_id=user_id)
        user = Image.query.filter_by(user=user_id).first()
        if user:
            response = {
                'status': 'failed',
                'message': 'You have a saved passport. Delete to update'
            }
            return make_response(jsonify(response)), 400
        else:
            url, options = cloudinary_url(
                response['public_id'],
                format=response['format'],
                width=250,
                height=250,
                gravity="faces",
                crop="fill"
            )
            new_image = Image(
                image_url=url,
                user=user_id
            )
            new_image.save()
            response = {
                "status": "success",
                "message": "Passport image has been successfully uploaded"
            }
            return make_response(jsonify(response)), 201

    @jwt_required
    def get(self):
        """
        Retrieve passport url
        """
        user_id = get_jwt_identity()
        image = Image.query.filter_by(user=user_id).first()
        if not image:
            response = {
                'status' : 'failed',
                'message' : 'You have not uploaded your passport image'
            }
            return make_response(jsonify(response))
        else:
            response = {
                "status": "success",
                "image_url": image.image_url
            }
            return make_response(jsonify(response)), 200


# Api endpoints
passport_view = Images.as_view('images')

# Rules
passport_blueprint.add_url_rule('/passport/image', view_func=passport_view)
